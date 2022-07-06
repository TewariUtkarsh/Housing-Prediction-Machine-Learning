from housing.entity.config_entity import DataIngestionConfig
from housing.logger import logging
from housing.exception_handler import HousingException
from housing.entity.artifact_entity import DataIngestionArtifact
import os, sys

# used for zip files extraction
import tarfile

#
from six.moves


class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'='*20}Data Ingestion Log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e, sys) from e



    def download_housing_data(self, ):
        pass


    def extract_tgz_file(self):
        pass


    def split_data_as_train_test(self):
        pass


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:

            pass

        except Exception as e:
            raise HousingException(e,sys) from e