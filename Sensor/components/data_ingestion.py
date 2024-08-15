from Sensor.exeption import SensorException
from Sensor.logger import logging
import os,sys
from pandas import DataFrame
from Sensor.entity.config_entity import DataIngestionConfig
from Sensor.entity.artifact_entity import DataIngestionArtifact
from Sensor.data_access.sensor_data import SensorData
from sklearn.model_selection import train_test_split

from Sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from Sensor.utils.main_utils import read_yaml_file

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig): # this is the constructor for the class DataIngestion which takes data_ingestion_config as an argument 
        try:
            logging.info(f"{'>>'*10} Data Ingestion log started. {'<<'*10} ") # this will print '>>' 10 times and '<<' 10 times, this is just for decoration
            
            self.data_ingestion_config = data_ingestion_config  # this makes the configuration available throughout the class
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH) # this will read the schema file
        
        except Exception as e:
            raise SensorException(e,sys)     # this sends any error to the main function, exeption.py        



    def export_data_into_feature_store(self) -> DataFrame: # this function will export the data into feature store
        """
        Export mongo db record as pandas dataframe and save it in feature store
        """
        try:
            logging.info("Exporting data from mongo db to feature store")
            sensor_data = SensorData()
            
            dataframe = sensor_data.export_collection_as_dataframe(collection_name=
                        self.data_ingestion_config.collection_name) # this will export the data from mongo db to pandas dataframe
            
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path # this will store the path of the feature store file
            
            # creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True) # this will create the folder if it doesn't exist

            dataframe.to_csv(feature_store_file_path,index=False,header=True) # this will save the dataframe to the feature store file
            return dataframe
        
        except Exception as e:
            raise SensorException(e,sys)
        

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Feature store dataset will be split into train and test
        """
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size = self.data_ingestion_config.train_test_split_ratio) # this will split the dataframe into train and test

            logging.info("Performed train test split on the dataframe")

            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path) # this will get the path of the training file

            os.makedirs(dir_path, exist_ok = True) # this will create the folder if it doesn't exist

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.testing_file_path, index = False,
                header = True
            )

            test_set.to_csv(
                self.data_ingestion_config.training_file_path, index = False,
                header = True
            )

            logging.info(f"Exported train and test file path.")

        except Exception as e:
            raise SensorData(e,sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact: # this will initiate the data ingestion
        try:
            dataframe = self.export_data_into_feature_store() # this will export the data into feature store
            dataframe = dataframe.drop(self._schema_config["drop_columns"],axis=1) # this will drop the columns from the dataframe
            
            self.split_data_as_train_test(dataframe=dataframe) # this will split the data into train and test
            
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path = 
                self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path) # this will return the data ingestion artifact
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}") # this will print the data ingestion artifact
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)
        

