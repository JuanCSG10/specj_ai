from pandas import DataFrame, concat
from typing import List, Dict

from specj_ai.experimental_descriptors.get_experimental_descriptors import (
    ExperimentalDescriptors,
)
from specj_ai.feature_strategies.mordred_feat import MordredFeatures
from specj_ai.feature_strategies.specj_ai_strategies import FeatureStrategy
from specj_ai.solvent_descriptors.load_solvent_descriptors import SolventDescriptors


import logging


class MordredSolv(FeatureStrategy):
    def get_features(
        self,
        molecule_smile: str,
        molecule_solvent: str,
        experimental_data: Dict[str, List[float]] = None,
    ) -> DataFrame:
        """Main function that calculates and returns mordred features for chromophore and solvent smile
        combined with empiric solvent and experimental features when using MordredSolv Strategy

        Args:
            molecule_smile (str): chromophore in smile format
            molecule_solvent (str): solvent in smile format
            experimental_data (Dict[str, List[float]], optional): dict of experimental data. Defaults to None.

        Returns:
            concated (DataFrame): DataFrame containing all the calculated descriptors
        """

        logging.info("mordred_solv_feat - get_features - IN")

        # Compute Mordred descriptors
        mordred_features = MordredFeatures()
        mordred_descriptors = mordred_features.get_features(
            molecule_smile, molecule_solvent
        )

        # Append solvent features
        solvent_descriptors = SolventDescriptors(molecule_solvent)
        empiric_descriptors = solvent_descriptors.concat_descriptors()
        concated = concat([mordred_descriptors, empiric_descriptors], axis=1)
        if experimental_data is not None:
            experimental_descriptors = ExperimentalDescriptors()
            experimental_descriptors = experimental_descriptors.get_descriptors(
                experimental_data
            )
            concated = concat([concated, experimental_descriptors], axis=1)
            return concated

        logging.info("mordred_solv_feat - get_features - OUT")
        return concated
