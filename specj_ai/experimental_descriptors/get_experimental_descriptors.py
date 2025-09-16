from pandas import DataFrame
from typing import List, Dict

import logging


class ExperimentalDescriptors:

    def __init__(self):

        self.experimental_descriptors = {
            "Absorption max (eV)": [None],
            "Emission max (eV)": [None],
            "Stokes shift (eV)": [None],
            "log(e/mol-1 dm3 cm-1)": [None],
        }

    def calculate_stokes_shift(self) -> List[float]:
        """Function that calculates stokes shift from absorption and emission

        Returns:
            list[float]: List containing the calculated stokes shift
        """
        absorption_max = self.experimental_descriptors["Absorption max (eV)"][0]
        emmision_max = self.experimental_descriptors["Emission max (eV)"][0]
        stokes_shift = abs(emmision_max - absorption_max)
        return [stokes_shift]

    def get_descriptors(self, experimental_input: Dict[str, List[float]]) -> DataFrame:
        """Main function that returns the experimental descriptors given by an input and
        transform it to a pandas dataframe

        Args:
            experimental_input (dict): experimental input: it may include absorption, emission and loge
            properties

        Returns:
            experimental_descriptros_df (DataFrame): DataFrame that contains the experimental data
        """
        logging.info("get_experimental_descriptors - get_descriptors - IN")

        experimental_descriptors_df = DataFrame.from_dict(self.experimental_descriptors)

        absorption_input = experimental_input["Absorption max (eV)"]
        emmision_input = experimental_input["Emission max (eV)"]
        loge_input = experimental_input["log(e/mol-1 dm3 cm-1)"]

        if absorption_input and emmision_input and loge_input:

            self.experimental_descriptors["Absorption max (eV)"] = absorption_input
            self.experimental_descriptors["Emission max (eV)"] = emmision_input
            self.experimental_descriptors["Stokes shift (eV)"] = (
                self.calculate_stokes_shift()
            )
            self.experimental_descriptors["log(e/mol-1 dm3 cm-1)"] = loge_input
            experimental_descriptors_df = DataFrame.from_dict(
                self.experimental_descriptors
            )
            return experimental_descriptors_df
        logging.info("get_experimental_descriptors - get_descriptors - OUT")
        return experimental_descriptors_df
