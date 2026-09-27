from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


PUBLIC_STATE_FIELDS = (
    "t",
    "p1_lon",
    "p2_lon",
    "p3_lon",
    "p4_lon",
    "d1",
    "d2",
    "illumination",
    "physical",
    "tidal",
    "angular_code",
    "sign_code",
)


def _safe_corr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) < 3:
        return 0.0
    if np.std(a) < 1e-10 or np.std(b) < 1e-10:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def _temporal_basis(states):
    arr = {
        key: np.asarray([float(row[key]) for row in states], dtype=float)
        for key in states[0]
    }
    basis = {}

    for key in (
        "physical",
        "tidal",
        "illumination",
        "angular_code",
        "sign_code",
    ):
        basis[key] = arr[key]

    phases = [
        arr[f"p{i}_lon"]
        for i in range(1, 5)
    ]

    for i, phase in enumerate(phases, 1):
        rad = np.radians(phase)
        for harmonic in (1, 2):
            basis[f"sin{harmonic}p{i}"] = np.sin(harmonic * rad)
            basis[f"cos{harmonic}p{i}"] = np.cos(harmonic * rad)

    generic_pairs = (
        (1, -1),
        (1, 1),
        (2, -1),
        (1, -2),
        (2, 1),
        (1, 2),
    )

    for i in range(4):
        for j in range(i + 1, 4):
            ri = np.radians(phases[i])
            rj = np.radians(phases[j])
            for ai, aj in generic_pairs:
                value = ai * ri + aj * rj
                name = f"{ai}p{i + 1}_{aj}p{j + 1}"
                basis[f"sin_{name}"] = np.sin(value)
                basis[f"cos_{name}"] = np.cos(value)

    return arr, basis


