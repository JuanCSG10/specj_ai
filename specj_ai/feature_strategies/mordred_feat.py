from pandas import DataFrame, concat
from typing import Dict, List

from specj_ai.feature_strategies.specj_ai_strategies import FeatureStrategy
from specj_ai.utils.mordred_calculator import MordredCalculator
from specj_ai.utils.utils import rename_solv_mordred

import logging


class MordredFeatures(FeatureStrategy):
    def get_features(
        self,
        molecule_smile: str,
        molecule_solvent: str,
        experimental_data: Dict[str, List[float]] = None,
    ) -> DataFrame:
        """Main function that calculates and returns mordred features for chromophore and solvent smile
        when using Mordred Strategy

        Args:
            molecule_smile (str): chromophore in smile format
            molecule_solvent (str): solvent in smile format
            experimental_data (Dict[str, List[float]]): Defaults to None

        Returns:
            concated (DataFrame): DataFrame containing all the calculated mordred descriptors
        """
        logging.info("mordred_feat - get_features - IN")
        mordred_calculator = MordredCalculator()
        mol_descriptors = mordred_calculator.calculate_descriptors(molecule_smile)
        solv_descriptors = rename_solv_mordred(
            mordred_calculator.calculate_descriptors(molecule_solvent)
        )
        concated = concat([mol_descriptors, solv_descriptors], axis=1)
        logging.info("mordred_feat - get_features - OUT")
        return concated
