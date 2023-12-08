import matplotlib.pyplot as plt


import yaml


import pandas as pd


import psycopg2


from sqlalchemy import create_engine


import sqlalchemy

"""
Loads in yaml file including the credentials to create and connect to databse

"""
with open('credentials.yaml', 'r') as f:
    credentials = yaml.safe_load(f)

class RDSDatabaseConnector:
    """"
    Class connects to yaml file with credentials to create and initialise engine, then extracts the data from the database and saves to a new file so it ready to use.

    Attributes:
    - Credentials: The name of the yaml file containing the database credentials
     
    Methods:
    - __init__(self, credentials): Initialises an instance of the class 
    - _create_engine(self): Establishes a connection to the database
    - initialise_engine(self): Initialises the connection to the database
    - save_to_file(self, data, file_path='loan_payments_data.csv'): Saves the database to a csv file under the name loan_payments_data
    - load_loan_data(self, file_path='loan_payments_data.csv'): Loads the data inside the newly initialised database including FileNotFound error if file path is not located 

    """

    def __init__(self, credentials):
        self.credentials = credentials

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

loan_data = RDSDatabaseConnector(credentials)
loan_data._create_engine()
loan_data.initialise_engine()
loan_data.data_extraction()
loan_data.data_extraction('loan_payments')
loan_data.save_to_file(data=loan_data.data_extraction('loan_payments'), file_path='loan_payments_data.csv')
loaded_data = loan_data.load_loan_data('loan_payments_data.csv')
loans_df = pd.read_csv('loan_payments_data.csv', index_col='id')
loans_df.tail(10).describe()
loans_df['recoveries']

"""
Removes months from term collumn and strings years and year form the eomployment_length collumn 

"""
loans_df['term'] = loans_df['term'].str.replace('months', '', regex=True)
loans_df['employment_length'] = loans_df['employment_length'].str.replace('years', '', regex=True)
loans_df['employment_length'] = loans_df['employment_length'].str.replace('year', '', regex=True)
loans_df.info()

"""
Extracts collumns that include null values
"""
null_data = loans_df.isnull()
null_columns = loans_df.columns[loans_df.isnull().any()]
numeric_null_columns = loans_df[null_columns].select_dtypes(include=['number']).columns
print(numeric_null_columns)

"""
Creates a histogram of collumns with null values to measure the spread of the data
"""
loans_df['funded_amount'].hist(bins=40)
loans_df['funded_amount'].hist(bins=40)
loans_df['term'].hist(bins=40)
loans_df['int_rate'].hist(bins=40)

class DataFrameTransform:
    """"
    Class to transform the data so it can be used analysed with more precision 

    Attributes:
    - loans_df: Dataset from csv filed which includes loan_information

    Methods: 
    - indetify_skewed_columns: Uses a lambda expression on the dataframe to identify columns where the level of skewdness is significant (more than 0.5)
    - visualise_skewdness: Visualises skewdness for each collumn using the mat plot library 
    - transform_columns: Transforms columns where type is an integer 
    - null_impute: Imputes the null values in each column with the median if the value is a float point number and the mode value if not a float point number 
    - save_transformed_data: Saves transormed data to a new file
     - outlier_removal: Removes outliers that do not fit in with the spread of the overall data from each column 
    """


    def __init__(self, loans_df):
        self.loans_df = loans_df
    
    def identify_skewed_columns(self, threshold=0.5):
        skewed_columns = self.loans_df.apply(lambda x: abs(x.skew()) > threshold)
        return skewed_columns[skewed_columns].index.tolist()

    def visualize_skewness(self, columns, plotter):
        for column in columns:
            plotter.plot_distribution(self.loans_df, column)

    def transform_columns(self, columns, transformation):
        for column in columns:
            if pd.api.types.is_numeric_dtype(self.loans_df[column]):
                self.loans_df[column] = transformation(self.loans_df[column])
            else:
                pass
    
    def null_impute(self, loans_df):
        for column in loans_df.columns:
            if pd.api.types.is_numeric_dtype(self.loans_df[column]) and loans_df[column].isnull().any() and loans_df[column].dtype == 'float64':
                loans_df[column].fillna(loans_df[column].median(), inplace=True)
            else:
                loans_df[column].fillna(loans_df[column].mode()[0], inplace=True)
        return loans_df
    
    def outlier_removal(self, column):
        Q1 = column.quantile(0.25)
        Q3 = column.quantile(0.75)
        IQR = Q3 - Q1 # Calculates the IQR (Interquartile Range)
        lower_bound = Q1 - 1.5 * IQR # Defines the lower and upper bounds to identify outliers
        upper_bound = Q3 + 1.5 * IQR
        return column[(column >= lower_bound) & (column <= upper_bound)] #Filters the DataFrame to exclude outliers
    
    def save_transformed_data(self, filename='transformed_data.csv'):
        self.loans_df.to_csv(filename, index=False)

transform = DataFrameTransform(loans_df)
threshold_skewness = 0.5 
skewed_columns = transform.identify_skewed_columns(threshold_skewness)
transform.save_transformed_data('transformed_data.csv', index=False)



