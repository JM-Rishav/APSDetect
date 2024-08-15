from datetime import datetime
import os
from Sensor.constant import training_pipeline

class TrainingPipelineConfig:
    # store APSDetect.csv with timestamp
    def __init__(self,timestamp=datetime.now()):

        timestamp = timestamp.strftime("%m_%d_%y_%H_%M_%S")
        self.pipeline_name: str = training_pipeline.PIPELINE_NAME
        self.artifact_dir: str = os.path.join(training_pipeline.ARTIFACT_NAME,timestamp)
        self.timestamp: str = timestamp

    

class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME 
        )       
                # This command constructs a file path by joining multiple path components and assigns it to an instance variable.
                # training_pipeline.DATA_INGESTION_DIR_NAME a constant or variable that holds the name of the directory where data ingestion artifacts should be stored.
                # training_pipeline.artifact_dir a directory path where artifacts (such as logs, models, or temporary files) related to the training pipeline are stored.
                # The resulting file path will be like D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion

        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir,training_pipeline.
            DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )       
                # output of above will be like
                #self.data_ingestion_dir = os.path.join(
                #     "D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion", 
                #     "feature_store", 
                #     "APSDetect.csv"
                # )
                # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion/feature_store/APSDetect.csv

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.
            DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
                # output of above will be like
                # self.training_file_path = os.path.join(
                #     "D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion", 
                #     "ingested", 
                #     "train.csv"
                # )
                # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion/ingested/train.csv

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.
            DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
                # output of above will be like
                # self.testing_file_path = os.path.join(
                #     "D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion",
                #     "ingested",
                #     "test.csv"   
                #)
                # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_ingestion/ingested/test.csv

        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME



class DataValidationConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        
        self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir
            , training_pipeline.DATA_VALIDATION_DIR_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation

        self.valid_data_dir: str = os.path.join(self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_VALID_DIR)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/validated
        
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_INVALID_DIR)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/invalid

        self.valid_train_file_path: str = os.path.join(self.valid_train_file_path,
            training_pipeline.TRAIN_FILE_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/validated/train.csv

        self.valid_test_file_path: str = os.path.join(self.valid_test_file_path,
            training_pipeline.TEST_FILE_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/validated/test.csv

        self.invalid_train_file_path: str = os.path.join(self.invalid_train_file_path,
            training_pipeline.TRAIN_FILE_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/invalid/train.csv

        self.invalid_test_file_path: str = os.path.join(self.invalid_test_file_path,
            training_pipeline.TEST_FILE_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/invalid/test.csv

        self.drift_report_file_path: str = os.path.join(self.data_validation_dir ,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)
        # output of the above will be like
        # D:/Essentials/Project/APSDetect/APSDetect/artifacts/data_validation/drift_report/report.yaml

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):


        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME )
        
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"),)
        
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            training_pipeline.TEST_FILE_NAME.replace("csv", "npy"), )
        
        
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            training_pipeline.PREPROCSSING_OBJECT_FILE_NAME,)

   

class ModelTrainerConfig:


    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )


        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, 
            training_pipeline.MODEL_FILE_NAME
        )



        self.expected_accuracy: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD



class ModelEvaluationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_EVALUATION_DIR_NAME
        )

        self.report_file_path = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)

        
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE





class ModelPusherConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):

        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_PUSHER_DIR_NAME
        )

        self.model_file_path = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_FILE_NAME)
        
        timestamp = round(datetime.now().timestamp())

        self.saved_model_path=os.path.join(
            training_pipeline.SAVED_MODEL_DIR,
            f"{timestamp}",
            training_pipeline.MODEL_FILE_NAME)