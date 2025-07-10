import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.custom_logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import numpy as np
import pandas as pd
from typing import List
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
from networksecurity.entity.artifacts_entity import DataIngestionArtifacts

mongo_db_url=os.getenv("mongo_db_url")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config=data_ingestion_config
        
        
    def export_data_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(mongo_db_url)
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
                
            df.replace({'na':np.nan},inplace=True)
            
            return df
            
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def split_train_test_split(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            
            test_set.to_csv(
                self.data_ingestion_config.test_file_path,index=False,header=True
            )
            
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_data_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe=dataframe)
            self.split_train_test_split(dataframe=dataframe)
            dataingestionartifact=DataIngestionArtifacts(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.test_file_path)
            return dataingestionartifact
        except Exception as e:
            raise CustomException(e,sys)

