from pandas import DataFrame
from rdkit.Chem import MolToSmiles, MolFromSmiles

import logging


def rename_solv_mordred(descriptors: DataFrame) -> DataFrame:
    """rename the solvent mordred descriptors to better identification

    Args:
        descriptors (DataFrame): solvent descriptors in a DataFrame fomat

    Returns:
        descriptors (DataFrame): renamed descriptors DataFrame
    """
    logging.info("utils - rename_solv_mordred - IN")
    descriptors.rename(
        columns={col: f"solv_{col}" for col in descriptors.columns}, inplace=True
    )
    logging.info("utils - rename_solv_mordred - OUT")
    return descriptors


def match_smile(smile_1: str, smile_2: str) -> bool:
    """Verify if a two given smiles are equal

    Args:
        smile_1 (str): smile_1 to compare
        smile_2 (str): smile_2 to compare

    Returns:
        (bool): True if matches, else False
    """

    if canonize_smile(smile_1) == canonize_smile(smile_2):
        return True
    else:
        return False


def canonize_smile(smile: str) -> str:
    """transform a str smile into a canonical smile

    Args:
        smile (str): target smile to transform

    Returns:
        canonized_smile (str): the canonized smile
    """
    try:
        canonized_smile = MolToSmiles(MolFromSmiles(smile), canonical=True)
        return canonized_smile
    except Exception as e:
        print(f"Error in canonize smile process: {e}")
