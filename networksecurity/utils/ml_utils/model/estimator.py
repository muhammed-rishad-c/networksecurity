from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os,sys
from networksecurity.exception.exception import CustomException

class NetworkModel:
    def __init__(self,preprocessor,model):
        self.preprocessor=preprocessor
        self.model=model
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)