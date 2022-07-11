from collections import namedtuple

DataIngestionArtifact = namedtuple("DataIngestionArtifact",
["train_flie_path", "test_file_path", "is_ingested", "message"])


DataValidationArtifact = namedtuple("DataValidationArtifact",
["schema_file_path", "report_file_path", "report_page_file_path", "is_validated", "message"])


DataTransformationArtifact = namedtuple("DataTransformationArtifact",
["is_tranformed", "message", "transformed_train_file_path", "transformed_test_file_path", "preprocessed_object_file_path"])


ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",
["is_trained", "message", "trained_model_file_path",
"train_rmse", "test_rmse", "train_accuracy", "test_accuracy", "model_accuracy"])


ModelEvalutaionArtifact = namedtuple("ModelEvalutaionArtifact",
["is_model_accepted", "evaluated_model_path"])


ModelPusherArtifact = namedtuple("ModelPusherArtifact",
["is_model_pusher", "export_model_file_path"])