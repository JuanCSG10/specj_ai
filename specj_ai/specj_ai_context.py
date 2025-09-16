from pandas import Series

from specj_ai.feature_strategies.specj_ai_strategies import (
    ModelStrategy,
    FeatureStrategy,
)


class MolecularPropertyPredictor:
    """main class that uses a specific model strategy and feature strategy to do a prediction"""

    def __init__(
        self, model_strategy: ModelStrategy, feature_strategy: FeatureStrategy
    ):
        self.model_strategy = model_strategy
        self.feature_strategy = feature_strategy

    def predict(
        self, molecule_smile: str, solvent_smile: str, experimental_data: dict = None
    ) -> Series:
        """main function that do inferece given a chromophore smile, its solvent, and optional experimental_data

        Args:
            molecule_smile (str): target chromophore smile
            solvent_smile (str): solvent smile
            experimental_data (dict, optional): If you have experimental features. Defaults to None.

        Returns:
            (Series): a Series containing the predicted value for a given system
        """
        features = self.feature_strategy.get_features(
            molecule_smile, solvent_smile, experimental_data
        )
        return self.model_strategy.predict(features)
