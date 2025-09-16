from rdkit import Chem
from typing import Tuple
import logging


class SmileValidator:

    def __init__(self, smile):
        self.smile = smile

    def validate_smile(self) -> Tuple[bool, str]:
        """Validates if a given str smile is valid

        Returns:
            Tuple[bool, str]: True if it is valid else False, a descripting message
        """
        logging.info("smile_validator - validate_smile - IN")
        try:
            mol = self.transform_to_mol()
            if mol is not None:
                logging.info("smile_validator - validate_smile - OUT")
                return True, "Valid SMILES"
            else:
                logging.warning("smile_validator - validate_smile - OUT")
                return False, "Invalid SMILES: Could not parse molecule"
        except Exception as e:
            logging.error("smile_validator - validate_smile - Error validating smile")
            return False, f"Error: {str(e)}"

    def transform_to_mol(self):
        """function that transform an smile to a mol object

        Returns:
            (Mol): Mol object
        """
        return Chem.MolFromSmiles(self.smile)
