import os,sys

from networksecurity.exception.exception import CustomException
from networksecurity.entity.artifacts_entity import DataTransformationArtifacts,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object,load_object,load_numpy_array,evaluate_model
from networksecurity.utils.ml_utils.metric.classification_metrics import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifacts,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config
        
        
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)
        
        best_model_score=max(sorted(model_report.values()))
        
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model=models[best_model_name]
        
        y_pred_train=best_model.predict(x_train)
        
        classification_train_metrics=get_classification_score(y_true=y_train,y_pred=y_pred_train)
        
        y_pred_test=best_model.predict(x_test)
        classification_test_metrics=get_classification_score(y_true=y_test,y_pred=y_pred_test)
        
        preprocessor=load_object(self.data_transformation_artifact.transform_object_file_path)
        
        dir_name=os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(dir_name,exist_ok=True)
        
        network_model=NetworkModel(preprocessor=preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
        
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metrics,
                             test_metric_artifact=classification_test_metrics)
        return model_trainer_artifact
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transform_train_file_path
            test_file_path=self.data_transformation_artifact.transform_test_file_path
            
            train_arr=load_numpy_array(train_file_path)
            test_arr=load_numpy_array(test_file_path)
            
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model_trainer_artifact=self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)