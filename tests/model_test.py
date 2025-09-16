from unittest import TestCase, main

from specj_ai.specj_ai_context import MolecularPropertyPredictor
from specj_ai.feature_strategies.spec_model import SpecModel
from specj_ai.load_strategies import load_strategy


class ModelTest(TestCase):
    def setUp(self):
        self.molecule_smile = (
            "CCN(CC)C1=CC2=C(C=C1)C(=C3C=CC(=[N+](CC)CC)C=C3O2)C4=CC=CC=C4C(=O)O.[Cl-]"
        )
        self.solvent_smile = "O"

        self.system = "Lifetime"
        self.subsystem = "cyanine_dye_epsilon"
        self.feature_set = "mordred_solv"
        self.experimental_features = {
            "Absorption max (eV)": [3.15],
            "Emission max (eV)": [4.7],
            "log(e/mol-1 dm3 cm-1)": [],
        }
        self.predictor = MolecularPropertyPredictor(
            *load_strategy(self.system, self.subsystem, self.feature_set)
        )

    def test_model_strategy(self):
        self.assertIsInstance(self.predictor.model_strategy, SpecModel)

    def test_invalid_strategy(self):
        invalid_feature_set = "mordred_experimental"
        with self.assertRaises(ValueError):
            MolecularPropertyPredictor(
                *load_strategy(self.system, self.subsystem, invalid_feature_set)
            )

    def test_prediction(self):
        predictions = self.predictor.predict(
            self.molecule_smile, self.solvent_smile, self.experimental_features
        )
        self.assertIsInstance(predictions[0], float)


if __name__ == "__main__":
    main()
