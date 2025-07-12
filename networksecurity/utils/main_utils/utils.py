import yaml
from networksecurity.exception.exception import CustomException
import os,sys
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath,'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
            
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_numpy_file(filepath:str,array:np.array):
    try:
        dir_name=os.path.dirname(filepath)
        os.makedirs(dir_name,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(filepath:str,obj:object)->None:
    try:
        dir_name=os.path.dirname(filepath)
        os.makedirs(dir_name,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(filepath:str)->object:
    try:
        if not os.path.exists(filepath):
            raise CustomException("filepath is not exist in load object function",sys)
        with open(filepath,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_numpy_array(filepath:str)->np.array:
    try:
        with open(filepath,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        for name,model in models.items():
            param=params[name]
            gs=GridSearchCV(model,param,cv=3)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            
            train_model_pred=model.predict(x_train)
            test_model_pred=model.predict(x_test)
            
            train_model_score=r2_score(train_model_pred,y_train)
            test_model_score=r2_score(test_model_pred,y_test)
            
            report[name]=test_model_score
            
        return report
            
            
            
            
    except Exception as e:
        raise CustomException(e,sys)