from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import CustomException
from networksecurity.components.data_validation import DataValidation
import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        dataingestion=DataIngestion(data_ingestion_config)
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        data_validation=data_validation.initiate_data_validation()
        print(data_validation)
        
        
    except Exception as e:
        raise CustomException(e,sys)