from matplotlib import pyplot
import seaborn as sns
from scipy.stats import normaltest
class Plotter:
    """"
    Class plots data using various visualisation methods

    Attributes: 
    - loans_df: Dataset containing loan information 

    Methods: 
    - null_percent_funded: Checks the percentage of null values in the funded amount collumn against total values
    - null_percent_term: Checks the percentage of null values in the term collumn against total values
    - null_percent_int_rate: Checks the percentage of null value in the interest rate collumn against total values
    - skew check: Visualises the skew of each collumn that does not contain numerical values 
    """
    def __init__(self, loans_df):
        self.loans_df = loans_df
    
    def plot_distribution(self, data, column):
        pass
    
    def null_percent_funded(self):
        return loans_df['funded_amount'].isnull().sum() * 100/len(loans_df['funded_amount'])
        loans_df['funded_amount'].hist(bins=40)
    
    def null_percent_term(self):
        return loans_df['term'].isnull().sum() * 100/len(loans_df['term'])
    
    def null_percent_int_rate(self):
        return loans_df['int_rate'].isnull().sum() * 100/len(loans_df['int_rate'])
        
    def skew_check(self):
        numeric_data = ['loan_amount',
                    'funded_amount', 
                    'funded_amount_inv',
                    'instalment',
                    'annual_inc',
                    'open_accounts',
                    'out_prncp',
                    'out_prncp_inv',
                    'total_payment',
                    'total_payment_inv',
                    'total_rec_prncp',
                    'total_rec_int'
                    ]

        categorical_data = [col for col in loans_df.columns if col not in numeric_data]
        sns.set(font_scale=0.7)
        f = pd.melt(loans_df, value_vars=numeric_data)
        g = sns.FacetGrid(f, col="variable",  col_wrap=3, sharex=False, sharey=False)
        g = g.map(sns.histplot, "value", kde=True)
        print(categorical_data)
    
plotting = Plotter(loans_df)
plotting.null_percent_funded()
plotting.null_percent_term()
plotting.null_percent_int_rate()
plotting.skew_check()
plotting.outlier_removal()

    
loans_df['total_payment'].sum()/loans_df['funded_amount_inv'].sum() * 100
loans_df[loans_df['months_to_recovery'] <= 6]['total_payment'].sum() / loans_df['loan_amount'].sum() * 100
label = ['Overall Recovery', 'Recovery Up to 6 Months']
percentages = ['percent_recovery', 'percent_recovery_up_to_6_months']


percent_recovery = loans_df['total_payment'].sum()/loans_df['loan_amount'].sum() * 100
total_payment = loans_df['total_payment'].sum()
loan_amount = loans_df['loan_amount']
labels = ['Total payment', 'Loan amount']
plt.bar(labels,  color=['red', 'blue'])
plt.ylabel('Percentage (%)')
plt.title('Loan Recovery Analysis')
plt.ylim(0, 100)
plt.show()

loan_loss = len(loans_df[loans_df['loan_status'] == 'Charged Off']) #Extracting loans that were charged off
percentage_loan_loss = (loan_loss/len(loans_df)) * 100  #calculated proportion of charged off loans compared to entire dataset
print(loan_loss)
print(round(percentage_loan_loss, 2), '%')
paid_until_charged_off = loans_df.loc[loans_df['loan_status'] == 'Charged Off', 'total_payment'].sum()
print(paid_until_charged_off)

sum_paid_until_charged_off = loans_df.loc[loans_df['loan_status'] == 'Charged Off', 'total_payment'].sum() #amount of money total remaining for loans that were charged off 
total_loan_charged_off = loans_df.loc[loans_df['loan_status'] == 'Charged Off', 'loan_amount'].sum() #amount of total loan owed for the loans that were charged off
projected_loss = total_loan_charged_off - sum_paid_until_charged_off
print(projected_loss)
late = loans_df[loans_df['loan_status'].str.contains('late', case=False)] #Extracting the collumns where the contents of the loan status collunm is late
money_owed_late_payments = late['out_prncp'].sum() #loss to company if late payers status changed to charged off
print(money_owed_late_payments)
len(loans_df) #extracting the number of loanees total
number_of_late_payers = len(late) #number of loanees who have late payments
total_loanees = len(loans_df)
percentage_owed_over_total = (number_of_late_payers/total_loanees) * 100 #calculates how much of the total loanees the late payees make up 
percentage_owed_over_total_rounded = round(percentage_owed_over_total, 2)
print(percentage_owed_over_total_rounded, '%')
#calculates the proportion of late payers compared to whole dataset 
percentage_owed_over_total_late = round(percentage_owed_over_total, 2)
percentage_owed_over_total_charged_off = round(percentage_loan_loss, 2)
print(f"The percentage of payments in the dataframe that are late is {percentage_owed_over_total}, %")
print(f"The percentage of payments in the dataframe that are charged off is {percentage_owed_over_total_charged_off}, %")

money_owed_charged_off = loans_df.loc[loans_df['loan_status'] == 'Charged Off', 'loan_amount'].sum() - loans_df.loc[loans_df['loan_status'] == 'Charged Off', 'total_payment'].sum()
print(f'1 {money_owed_charged_off}')
print(f'2 {money_owed_late_payments}')
money_owed_charged_off_and_late = (money_owed_late_payments + money_owed_charged_off)/ loans_df['loan_amount'].sum() * 100
money_owed_charged_off_and_late_rounded = round(money_owed_charged_off_and_late)
print(f'The percentage of total expected revenue represented by people whose loan status is charged off and late is {money_owed_charged_off_and_late}')
loans_df_chargedoff = loans_df[loans_df['loan_status'].isin(['Charged Off'])] #Saves data where loan status is charged off 
loans_df_chargedoff.to_csv('filtered_loans.csv', index=False)
loans_paid_current = loans_df[loans_df['loan_status'].isin(['Fully paid']) & loans_df['loan_status'].isin(['Current'])] #Saves data where loan status is current
loans_paid_current.to_csv('paid_and_current_loans.csv', index=False)