def extract_features(births, states, outcomes, culture):
    steps = len(states)
    agents = max(int(row["agent_id"]) for row in births) + 1

    count_t = np.zeros(steps)
    sum_t = np.zeros(steps)
    environment_t = np.zeros(steps)

    agent_sum = np.zeros(agents)
    agent_count = np.zeros(agents)

    coarse_bins = 6
    coarse_sum = np.zeros((agents, coarse_bins))
    coarse_count = np.zeros((agents, coarse_bins))

    fine_bins = 12
    fine_sum = np.zeros((agents, fine_bins))
    fine_count = np.zeros((agents, fine_bins))

    for row in outcomes:
        t = int(row["t"])
        agent = int(row["agent_id"])
        outcome = float(row["outcome"])
        environment = float(row["environment"])

        count_t[t] += 1
        sum_t[t] += outcome
        environment_t[t] = environment

        agent_sum[agent] += outcome
        agent_count[agent] += 1

        cbin = min(coarse_bins - 1, int(t * coarse_bins / steps))
        coarse_sum[agent, cbin] += outcome
        coarse_count[agent, cbin] += 1

        fbin = min(fine_bins - 1, int(t * fine_bins / steps))
        fine_sum[agent, fbin] += outcome
        fine_count[agent, fbin] += 1

    rate_t = np.divide(
        sum_t,
        count_t,
        out=np.zeros_like(sum_t),
        where=count_t > 0,
    )

    active = count_t > 0
    x_env = np.column_stack(
        [
            np.ones(active.sum()),
            environment_t[active],
        ]
    )
    beta = np.linalg.lstsq(
        x_env,
        rate_t[active],
        rcond=None,
    )[0]

    residual_t = np.zeros(steps)
    residual_t[active] = (
        rate_t[active]
        - x_env @ beta
    )

    _, basis = _temporal_basis(states)

    features = {
        "env_beta": float(beta[1]),
        "temporal_resid_sd": float(np.std(residual_t[active])),
    }

    temporal_corr = {}
    for name, values in basis.items():
        correlation = _safe_corr(
            residual_t[active],
            np.asarray(values)[active],
        )
        temporal_corr[name] = correlation
        features[f"corr_{name}"] = correlation

    features["maxabs_physical"] = max(
        abs(temporal_corr[key])
        for key in (
            "physical",
            "tidal",
            "illumination",
        )
    )
    features["maxabs_angular"] = max(
        abs(value)
        for key, value in temporal_corr.items()
        if "p" in key
        or key in (
            "angular_code",
            "sign_code",
        )
    )

    agent_rate = np.divide(
        agent_sum,
        agent_count,
        out=np.full(agents, np.nan),
        where=agent_count > 0,
    )

    birth_t = np.asarray(
        [
            int(row["birth_t"])
            for row in births
        ],
        dtype=int,
    )

    valid_agent = ~np.isnan(agent_rate)
    overall = float(np.nanmean(agent_rate))

    groups = defaultdict(list)
    for agent in np.where(valid_agent)[0]:
        groups[int(birth_t[agent])].append(agent)

    between_ss = 0.0
    within_ss = 0.0
    grouped_n = 0
    grouped_count = 0
    same_birth_products = []
    same_birth_absdiff = []
    group_means = []

    for ids in groups.values():
        values = agent_rate[ids]

        if len(ids) >= 2:
            mean = float(np.mean(values))
            group_means.append(mean)

            between_ss += len(ids) * (mean - overall) ** 2
            within_ss += float(np.sum((values - mean) ** 2))
            grouped_n += len(ids)
            grouped_count += 1

            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    ai = ids[i]
                    aj = ids[j]
                    same_birth_products.append(
                        (agent_rate[ai] - overall)
                        * (agent_rate[aj] - overall)
                    )
                    same_birth_absdiff.append(
                        abs(agent_rate[ai] - agent_rate[aj])
                    )

    if (
        grouped_count > 1
        and grouped_n > grouped_count
        and within_ss > 0
    ):
        features["birth_anova_f"] = (
            between_ss / (grouped_count - 1)
        ) / (
            within_ss / (grouped_n - grouped_count)
        )
        features["birth_between_frac"] = (
            between_ss
            / (between_ss + within_ss)
        )
    else:
        features["birth_anova_f"] = 0.0
        features["birth_between_frac"] = 0.0

    features["same_birth_cov"] = (
        float(np.mean(same_birth_products))
        if same_birth_products
        else 0.0
    )
    features["same_birth_absdiff"] = (
        float(np.mean(same_birth_absdiff))
        if same_birth_absdiff
        else 0.0
    )
    features["same_birth_pairs"] = float(len(same_birth_products))
    features["birth_group_mean_sd"] = (
        float(np.std(group_means))
        if group_means
        else 0.0
    )

    birth_states = [
        states[min(t, steps - 1)]
        for t in birth_t
    ]
    _, birth_basis = _temporal_basis(birth_states)

    for name, values in birth_basis.items():
        features[f"birthcorr_{name}"] = _safe_corr(
            agent_rate[valid_agent],
            np.asarray(values)[valid_agent],
        )

    features["maxabs_birthcorr"] = max(
        abs(value)
        for key, value in features.items()
        if key.startswith("birthcorr_")
    )

    coarse_rate = np.divide(
        coarse_sum,
        coarse_count,
        out=np.full_like(coarse_sum, np.nan),
        where=coarse_count > 0,
    )

    slopes = []
    differences = []
    roughness = []
    x_coarse = np.arange(coarse_bins)

    for agent in range(agents):
        values = coarse_rate[agent]
        mask = ~np.isnan(values)
        if mask.sum() >= 4:
            slopes.append(
                np.polyfit(
                    x_coarse[mask],
                    values[mask],
                    1,
                )[0]
            )
            selected = values[mask]
            differences.append(
                selected[-1] - selected[0]
            )
            roughness.append(
                float(np.mean(np.diff(selected) ** 2))
            )

    features["agent_slope_sd"] = (
        float(np.std(slopes))
        if slopes
        else 0.0
    )
    features["agent_diff_sd"] = (
        float(np.std(differences))
        if differences
        else 0.0
    )
    features["agent_rough_mean"] = (
        float(np.mean(roughness))
        if roughness
        else 0.0
    )
    features["agent_rate_sd"] = float(np.nanstd(agent_rate))

    fine_rate = np.divide(
        fine_sum,
        fine_count,
        out=np.full_like(fine_sum, np.nan),
        where=fine_count > 0,
    )

    fine_qvar = []
    fine_qvar_per_agent = []
    late_early = []
    curvature = []

    for agent in range(agents):
        values = fine_rate[agent]
        selected = values[~np.isnan(values)]

        if len(selected) >= 8:
            qvar = float(np.mean(np.diff(selected) ** 2))
            fine_qvar.append(qvar)
            fine_qvar_per_agent.append(qvar)
            late_early.append(
                float(
                    np.mean(selected[-3:])
                    - np.mean(selected[:3])
                )
            )
            curvature.append(
                float(
                    np.mean(
                        np.diff(selected, n=2) ** 2
                    )
                )
            )

    features["fine_qvar_mean"] = (
        float(np.mean(fine_qvar))
        if fine_qvar
        else 0.0
    )
    features["fine_qvar_sd"] = (
        float(np.std(fine_qvar_per_agent))
        if fine_qvar_per_agent
        else 0.0
    )
    features["late_early_sd"] = (
        float(np.std(late_early))
        if late_early
        else 0.0
    )
    features["curvature_mean"] = (
        float(np.mean(curvature))
        if curvature
        else 0.0
    )

    features["culture_present"] = 1.0 if culture else 0.0

    if culture:
        values = np.asarray(
            [
                float(row["mean_belief"])
                for row in culture
            ],
            dtype=float,
        )
        times = np.asarray(
            [
                float(row["t"])
                for row in culture
            ],
            dtype=float,
        )

        features["culture_mean"] = float(np.mean(values))
        features["culture_end"] = float(values[-1])
        features["culture_sd"] = float(np.std(values))
        features["culture_slope"] = (
            float(np.polyfit(times, values, 1)[0])
            if len(values) > 1
            else 0.0
        )
    else:
        features["culture_mean"] = 0.0
        features["culture_end"] = 0.0
        features["culture_sd"] = 0.0
        features["culture_slope"] = 0.0

    return features


def _read_csv(path):
    with Path(path).open(
        newline="",
        encoding="utf-8",
    ) as handle:
        return list(csv.DictReader(handle))


def load_public_run(run_dir):
    run_dir = Path(run_dir)

    births = _read_csv(
        run_dir / "agent_births.csv"
    )
    states = _read_csv(
        run_dir / "celestial_state.csv"
    )
    outcomes = _read_csv(
        run_dir / "agent_outcomes.csv"
    )

    culture_path = (
        run_dir
        / "cultural_claims.csv"
    )

    culture = (
        _read_csv(culture_path)
        if culture_path.exists()
        and culture_path.stat().st_size > 0
        else []
    )

    return births, states, outcomes, culture


def frame(feature_rows):
    return pd.DataFrame(feature_rows).fillna(0.0)
