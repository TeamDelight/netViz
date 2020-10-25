import pandas as pd
from netViz_Dev.database.tabe_insert_scripts import insert_into_table
from netViz_Dev.config.Data_Prep_Script import insert_set_prep

transaction_df = pd.read_excel('C://Users/hExaG0n/Desktop/Data Sheet.xlsx', sheet_name="transaction")

transaction_df = transaction_df.replace({pd.np.nan:''})
transaction_df['Transaction Date'] = transaction_df['Transaction Date'].astype(str)
number_of_records = len(transaction_df)
transaction_feed = transaction_df.to_dict()

transaction_column_list = ['Transaction Reference Number', 'Account ID', 'Transaction Type', 'Transaction Date', 'Amount']
transaction_column_list = transaction_df.columns.to_list()

transaction_details_column_list = ['Transaction Reference Number', 'Account ID', 'Transaction Type', 'Transaction Date', 'Amount']
    
account_details_data_list = insert_set_prep(transaction_details_column_list, transaction_df, number_of_records)

insert_into_table('TRANSACTION_DETAIL', account_details_data_list)