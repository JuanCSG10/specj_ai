from mordred import Calculator, descriptors
from pandas import DataFrame
from rdkit import Chem
from rdkit.Chem import AllChem

from specj_ai.utils.smile_validator import SmileValidator

import logging


class MordredCalculator:

    def calculate_descriptors(
        self, smile: str, ignore_calc_3d: bool = False
    ) -> DataFrame:
        """Calculate mordred descriptors given a valid smile

        Args:
            smile (str): target smile to calculate its descriptors
            ignore_calc_3d (bool, optional): If you want to generate 3d descriptors. Defaults to False.

        Returns:
            mol_descriptor_df (DataFrame): all the calculated mordred descriptors in a DataFrame format
        """
        logging.info("mordred_calculator - calculate_descriptors - IN")
        try:
            if SmileValidator(smile).validate_smile()[0]:
                mol = Chem.AddHs(SmileValidator(smile).transform_to_mol())
                params = AllChem.srETKDGv3()
                params.useSmallRingTorsions = True
                params.useMacrocycleTorsions = True
                AllChem.EmbedMolecule(mol, params)
                calc = Calculator(descriptors, ignore_3D=ignore_calc_3d)
                mol_descriptor_df = calc.pandas([mol])
                logging.info("mordred_calculator - calculate_descriptors - OUT")
                return mol_descriptor_df
        except NameError:
            logging.error("mordred_calculator - calculate_descriptors - Invalid Smile")
