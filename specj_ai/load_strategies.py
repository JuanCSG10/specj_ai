from typing import Tuple

from specj_ai.enums.prediction_configuration import PredictionConfiguration
from specj_ai.feature_strategies.specj_ai_strategies import (
    FeatureStrategy,
    ModelStrategy,
)
from specj_ai.feature_strategies.spec_model import SpecModel


def load_strategy(
    system: str, subsystem: str, feature_set: str
) -> Tuple[ModelStrategy, FeatureStrategy]:
    """Function that parse all the needed configuration from PredictionConfiguration enum

    Args:
        system (str): main system, it could be "Lifime (ns)", "Quantum yield"
        subsystem (str): subsystem that correspond to the subset of molecules: "all_molecules", "cyanine_dye"
        feature_set (str): the desired feature set to use: "mordred" or "mordred_solv"

    Raises:
        ValueError: If a given configuration is not available

    Returns:
        (Tuple[ModelStrategy, FeatureStrategy]): The ModelStrategy and FeatureStrategy to use
    """

    try:
        system_config = PredictionConfiguration.CONFIG.value[system]
        subsystem_config = system_config["subsystems"][subsystem]
        feature_set_config = subsystem_config["feature_sets"][feature_set]
        model_path = feature_set_config["model_path"]
        if model_path:
            model_strategy = SpecModel(model_path)
        else:
            print("Not model found")

        feature_strategy = feature_set_config["feature_strategy"]
        return model_strategy, feature_strategy
    except KeyError as e:
        raise ValueError(f"Invalid Configuration: {e}")
