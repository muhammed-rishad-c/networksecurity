from networksecurity.entity.artifacts_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import CustomException
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
import os,sys
from scipy.stats import ks_2samp
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_column=len(self._schema_config)
            if len(dataframe.columns)==number_of_column:
                return True
            return False
        except Exception as e:
            raise CustomException(e,sys)
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(filepath=drift_report_file_path,content=report)
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message="train dataframe does not contain all columns"
                
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message="train dataframe does not contain all columns"
                
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            
            data_validation_artifact=DataValidationArtifacts(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            
        except Exception as e:
            raise CustomException(e,sys)