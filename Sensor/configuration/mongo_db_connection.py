from dotenv import load_dotenv  # this is used to load .env file
import pymongo
import os
import logging
import certifi
ca = certifi.where()
from Sensor.constant.database import DATABASE_NAME
from Sensor.constant.env_variable import MONGODB_URL_KEY

load_dotenv()
class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None: 
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY) # this will get the url from .env file
                logging.info(f"{'>>'*10}Retrieved MongoDB url: {mongo_db_url}{'>>'*10}") # this will print '>>' 10 times and '<<' 10 times, this is just for decoration

                if "localhost" in mongo_db_url: # this will check if the url is localhost
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url) # this will connect to the mongo db
                else: 
                    MongoDBClient.client = pymongo.MongoClient(MONGODB_URL_KEY, tlsCAFile=ca) # this will connect to the mongo db and tlsCAFile is used to verify the certificate
            
            self.client = MongoDBClient.client # this will connect to the mongo db
            self.database = self.client[database_name] 
            self.database_name = database_name
            
        except Exception as e:
            logging.error(f"{'>>'*5}Error initializing MongoDB client: {e} {'>>'*5}")
            raise
        
