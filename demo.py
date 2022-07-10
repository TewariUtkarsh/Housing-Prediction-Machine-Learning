from importlib import import_module
from housing.config.configuration import Configuration
from housing.exception_handler import HousingException
from housing.pipeline.pipeline import Pipeline
import sys,os
# from evidently.profile_sections.data_drift_profile_section import DataDriftProfileSection
# from evidently.profile_sections import data_drift_profile_section, DataDriftProfileSection
from housing.component.data_transformation import DataTransformation
from housing.util.util import read_yaml_file
import pandas as pd
from housing.constants import *


def main():
    try: 
        pipeline = Pipeline()
        pipeline.run_pipeline()
        # DataDriftProfileSection()

        # data_transformation_config = Configuration().get_data_transformation_config()
        # print(data_transformation_config)
        # train_path = r"C:\Users\DJ\Desktop\Current Batch Project\Housing-Prediction-Machine-Learning\housing\artifact\data_ingestion\2022-07-07-13-04-59\ingested_data\train\housing.csv"
        # schema_path = r"C:\Users\DJ\Desktop\Current Batch Project\Housing-Prediction-Machine-Learning\config\schema.yaml"
        # df = DataTransformation.load_data(train_path, schema_path)
        # print(df.dtypes)
        # schema_file_path = r"C:\Users\DJ\Desktop\Current Batch Project\Housing-Prediction-Machine-Learning\config\schema.yaml"
        # schema_info=read_yaml_file(schema_file_path)
        # base_categorical_column = schema_info[CATEGORICAL_COLUMN_KEY][0]
        # # print(base_categorical_column)
        # print(schema_info[DOMAIN_VALUE_KEY][base_categorical_column])
        # file_path=r"C:\Users\DJ\Desktop\Current Batch Project\Housing-Prediction-Machine-Learning\housing\artifact\data_ingestion\2022-07-06-12-40-15\raw_data\housing.csv"
        # df = pd.read_csv(file_path)
        # print(list(df['ocean_proximity'].unique()))

        # if list(df['ocean_proximity'].unique()).sort() == schema_info[DOMAIN_VALUE_KEY][base_categorical_column].sort():
        #     print("Yes")


        


    except Exception as e:
        raise HousingException(e, sys) from e 

if __name__=='__main__':
    main()
