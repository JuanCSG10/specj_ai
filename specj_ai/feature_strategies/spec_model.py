from pandas import DataFrame

from specj_ai.feature_strategies.specj_ai_strategies import ModelStrategy

import logging


class SpecModel(ModelStrategy):

    def __init__(self, model_path: str):
        """loads the model

        Args:
            model_path (str): path where model is stored
        """
        from joblib import load

        self.model = load(model_path)

    def predict(self, input_data: DataFrame):
        """function that uses the sklearn model for inference

        Args:
            input_data (DataFrame): DataFrame that contains all the features

        Returns:
            (ndarray): array containing the predicted value
        """
        logging.info("spec_model - predict - IN")
        features_in = input_data[self.model.feature_names_in_]
        logging.info("spec_model - predict - OUT")
        return self.model.predict(features_in)
