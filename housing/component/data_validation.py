from housing.logger import logging
from housing.exception_handler import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from housing.util.util import read_yaml_file
from housing.constants import *
import os, sys


from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import pandas as pd
import json
import yaml

from housing.util.util import read_yaml_file


class DataValidation:
    
    def __init__(self, data_validation_config:DataValidationConfig,
                data_ingestion_artifact:DataIngestionArtifact):
        
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise HousingException(e, sys) from e


    
    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_flie_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df, test_df

        except Exception as e:
            raise HousingException(e, sys) from e




    def is_train_test_file_exists(self) -> bool:
        try:
            logging.info("Checking if training and testing files are available")

            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_flie_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available = is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists? -> [{is_available}]")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_flie_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Training File: [{training_file}] or Testing File: [{testing_file}] not present"
                logging.info(message)
                raise Exception(message)

            return is_available

        except Exception as e:
            raise HousingException(e, sys) from e




    def validate_dataset_schema(self) -> bool:
        try:

            train_df, test_df = self.get_train_and_test_df()

            validation_status = False

            schema_file_info = read_yaml_file(self.data_validation_config.schema_file_path)

            base_column_names = list(schema_file_info[DATASET_SCHEMA_COLUMNS_KEY].keys())
            base_number_of_columns = len(base_column_names)

            train_df_columns = list(train_df.columns)
            train_df_number_of_columns = len(train_df_columns)

            test_df_columns = list(test_df.columns)
            test_df_number_of_columns = len(test_df_columns)

            base_categorical_column = schema_file_info[CATEGORICAL_COLUMN_KEY][0]
            # base_target_column = schema_file_info[TARGET_COLUMN_KEY]
            base_domain_values = schema_file_info[DOMAIN_VALUE_KEY][base_categorical_column].sort()



            train_df_domain_values = list(train_df[base_categorical_column].unique()).sort()
            test_df_domain_values = list(test_df[base_categorical_column].unique()).sort()

            if train_df_number_of_columns == base_number_of_columns:
                if train_df_columns == base_column_names:
                    if train_df_domain_values == base_domain_values:
                        validation_status = True
                    else:
                        raise Exception(f"Domain Values not matched for training file:[{self.data_ingestion_artifact.train_flie_path}]")
                else:
                    raise Exception(f"Column names not matched for training file:[{self.data_ingestion_artifact.train_flie_path}]")
            else:
                raise Exception(f"Number of Columns not matched for training file:[{self.data_ingestion_artifact.train_flie_path}]")

            
            if test_df_number_of_columns == base_number_of_columns:
                if test_df_columns == base_column_names:
                    if test_df_domain_values == base_domain_values:
                        validation_status = True
                    else:
                        validation_status = False
                        raise Exception(f"Domain Values not matched for training file:[{self.data_ingestion_artifact.test_flie_path}]")
                else:
                    validation_status = False
                    raise Exception(f"Column names not matched for training file:[{self.data_ingestion_artifact.test_flie_path}]")
            else:
                validation_status = False
                raise Exception(f"Number of Columns not matched for training file:[{self.data_ingestion_artifact.test_flie_path}]")

            # categorical_column

            # Task:
            # 1. col num
            # 2. col name
            # 3. domain value

            """
            Approach:
            1. read schema file path as yaml dict
            2. acquire and for train and test df, equate the number and name columns, 
            3. if same then fine

            1. for domain value access throgh schema and for the file df[ocean_value].unique() / set(df[ocean_value])
            2. then map

            Define Constants for schema.yaml:
            1. to access key value for schema.yaml
            2. 
            """

            # self.data_ingestion_artifact.
            # self.data_validation_config.schema_file_path
            



            return validation_status

        except Exception as e:
            raise HousingException(e, sys) from e




    def get_and_save_data_drift_report(self):
        """
        we will get the data_drift value: true/false from
        json file(dict) generated in order to display result
        and proceed further
        """
        
        try:
            # Specifying/Creating a profile for finding Data Drift
            profile = Profile(sections=[DataDriftProfileSection()])
            
            train_df, test_df = self.get_train_and_test_df()

            # To calculate reference and current data drift
            profile.calculate(train_df, test_df)

            # returns string format of json file for our profile: profile.json()

            # to load our json file as dict as output
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path

            # Creating the artifact directory for Data Validation
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)

            return report

        except Exception as e:
            raise HousingException(e, sys) from e




    def save_data_drift_report_page(self):
        try:
            
            dashboard = Dashboard(tabs=[DataDriftTab()])

            train_df, test_df = self.get_train_and_test_df()


            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_dir, exist_ok=True)
            

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e, sys) from e




    def is_data_drift_found(self) -> bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()

            
            return True

        except Exception as e:
            raise HousingException(e, sys) from e




    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                self.data_validation_config.schema_file_path,
                self.data_validation_config.report_file_path,
                self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation Performed Successfully."
            )

            logging.info(f"Data Validation Artiface: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys)

