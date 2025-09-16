from abc import ABC, abstractmethod
from pandas import DataFrame, Series
from typing import Dict, List


class ModelStrategy(ABC):
    """Abstract base class for model strategies."""

    @abstractmethod
    def predict(self, input_data: DataFrame) -> Series:
        pass


class FeatureStrategy(ABC):
    """Abstract base class for feature strategies."""

    @abstractmethod
    def get_features(
        self,
        molecule_smile: str,
        solvent_smile: str,
        experimental_data: Dict[str, List[float]],
    ) -> DataFrame:
        pass
