from Sensor.exeption import SensorException
import os
import sys

from Sensor.logger import logging

def test_exception():
    try:
        logging.info("ki yanha p bhaiyaa ek error ayegi dividion by zero wali error ")
        a = 1/0
    except Exception as e:
        raise SensorException(e,sys)


# we use the below commands to not run the exception values given earlier
# whatever values we give here that will only run
# if __name__ == "__main__"  this is called module execution control/ prevent execution control
# wanha ke variable yanha na aajee isleye use karte hain    
if __name__ == "__main__":
    try:
        test_exception()
    except Exception as e:
        print(e)