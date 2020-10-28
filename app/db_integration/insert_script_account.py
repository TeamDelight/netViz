import pandas as pd
from config.data_prep_script import insert_set_prep

def account_data_list():
    account_df = pd.read_excel('Data Sheet.xlsx', sheet_name="account")
    
    account_df = account_df.replace({pd.np.nan:''})
    number_of_records = len(account_df)
    account_feed = account_df.to_dict()
    
    account_column_list = ['Account ID', 'Account Status', 'Product Code', 'Account Balance', 'Balance', 'Customer ID']
    account_column_list = account_df.columns.to_list()
    
    account_details_column_list = ['Account ID', 'Account Status', 'Product Code']
    account_balance_column_list = ['Account ID', 'Account Balance']
    cus_acc_rltshp_column_list = ['Account ID', 'Customer ID']
    
        
    account_details_data_list = insert_set_prep(account_details_column_list, account_feed, number_of_records)
    account_balance_data_list = insert_set_prep(account_balance_column_list, account_feed, number_of_records)
    cus_acc_rltshp_data_list = insert_set_prep(cus_acc_rltshp_column_list, account_feed, number_of_records)
    
    account_detail = {
        "account_detail" : account_details_data_list,
        "account_balance" : account_balance_data_list,        
        "cus_acc_rltshp" : cus_acc_rltshp_data_list
        }
    
    return account_detail

print(account_data_list())