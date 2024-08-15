import sys
from typing import Optional

import numpy as np
import pandas as pd
import json
from Sensor.configuration.mongo_db_connection import MongoDBClient
from Sensor.constant.database import DATABASE_NAME
from Sensor.exeption import SensorException
from pymongo import MongoClient
from Sensor.constant.env_variable import MONGODB_URL_KEY
from Sensor.logger import logging


class SensorData:
    """
    This class hwlp to export entire mongo db recored as pandas dataframe.
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            mongodb_uri = MONGODB_URL_KEY
            client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            db = client.get_database('APSDetect')
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            raise SensorException(e, sys)   



    def save_csv_file(self, file_path, collection_name: str, database_name: Optional[str] = None): 
        # this will save the csv file to mongo db
        try:
            data_frame = pd.read_csv(file_path) # this will read the csv file
            data_frame.reset_index(drop=True, inplace=True) # this will reset the index
            records = list(json.loads(data_frame.T.to_json()).values()) # this will convert the dataframe to json
            if database_name is None: # this will check if the database name is None
                collection = self.mongo_client.database[collection_name] # this will create a connection to the mongo db
            else:
                collection = self.mongo_client[database_name][collection_name] # it will just connect to the db
            collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise SensorException(e, sys)



    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            """
            export entire collection as dataframe
            return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find())) # this will convert the collection to pandas dataframe

            if "_id" in df.columns.to_list(): # this will check if _id is in the dataframe
                df = df.drop(columns=["_id"], axis=1) # this will drop the _id column

            df.replace({"na": np.nan}, inplace=True) # this will replace na with nan

            return df

        except Exception as e:
            raise SensorException(e, sys)



