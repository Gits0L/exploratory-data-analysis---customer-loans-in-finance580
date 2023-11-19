#%%
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials 
        self.engine = self.create_engine()
    #PROBLEM WITH STRING LITERAL EU-WEST1 AND INDENTATION IN NEXT CODE
    def _create_engine(self):
        engine = create_engine(f"postgresql+psycopg2://{loansanalyst}:{EDAloananalyst}@{eda-projects.cq2e8zno855e.eu-west-1.rds.amazonaws.com}:{5432}/{payments}")
        return engine
    
    def initialise_engine(self):
        self.engine = self.create_engine()

    def data_extraction(self, table_name='loan_payments'):
        query = f"SELECT * FROM loan_payments;"
        data = pd.read_sql(query, self.engine)
        return data
    
    def save_to_file(self, data, file_path='loan_payments_data.csv'):
        data.to.csv(file_path, index=FALSE)

    def load_loan_date(file_path='loan_payments_data.csv'):
        try:
            data = pd.read_csv(file_path)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None

# %%
