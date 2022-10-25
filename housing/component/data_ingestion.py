from housing.entity.config_entity import DataIngestionConfig
from housing.logger import logging
from housing.exception_handler import HousingException
from housing.entity.artifact_entity import DataIngestionArtifact
import os, sys

# used for zip files extraction
import tarfile

# to download files
from six.moves import urllib
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit



class DataIngestion:

    def __init__(self, data_ingestion_config:DataIngestionConfig) -> None:
        try:
            logging.info(f"{'='*20}Data Ingestion Log started.{'='*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise HousingException(e, sys) from e



    def download_housing_data(self) -> str:
        try:
            
            # Extracting download url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url
            
            # Folder location to download data
            tgz_download_dir = self.data_ingestion_config.tgz_download_dir

            # Checking and creating the directory
            if os.path.exists(tgz_download_dir):
                os.remove(tgz_download_dir)

            os.makedirs(tgz_download_dir, exist_ok=True)

            # To extract only the filename from given dir/link
            housing_file_name = os.path.basename(download_url)

            # File to specify where to download the tgz file 
            tgz_file_path = os.path.join(
                tgz_download_dir,
                housing_file_name
            )

            logging.info(f"Downloading File from: [{download_url}] into: [{tgz_file_path}]")

            # Code to download the file 
            urllib.request.urlretrieve(download_url, tgz_file_path)

            logging.info(f"File: [{tgz_file_path}] Downloaded Successfully!!")

            return tgz_file_path

        except Exception as e:
            # from e means, the line number displayed will be from the point where exception was generated
            raise HousingException(e,sys) from e


    def extract_tgz_file(self, tgz_file_path:str):
        try:
            # Dir where we extract our downloaded tgz file
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            # Checking and creating the directory
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)

            logging.info(f"Extracting tgz file: [{tgz_file_path}] into dir: [{raw_data_dir}]")
            
            # Reading and extracting the downloaded tgz to raw data dir
            with tarfile.open(tgz_file_path) as housing_tgz_file_object:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(housing_tgz_file_object, raw_data_dir)
            

            logging.info(f"Extraction completed!!")
            pass
        
        except Exception as e:
            raise HousingException(e,sys) from e



    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            file_name = os.listdir(raw_data_dir)[0]

            housing_file_path = os.path.join(
                raw_data_dir,
                file_name
            )

            logging.info(f"Reading csv file: [{housing_file_path}]")

            housing_data_frame = pd.read_csv(housing_file_path)

            housing_data_frame['income_cat'] =  pd.cut(
                housing_data_frame["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )

            logging.info("Splitting Data into Train Test")

            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.20, random_state=42)

            for train_index, test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
                strat_train_set = housing_data_frame.loc[train_index].drop(['income_cat'], axis=1)
                strat_test_set = housing_data_frame.loc[test_index].drop(['income_cat'], axis=1)

            train_file_path = os.path.join(
                self.data_ingestion_config.ingested_train_dir,
                file_name
            )

            test_file_path = os.path.join(
                self.data_ingestion_config.ingested_test_dir,
                file_name
            )


            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to csv: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to csv: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)


            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path,
                test_file_path,
                is_ingested=True,
                message=f"Data Ingestion Completed successfully"
            )

            logging.info(f"Data ingestion artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e




    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_housing_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)

            # Returns the Artifact only, implemented inside the function
            return self.split_data_as_train_test()


        except Exception as e:
            raise HousingException(e,sys) from e


    
    def __del__(self):

        """
        Whenever this object is about to destruct then we can log the completoin log
        """
        logging.info(f"{'='*20}Data Ingestion Log Completed.{'='*20} \n\n")





        