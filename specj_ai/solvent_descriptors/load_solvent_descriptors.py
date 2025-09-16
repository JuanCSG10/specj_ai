from os import path
from pandas import DataFrame, concat, read_csv

from specj_ai.utils.utils import match_smile

import logging

base_path = path.dirname(path.abspath(__file__))
minnesota_solv_path = path.join(base_path, "minnesota_solv.csv")
empiric_solv_path = path.join(base_path, "empiric_solv.csv")


class SolventDescriptors:

    def __init__(self, solvent_smile: str):

        self.solvent_smile = solvent_smile
        self.minnesota_descriptors = read_csv(minnesota_solv_path)
        self.empiric_descriptors = read_csv(empiric_solv_path)

    def concat_descriptors(self) -> DataFrame:
        """It concats all the descriptors available in all the databases

        Returns:
            DataFrame: all the concated descriptors
        """
        logging.info("load_solvent_descriptors - concat_descriptors - IN")
        try:
            descriptors_list = []
            descriptors_list.append(self.get_descriptors(self.minnesota_descriptors))
            descriptors_list.append(self.get_descriptors(self.empiric_descriptors))
            concated_descriptors = concat(descriptors_list)
            concated_descriptors = concated_descriptors.drop(
                [r"\alpha_1", r"\beta_1", "n", "n25", "e", "Solvent"]
            )
            logging.info("load_solvent_descriptors - concat_descriptors - OUT")
            return concated_descriptors.to_frame().T
        except Exception:
            logging.error("Solvent not found in database")

    def get_descriptors(self, descriptors_df: DataFrame):
        """Search the solvent smile in the descriptor_df database and returns its descriptors

        Args:
            descriptors_df (DataFrame): Database that contains all the solvent empiric descriptors

        Returns:
             extracted_row (pd.Series): all the solvent descriptors for a given solvent smile
        """
        logging.info("load_solvent_descriptors - get_descriptors - IN")
        for index, solvent in enumerate(descriptors_df["Solvent"]):
            try:
                if match_smile(solvent, self.solvent_smile):
                    extracted_row = descriptors_df.iloc[index]
                    extracted_row = extracted_row.drop(["Name"])
                    logging.info("load_solvent_descriptors - get_descriptors - OUT")
                    return extracted_row
            except Exception:
                logging.error(
                    "load_solvent_descriptors - get_descriptors - Error matching solvent"
                )
