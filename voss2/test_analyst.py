from __future__ import annotations

import unittest

from analyst import VossForensicAnalyst


class GateTests(unittest.TestCase):
    def setUp(self):
        self.analyst = VossForensicAnalyst()

    def test_strong_temporal_gate(self):
        self.assertEqual(
            self.analyst._gate(
                "S1_PHYSICAL",
                0.60,
                0.02,
            ),
            "S1_PHYSICAL",
        )

    def test_cultural_gate_requires_margin(self):
        self.assertEqual(
            self.analyst._gate(
                "S6_CULTURAL_ONLY",
                0.70,
                0.10,
            ),
            "UNRESOLVED",
        )

    def test_hard_latent_gate_is_strict(self):
        self.assertEqual(
            self.analyst._gate(
                "S4_PLASTICITY",
                0.67,
                0.30,
            ),
            "UNRESOLVED",
        )

        self.assertEqual(
            self.analyst._gate(
                "S4_PLASTICITY",
                0.72,
                0.25,
            ),
            "S4_PLASTICITY",
        )


if __name__ == "__main__":
    unittest.main()
