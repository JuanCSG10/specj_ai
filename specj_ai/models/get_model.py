from enum import Enum
from os import path

base_path = path.dirname(path.abspath(__file__))
models_folder = "models"


class SklearnModel(Enum):
    """Enum that contains the available models"""

    # system 1 models
    rf_model_tao_sistema_1_mordred_forzado = path.join(
        base_path, models_folder, "rf_model_tao_sistema_1_mordred_forzado.pkl"
    )

    # system 2 models
    rf_model_tao_sistema_2_mordred_forzado = path.join(
        base_path, models_folder, "rf_model_tao_sistema_2_mordred_forzado.pkl"
    )
    rf_model_tao_system_2_mordred = path.join(
        base_path, models_folder, "rf_model_tao_sistema_2_mordred.pkl"
    )
    rf_model_quantum_yield_sistema_2_mordred = path.join(
        base_path, models_folder, "rf_model_quantum_yield_sistema_2_mordred.pkl"
    )
    rf_model_quantum_yield_sistema_2_mordred_forzado = path.join(
        base_path, models_folder, "rf_model_quantum_yield_sistema_2_mordred_forzado.pkl"
    )

    # system 3 models
    rf_model_tao_sistema_3_mordred_forzado = path.join(
        base_path, models_folder, "rf_model_tao_sistema_3_mordred_forzado.pkl"
    )
