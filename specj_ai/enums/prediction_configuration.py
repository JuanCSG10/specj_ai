from enum import Enum

from specj_ai.feature_strategies.mordred_feat import MordredFeatures
from specj_ai.feature_strategies.mordred_solv_feat import MordredSolv
from specj_ai.models.get_model import SklearnModel


class PredictionConfiguration(Enum):
    """All the available configurations for predicting molecular properties"""

    CONFIG = {
        "Lifetime": {
            "subsystems": {
                "all_molecules": {
                    "feature_sets": {
                        "mordred_solv": {
                            "model_path": SklearnModel.rf_model_tao_sistema_1_mordred_forzado.value,
                            "feature_strategy": MordredSolv(),
                        }
                    }
                },
                "cyanine_dye": {
                    "feature_sets": {
                        "mordred": {
                            "model_path": SklearnModel.rf_model_tao_system_2_mordred.value,
                            "feature_strategy": MordredFeatures(),
                        },
                        "mordred_solv": {
                            "model_path": SklearnModel.rf_model_tao_sistema_2_mordred_forzado.value,
                            "feature_strategy": MordredSolv(),
                        },
                    }
                },
                "cyanine_dye_epsilon": {
                    "feature_sets": {
                        "mordred_solv": {
                            "model_path": SklearnModel.rf_model_tao_sistema_3_mordred_forzado.value,
                            "feature_strategy": MordredSolv(),
                        }
                    }
                },
            }
        },
        "Quantum Yield": {
            "subsystems": {
                "all_molecules": {
                    "feature_sets": {
                        "mordred_solv": {
                            "model_path": SklearnModel.rf_model_quantum_yield_sistema_2_mordred_forzado.value,
                            "feature_strategy": MordredSolv(),
                        }
                    }
                },
                "cyanine_dye": {
                    "feature_sets": {
                        "mordred": {
                            "model_path": SklearnModel.rf_model_quantum_yield_sistema_2_mordred.value,
                            "feature_strategy": MordredFeatures(),
                        }
                    }
                },
            }
        },
    }
