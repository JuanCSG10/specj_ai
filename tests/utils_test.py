from pandas import DataFrame
from unittest import TestCase, main

from specj_ai.utils.smile_validator import SmileValidator
from specj_ai.utils.mordred_calculator import MordredCalculator


class UtilsTest(TestCase):

    def test_validator_true(self):
        valid_smile = "CCCO"
        validator = SmileValidator(valid_smile)
        self.assertTrue(validator.validate_smile()[0])

    def test_validator_false(self):
        invalid_smile = "COOOOCHU"
        validator = SmileValidator(invalid_smile)
        self.assertFalse(validator.validate_smile()[0])

    def test_mordred_calculator(self):
        smile = "CO"
        calculator = MordredCalculator()
        descriptors = calculator.calculate_descriptors(smile)
        self.assertIsInstance(descriptors, DataFrame)


if __name__ == "__main__":
    main()
