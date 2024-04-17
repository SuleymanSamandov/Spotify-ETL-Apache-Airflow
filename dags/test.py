import requests
from datetime import datetime,timedelta
import time
import datetime
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import datetime


TOKEN=' BQBVJFUpwA2uSiM0i1GKrl3l8JyLBMCnNdJ9lAUiCGRvQBoIhCq7msEyRsF_hLqxw1ZIkQiaR5PuOXKSDonBiWQYkK1NmFs7pKBNw8vk5r9Q25E2V9L_IGL9CDbmmA2bhmcR0tZ1oF6_RKAccpT6KK726lIuZ1TdqEzsih6KQnDs9rah6aT7vF7S0XttjtK4-dtnQpIwv-NVVIAWXNF3K9f8IzOLtbWXytxszKfRAG1ynv8hDMX0R1R4xDTJq3WNtsGT1wm0grMIsRLawx3I1_pnV9TgpFUAhr--Q5qcAwwmPwAArnQOi_GmGWBWUhTGXWhHMSxfSN-nBCDt'

def connection():
    data=None
    # HTTP request headers
    input_params = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=7)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    try:
        r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers=input_params)
        if r.status_code == 200:
            print("Connection successful")
            data = r.json()
        else:
            for i in range(2):
                time.sleep(3)
                r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers=input_params)
                if r.status_code == 200:
                    print("Connection successful")
                    data = r.json()
                    break
                else:
                    print("There was a problem with the connection. Trial number {number}, Status Code: {code}".format(number=i + 1, code=r.status_code))
    except Exception as e:
        print("Error:", e)
    
    return data