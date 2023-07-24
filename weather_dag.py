from datetime import timedelta, datetime
import pandas as pd
import json
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator



# convert temperature from kelvin to fahrenheit
def kelvin_to_fahrenheit(temp_in_kelvin):
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9/5) + 32
    return temp_in_fahrenheit


# transform data into dataframe 
def transform_load_data(task_instance):
        data = task_instance.xcom_pull(task_ids='extract_weather_data')
        city = data['name']
        weather_desc = data["weather"][0]['description']
        temp_f = kelvin_to_fahrenheit(data["main"]["temp"])
        feels_like = kelvin_to_fahrenheit(data["main"]["feels_like"])
        temp_min = kelvin_to_fahrenheit(data["main"]["temp_min"])
        temp_max = kelvin_to_fahrenheit(data["main"]["temp_max"])
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        record = datetime.utcfromtimestamp(data['dt']+data['timezone'])
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])
        
        # extracted data to a dictonary
        new_data = {
               'city': city,
               'temperature (F)' : temp_f,
                'desc' : weather_desc,
                'feels like' : feels_like,
                'temp minimum' : temp_min,
                'temp max' : temp_max,
                'pressure' : pressure,
                'humidity' : humidity,
                'wind speed' : wind_speed,
                'record time' : record,
                'sunrise' : sunrise,
                'sunset' : sunset
        }

        transformed_data = [new_data]

        df = pd.DataFrame(transformed_data) # data to a dataframe

        dt = datetime.now().strftime("%d%m%Y%H%M%S")
        filename = 'current_weather_data_boston_' + dt # setting the file name with current date and time

        aws_creds = {
                "key" : 'XXXXXXXXXXXXXXXXXXX',
                'secret' : 'XXXXXXXXXXXXXXXXXXX',
                'token' : "XXXXXXXXXXXXXXXXXXX"
        }
        df.to_csv(f"s3://weatherairflowbucket/{filename}.csv", index = False, storage_options = aws_creds) # load csv to S3 bucket

        
# default rgs
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023,1,8),
    'email': ['youremail@email.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}


with DAG('weather_dag',
         default_args = default_args,
         schedule_interval = '@daily',
         is_paused_upon_creation=True,
         catchup = False
         ) as dag:

        # TASK 1 - connect to api
        is_weather_api_ready = HttpSensor(
        task_id = 'is_weather_api_ready',
        http_conn_id = 'weather_api',
        endpoint = '/data/2.5/weather?q=Boston&appid=XXXXXXXXXXXXXXXXX'
        )

        # TASK 2 - extract data from api
        extract_weather_data = SimpleHttpOperator(
                task_id = 'extract_weather_data',
                http_conn_id = 'weather_api',
                endpoint = '/data/2.5/weather?q=Boston&appid=XXXXXXXXXXXXXXXXX',
                method = 'GET',
                response_filter = lambda r: json.loads(r.text),
                log_response = True
        )
        # TASK 3 - Transform and load data to S3 bucket
        transform_and_load_data = PythonOperator(
                task_id = 'transform_load_data',
                python_callable = transform_load_data
        )


        # set sequnce of the flow for airflow
        is_weather_api_ready >> extract_weather_data >> transform_and_load_data