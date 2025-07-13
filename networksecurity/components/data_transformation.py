import os,sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.custom_logger import logging
from networksecurity.entity.artifacts_entity import DataValidationArtifacts,DataTransformationArtifacts
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_file,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact:DataValidationArtifacts=data_validation_artifact
        self.data_transformation_config:DataTransformationConfig=data_transformation_config
        
        
    @staticmethod
    def read_data(filepath:str)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def get_data_transformer_object(self)->Pipeline:
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            output_train_df=train_df[TARGET_COLUMN]
            output_train_df=output_train_df.replace(-1,0)
            
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            output_test_df=test_df[TARGET_COLUMN]
            output_test_df=output_test_df.replace(-1,0)
            
            processor=self.get_data_transformer_object()
            
            preprocessor_object=processor.fit(input_feature_train_df)
            transformed_input_feature_train=preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test=preprocessor_object.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_input_feature_train,np.array(output_train_df)]
            test_arr=np.c_[transformed_input_feature_test,np.array(output_test_df)]
            
            save_numpy_file(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_file(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            save_object("final_model/preprocessor.pkl",preprocessor_object)
            
            data_transformation_artifact=DataTransformationArtifacts(
                transform_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transform_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transform_train_file_path=self.data_transformation_config.transformed_train_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)