# Automated Weather Data ETL Pipeline on AWS
the main focus of the project, which is to extract and process weather data efficiently using automation and AWS cloud resources.
Welcome to the "WeatherWise" Data Engineering Project!

# Project Overview:
The "WeatherWise" project is an exciting data engineering endeavor where I design and implement an end-to-end ETL (Extract, Transform, Load) pipeline to fetch real-time weather data from the Open Weather Map API. The project's primary objective is to automate the entire process using Apache Airflow, a powerful open-source platform for orchestrating and scheduling tasks and data pipelines. All aspects of the project will be executed on the robust and reliable AWS cloud platform.

# Key Objectives:

## Data Extraction
We will employ the Open Weather Map API to extract up-to-date weather data, encompassing essential weather metrics such as temperature, humidity, wind speed, and more.

## Data Transformation
The extracted raw weather data will undergo comprehensive transformation processes. These transformations will include data cleaning, normalization, and any necessary adjustments to make the data suitable for storage and downstream analytics.

## Data Loading
The transformed weather data will be efficiently loaded into an S3 bucket, leveraging AWS's scalable storage solution. This ensures that the processed data is securely stored and readily available for further analysis and insights.

## Automation with Apache Airflow
A key highlight of the "WeatherWise" project is the implementation of Apache Airflow to automate the entire ETL workflow. By orchestrating tasks and scheduling pipelines, we will achieve a seamless and reliable data flow.



#
Through "WeatherWise," we will not only demonstrate our expertise in data engineering and AWS cloud services but also develop a valuable data pipeline for accessing real-time weather information. This project will serve as a testament to our ability to handle complex data workflows and showcase our proficiency in deploying cutting-edge technologies to solve real-world challenges. Let's embark on this data-driven journey and unlock the power of weather data!

# installing required dependencies on EC2 machine
```bash
# update all packages in ec2 instance
sudo apt update
 # install python
sudo apt install python3-pip

# install python virtual environment
sudo apt install python3.10-venv

# create a python virual environment
python3 -m venv airflow_venv

# activate python virual environment
source airflow_venv/bin/activate

# install pandas
sudo pip install pandas

# install S3 filesystem
sudo pip install s3fs

# install S3 airflow
sudo pip install apache-airflow

# launch airflow service
airflow standalone

# install aws cli
sudo apt  install awscli

# use the below command to configure and set credentials
aws configure

# get session token
aws sts get-session-token
```
