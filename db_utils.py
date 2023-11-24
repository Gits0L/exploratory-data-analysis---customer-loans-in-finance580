#%%
import yaml
#%%
import pandas as pd
#%%
import psycopg2
#%%
from sqlalchemy import create_engine
#%%
import sqlalchemy
#%%
with open('credentials.yaml', 'r') as f:
    credentials = yaml.safe_load(f)
#%%
class RDSDatabaseConnector:
    def __init__(self, credentials):
        self.credentials = credentials

    #PROBLEM WITH STRING LITERAL EU-WEST1 AND INDENTATION IN NEXT CODE
    def _create_engine(self):
        engine = create_engine(f"postgresql+psycopg2://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}")
        return engine
    
    def initialise_engine(self):
        self.engine = self._create_engine()

    def data_extraction(self, table_name='loan_payments'):
        query = f"SELECT * FROM loan_payments;"
        data = pd.read_sql(query, self.engine)
        return data
    
    def save_to_file(self, data, file_path='loan_payments_data.csv'):
        data.to_csv(file_path, index=False)

    def load_loan_data(self, file_path='loan_payments_data.csv'):
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
#%%
loan_data = RDSDatabaseConnector(credentials)
loan_data._create_engine()
loan_data.initialise_engine()
loan_data.data_extraction()
loan_data.data_extraction('loan_payments')
loan_data.save_to_file(data=loan_data.data_extraction('loan_payments'), file_path='loan_payments_data.csv')
loaded_data = loan_data.load_loan_data('loan_payments_data.csv')
print(loaded_data) 

loans_df = pd.read_csv('loan_payments_data.csv')
loans_df.head(10)
loans_
# %%
