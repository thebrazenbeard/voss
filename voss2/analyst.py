from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier


WORLD_TYPES = (
    "S0_NULL",
    "S1_PHYSICAL",
    "S2_NATAL_SEED",
    "S3_RUNTIME",
    "S4_PLASTICITY",
    "S5_COMMON_CAUSE",
    "S6_CULTURAL_ONLY",
    "S7_WEAK_SIGNAL_CULTURAL",
)

STRONG_TEMPORAL = {
    "S1_PHYSICAL",
    "S3_RUNTIME",
    "S5_COMMON_CAUSE",
}

CULTURAL = {
    "S6_CULTURAL_ONLY",
    "S7_WEAK_SIGNAL_CULTURAL",
}

HARD_LATENT = {
    "S0_NULL",
    "S2_NATAL_SEED",
    "S4_PLASTICITY",
}


@dataclass(frozen=True)
class Verdict:
    forced_choice: str
    voss_verdict: str
    max_probability: float
    margin: float
    top_probabilities: tuple
    evidence: dict


class VossForensicAnalyst:
    def __init__(self):
        self.model = ExtraTreesClassifier(
            n_estimators=1200,
            min_samples_leaf=2,
            max_features=0.8,
            random_state=77,
            class_weight="balanced",
        )
        self.columns = None

    def fit(self, features, labels):
        frame = pd.DataFrame(features).fillna(0.0)
        self.columns = list(frame.columns)
        self.model.fit(frame[self.columns], labels)
        return self

    def _gate(self, label, max_probability, margin):
        if label in STRONG_TEMPORAL:
            return (
                label
                if max_probability >= 0.55
                else "UNRESOLVED"
            )

        if label in CULTURAL:
            return (
                label
                if (
                    max_probability >= 0.58
                    and margin >= 0.18
                )
                else "UNRESOLVED"
            )

        if label in HARD_LATENT:
            return (
                label
                if (
                    max_probability >= 0.68
                    and margin >= 0.22
                )
                else "UNRESOLVED"
            )

        return "UNRESOLVED"

    def predict_one(self, feature_row):
        if self.columns is None:
            raise RuntimeError(
                "analyst must be fit before prediction"
            )

        frame = pd.DataFrame(
            [feature_row]
        ).fillna(0.0)

        for column in self.columns:
            if column not in frame:
                frame[column] = 0.0

        frame = frame[self.columns]

        probabilities = self.model.predict_proba(frame)[0]
        order = np.argsort(probabilities)[::-1]

        forced = self.model.classes_[order[0]]
        max_probability = float(probabilities[order[0]])
        second_probability = float(probabilities[order[1]])
        margin = max_probability - second_probability

        verdict = self._gate(
            forced,
            max_probability,
            margin,
        )

        top = tuple(
            (
                str(self.model.classes_[index]),
                float(probabilities[index]),
            )
            for index in order[:3]
        )

        evidence = {
            "culture_present": float(
                feature_row.get(
                    "culture_present",
                    0.0,
                )
            ),
            "maxabs_physical": float(
                feature_row.get(
                    "maxabs_physical",
                    0.0,
                )
            ),
            "maxabs_angular": float(
                feature_row.get(
                    "maxabs_angular",
                    0.0,
                )
            ),
            "birth_anova_f": float(
                feature_row.get(
                    "birth_anova_f",
                    0.0,
                )
            ),
            "same_birth_cov": float(
                feature_row.get(
                    "same_birth_cov",
                    0.0,
                )
            ),
            "agent_slope_sd": float(
                feature_row.get(
                    "agent_slope_sd",
                    0.0,
                )
            ),
        }

        return Verdict(
            forced_choice=str(forced),
            voss_verdict=str(verdict),
            max_probability=max_probability,
            margin=margin,
            top_probabilities=top,
            evidence=evidence,
        )
