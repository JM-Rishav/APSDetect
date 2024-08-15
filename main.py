from Sensor.exeption import SensorException
import os
import sys

from Sensor.logger import logging
from Sensor.utils2 import dump_csv_file_to_mongodb_collection

from Sensor.configuration.mongo_db_connection import MongoDBClient

#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig

from Sensor.pipeline.training_pipeline import TrainPipeline


# def test_exception():
#     try:
#         logging.info("ki yanha p bhaiyaa ek error ayegi dividion by zero wali error ")
#         a = 1/0
#     except Exception as e:
#         raise SensorException(e,sys)
# we use the below commands to not run the exception values given earlier
# whatever values we give here that will only run
# if __name__ == "__main__"  this is called module execution control/ prevent execution control
# wanha ke variable yanha na aajee isleye use karte hain   
from Sensor.configuration.mongo_db_connection import MongoDBClient
from Sensor.exeption import SensorException
import os , sys
from Sensor.logger import logging


from Sensor.pipeline.training_pipeline import TrainPipeline
from Sensor.utils.main_utils import load_object
from Sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from Sensor.configuration.mongo_db_connection import MongoDBClient
from Sensor.exeption import SensorException
import os,sys
from Sensor.logger import logging
from Sensor.pipeline import training_pipeline
from Sensor.pipeline.training_pipeline import TrainPipeline
import os
from Sensor.utils.main_utils import read_yaml_file
from Sensor.constant.training_pipeline import SAVED_MODEL_DIR


from fastapi import FastAPI
from Sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from Sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from Sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, File, UploadFile, Response
import pandas as pd


app = FastAPI()



origins = ["*"]
#Cross-Origin Resource Sharing (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=["authentication"])
async def  index():
    return RedirectResponse(url="/docs")





@app.get("/train")
async def train():
    try:

        training_pipeline = TrainPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
        




@app.get("/predict")
async def predict():
    try:

    # get data and from the csv file 
    # covert it into dataframe 

        df =None

        Model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not Model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = Model_resolver.get_best_model_path()
        model= load_object(file_path=best_model_path)
        y_pred=model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping,inplace=True)


        # get the prediction output as you wnat 


    except  Exception as e:
        raise  SensorException(e,sys)





def main():
    try:
            
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)



if __name__ == "__main__":

    # file_path="/Users/myhome/Downloads/sensorlive/aps_failure_training_set1.csv"
    # database_name="ineuron"
    # collection_name ="sensor"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)
    app_run(app ,host=APP_HOST,port=APP_PORT)







  












    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)