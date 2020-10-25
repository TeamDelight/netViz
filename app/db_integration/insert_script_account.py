import pandas as pd
from netViz_Dev.database.tabe_insert_scripts import insert_into_table
from netViz_Dev.config.Data_Prep_Script import insert_set_prep

account_df = pd.read_excel('C://Users/hExaG0n/Desktop/Data Sheet.xlsx', sheet_name="account")

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

insert_into_table('ACCOUNT_DETAIL', account_details_data_list)
insert_into_table('ACCOUNT_BALANCE', account_balance_data_list)
insert_into_table('CUS_ACC_RLTSHP', cus_acc_rltshp_data_list)