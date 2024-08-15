from distutils import dir_util
import os 
import sys

from Sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from Sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Sensor.entity.config_entity import DataValidationConfig
from Sensor.exeption import SensorException
from Sensor.logger import logging
from Sensor.utils.main_utils import read_yaml_file, write_yaml_file

from scipy.stats import ks_2samp
import pandas as pd
import json

# reading the file from yaml file
# checking the columns
# checking the data drifting
# merge them all together and initiate the data validation class

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):         
        try:
            logging.info(f"{'>>' * 10}Data Validation log started.{'<<' * 10} ")    
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH) # _schema_config is a private variable

        except Exception as e: 
            raise SensorException(e, sys) 
        
    def drop_zero_std_columns(self, dataframe): # this function will drop the columns with zero standard deviation
        pass

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool: # this function will validate the number of columns
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required numbers of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")

            if len(dataframe.columns) == number_of_columns:
                return True
            return False

        except Exception as e:
            raise SensorException(e, sys)
    
    def is_numerical_column_exist(self, dataframe: pd.DataFrame) -> bool: # this function will validate the numerical columns
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            dataframe_columns = dataframe.columns
            numerical_columns_present = True
            missing_numerical_columns = []

            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    numerical_columns_present = False
                    missing_numerical_columns.append(num_column)

            logging.info(f"Missing numerical columns: [{missing_numerical_columns}]")
            return numerical_columns_present

        except Exception as e:
            raise SensorException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame: # this function will read the data
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise SensorException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold:0.05) -> bool:
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {
                    "p_value": is_same_dist.pvalue,
                    "drift_status": is_found}})
                
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            #create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error_message = "" # this will store the error message

            # reading the data from the data ingestion artifact
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # reading the train and test file
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validating the number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all columns.\n"

            # validating the numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message}Train dataframe does not contain all numerical columns.\n"
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message}Test dataframe does not contain all numerical columns.\n"

            if len(error_message) > 0:
                raise Exception(error_message)

            # validating the dataset drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path=self.data_ingestion_artifact.training_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path= None,
                invalid_test_file_path= None,
                drift_report_file_path= self.data_validation_config.
                drift_report_file_path,
                )

            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)