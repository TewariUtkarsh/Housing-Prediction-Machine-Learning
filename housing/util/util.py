# To access the yaml files
import yaml
from housing.exception_handler import HousingException
import os, sys


def read_yaml_file(file_path:str) -> dict:
    """ 
    Reads a yaml file and returns the content of the file
    as a dictionary
    
    file_path:str
        File path to the yaml file
    """

    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise HousingException(e, sys) from e

        