from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact",
["train_flie_path", "test_file_path", "is_ingested", "message"])


DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path", "report_file_path", "report_page_file_path", "is_validated", "message"])


DataTransformationArtifact = namedtuple("DataTransformationArtifact",
[])


ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",
[])


ModelEvalutaionArtifact = namedtuple("ModelEvalutaionArtifact",
[])


ModelPusherArtifact = namedtuple("ModelPusherArtifact",
[])