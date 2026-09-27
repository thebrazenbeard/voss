from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyst import VossForensicAnalyst, WORLD_TYPES
from feature_extractor import extract_features


AGENTS = 200
STEPS = 360
CALIBRATION_PER_CLASS = 20
EVALUATION_PER_CLASS = 25
CALIBRATION_BASE = 10000
EVALUATION_BASE = 30000
CLASS_STRIDE = 1000


def load_simulator(path):
    path = Path(path)
    spec = importlib.util.spec_from_file_location(
        "on_theo_reference_simulation",
        path,
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def public_projection(raw):
    births, states, outcomes, culture, truth = raw

    public_births = [
        {
            "agent_id": row["agent_id"],
            "birth_t": row["birth_t"],
        }
        for row in births
    ]

    public_states = [
        {
            key: value
            for key, value in row.items()
            if key != "controller"
        }
        for row in states
    ]

    public_outcomes = [
        {
            "t": row["t"],
            "agent_id": row["agent_id"],
            "outcome": row["outcome"],
            "environment": row["environment"],
        }
        for row in outcomes
    ]

    public_culture = [
        {
            "t": row["t"],
            "claim": row["claim"],
            "mean_belief": row["mean_belief"],
        }
        for row in culture
    ]

    return (
        public_births,
        public_states,
        public_outcomes,
        public_culture,
    ), truth


def seed_for(base, class_index, offset):
    return (
        base
        + class_index * CLASS_STRIDE
        + offset
    )


def confusion(rows, field):
    labels = list(WORLD_TYPES) + (
        ["UNRESOLVED"]
        if field == "voss_verdict"
        else []
    )

    matrix = {
        actual: {
            predicted: 0
            for predicted in labels
        }
        for actual in WORLD_TYPES
    }

    for row in rows:
        matrix[row["actual"]][row[field]] += 1

    return matrix


def evaluate_accuracy(rows, field):
    resolved = [
        row
        for row in rows
        if row[field] != "UNRESOLVED"
    ]

    exact = sum(
        row[field] == row["actual"]
        for row in resolved
    )

    return {
        "total": len(rows),
        "resolved": len(resolved),
        "coverage": (
            len(resolved) / len(rows)
            if rows
            else 0.0
        ),
        "exact_correct": exact,
        "accuracy_resolved": (
            exact / len(resolved)
            if resolved
            else None
        ),
        "overall_exact": (
            exact / len(rows)
            if rows
            else None
        ),
    }


def run_benchmark(simulator):
    calibration_features = []
    calibration_labels = []

    for class_index, world in enumerate(WORLD_TYPES):
        for offset in range(CALIBRATION_PER_CLASS):
            seed = seed_for(
                CALIBRATION_BASE,
                class_index,
                offset,
            )

            public, _ = public_projection(
                simulator.run(
                    world,
                    AGENTS,
                    STEPS,
                    seed,
                )
            )

            calibration_features.append(
                extract_features(*public)
            )
            calibration_labels.append(world)

    analyst = VossForensicAnalyst().fit(
        calibration_features,
        calibration_labels,
    )

    predictions = []

    for class_index, actual_world in enumerate(WORLD_TYPES):
        for offset in range(EVALUATION_PER_CLASS):
            seed = seed_for(
                EVALUATION_BASE,
                class_index,
                offset,
            )

            raw = simulator.run(
                actual_world,
                AGENTS,
                STEPS,
                seed,
            )

            public, private_truth = public_projection(raw)

            # Critical blind boundary:
            # only public enters feature extraction and predict_one.
            features = extract_features(*public)
            verdict = analyst.predict_one(features)

            # The held-out label is attached only after prediction.
            predictions.append(
                {
                    "actual": actual_world,
                    "seed": seed,
                    "forced_choice": verdict.forced_choice,
                    "voss_verdict": verdict.voss_verdict,
                    "max_probability": verdict.max_probability,
                    "margin": verdict.margin,
                    "top_probabilities": list(
                        verdict.top_probabilities
                    ),
                    "evidence": verdict.evidence,
                    "private_coupling": private_truth["coupling"],
                }
            )

    report = {
        "schema": "VOSS_ASTROLOGY_BLIND_BENCHMARK_REPORT_V1",
        "agents": AGENTS,
        "steps": STEPS,
        "calibration_per_class": CALIBRATION_PER_CLASS,
        "evaluation_per_class": EVALUATION_PER_CLASS,
        "evaluation_runs": len(predictions),
        "forced": evaluate_accuracy(
            predictions,
            "forced_choice",
        ),
        "cautious": evaluate_accuracy(
            predictions,
            "voss_verdict",
        ),
        "forced_confusion": confusion(
            predictions,
            "forced_choice",
        ),
        "cautious_confusion": confusion(
            predictions,
            "voss_verdict",
        ),
    }

    return predictions, report


def write_outputs(out_dir, predictions, report):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    (out / "report.json").write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    with (
        out
        / "predictions.csv"
    ).open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "actual",
                "seed",
                "forced_choice",
                "voss_verdict",
                "max_probability",
                "margin",
            ],
        )
        writer.writeheader()
        for row in predictions:
            writer.writerow(
                {
                    key: row[key]
                    for key in writer.fieldnames
                }
            )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--simulator",
        required=True,
        help=(
            "Path to on-theo "
            "experiments/astrology/reference_simulation.py"
        ),
    )
    parser.add_argument(
        "--out",
        default="voss-benchmark-output",
    )
    args = parser.parse_args(argv)

    simulator = load_simulator(args.simulator)
    predictions, report = run_benchmark(simulator)
    write_outputs(
        args.out,
        predictions,
        report,
    )


if __name__ == "__main__":
    main()
