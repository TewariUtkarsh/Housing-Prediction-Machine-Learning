from housing.exception_handler import HousingException
from housing.pipeline.pipeline import Pipeline
import sys,os

def main():
    try: 
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise HousingException(e, sys) from e 

if __name__=='__main__':
    main()
