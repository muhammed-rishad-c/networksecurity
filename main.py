from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import CustomException
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
import sys
from networksecurity.entity.config_entity import (DataIngestionConfig,
                                                  DataValidationConfig,
                                                  DataTransformationConfig,
                                                  ModelTrainerConfig)
from networksecurity.entity.config_entity import TrainingPipelineConfig


if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        dataingestion=DataIngestion(data_ingestion_config)
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        ##print(dataingestionartifact)
        
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        data_validation_artifact=data_validation.initiate_data_validation()
        ##print(data_validation)
        
        data_tranformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_tranformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        ##print(data_transformation_artifact)
        
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        
        
        
        
        
        
        
        
    except Exception as e:
        raise CustomException(e,sys)