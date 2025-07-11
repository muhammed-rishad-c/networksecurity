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