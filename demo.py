from housing.exception_handler import HousingException
from housing.pipeline.pipeline import Pipeline
import sys,os
from evidently.profile_sections.data_drift_profile_section import DataDriftProfileSection
from evidently.profile_sections import data_drift_profile_section, DataDriftProfileSection
def main():
    try: 
        pipeline = Pipeline()
        pipeline.run_pipeline()
        # DataDriftProfileSection()
    except Exception as e:
        raise HousingException(e, sys) from e 

if __name__=='__main__':
    main()
