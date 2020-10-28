import pandas as pd
from netViz.config.data_prep_script import insert_set_prep


def transaction_data_list():
    transaction_df = pd.read_excel('Data Sheet.xlsx', sheet_name="transaction")
    
    transaction_df = transaction_df.replace({pd.np.nan:''})
    transaction_df['Transaction Date'] = transaction_df['Transaction Date'].astype(str)
    number_of_records = len(transaction_df)
    transaction_feed = transaction_df.to_dict()
    
    transaction_column_list = ['Transaction Reference Number', 'Account ID', 'Transaction Type', 'Transaction Date', 'Amount']
    transaction_column_list = transaction_df.columns.to_list()
    
    transaction_details_column_list = ['Transaction Reference Number', 'Account ID', 'Transaction Type', 'Amount', 'Transaction Date']
        
    account_details_data_list = insert_set_prep(transaction_details_column_list, transaction_df, number_of_records)
    
    return account_details_data_list  
    