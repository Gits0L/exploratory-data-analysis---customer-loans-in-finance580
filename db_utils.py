#%%
import yaml
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sqlalchemy

#Figure yout how to add docustring proprly
#" " 
Initalises yaml file as parametere 

Defines: 
function1 creates the engine using the credentials in the yaml file 
function2 initalises the engine using the _create_engine method
function3 extracts the data from the loan database 
unction4 saves the loan data within the loan database as a csv file 
#function5 loads the loan data from the cvs file from function 4 into a Pandas Dataframe 
#find name for error handling thing 
#" " 
RDS_HOST: eda-projects.cq2e8zno855e.eu-west-1.rds.amazonaws.com
RDS_PASSWORD: EDAloananalyst
RDS_USER: loansanalyst
RDS_DATABASE: payments
RDS_PORT: 5432
import yaml


with open('credentials.yaml', 'r') as f:
    credentials = yaml.safe_load(f)

class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials

    #PROBLEM WITH STRING LITERAL EU-WEST1 AND INDENTATION IN NEXT CODE
    def _create_engine(self):
        engine = create_engine(f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}")
        connection = engine.connect
    
    def initialise_engine(self):
        self.engine = self._create_engine()

    def data_extraction(self, table_name='loan_payments'):
        query = f"SELECT * FROM loan_payments;"
        data = pd.read_sql(query, self.engine)
        return data
    
    def save_to_file(self, data, file_path='loan_payments_data.csv'):
        data.to.csv(file_path, index=FALSE)

    def load_loan_data(file_path='loan_payments_data.csv'):
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
data_from_yaml = RDSDatabaseConnector()
data_from_yaml._create_engine()
# %%
