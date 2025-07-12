import yaml
from networksecurity.exception.exception import CustomException
import os,sys
import numpy as np
import dill
import pickle


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