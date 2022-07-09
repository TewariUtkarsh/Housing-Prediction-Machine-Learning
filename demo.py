from housing.config.configuration import Configuration
from housing.exception_handler import HousingException
from housing.pipeline.pipeline import Pipeline
import sys,os
from evidently.profile_sections.data_drift_profile_section import DataDriftProfileSection
from evidently.profile_sections import data_drift_profile_section, DataDriftProfileSection
from housing.component.data_transformation import DataTransformation


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

    except Exception as e:
        raise HousingException(e, sys) from e 

if __name__=='__main__':
    main()
