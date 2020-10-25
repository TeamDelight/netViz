import sys
sys.path.append("C://Users\hExaG0n//My Documents//LiClipse Workspace//")
import pandas as pd
from netViz_Dev.database.table_insert_scripts import insert_into_table
from netViz_Dev.config.Data_Prep_Script import insert_set_prep

customer_df = pd.read_excel('C://Users/hExaG0n/Desktop/Data Sheet.xlsx', sheet_name="customer")

customer_df = customer_df.replace({pd.np.nan:''})
customer_df['Data of Birth'] = customer_df['Data of Birth'].astype(str)
customer_df['Date of Establishment'] = customer_df['Date of Establishment'].astype(str)
customer_df['Expiry Date'] = customer_df['Expiry Date'].astype(str)
number_of_records = len(customer_df)
customer_feed = customer_df.to_dict()

customer_column_list = ['Customer number', 'First Name', 'Middle Name', 'Last Name', 'Cus Type', 'Data of Birth', 'Gender', 'Date of Establishment',    
'Address Line 1', 'Address Line 2',    'Address Line 3', 'City', 'State', 'Zip Code', 'Address Type', 'Contact Method', 'Contact Number', 'Email id', 
'Identification ID', 'Identification Type', 'Expiry Date', 'Open Date', 'Close Date']
customer_column_list = customer_df.columns.to_list()


customer_details_column_list = ['Customer number', 'First Name', 'Middle Name', 'Last Name', 'Cus Type', 'Data of Birth', 'Date of Establishment', 'Gender']
customer_address_column_list = ['Customer number', 'Address Line 1', 'Address Line 2', 'Address Line 3', 'City', 'State', 'Zip Code', 'Address Type']
customer_conatct_column_list = ['Customer number', 'Contact Method', 'Contact Number',  'Email id']
customer_dcmnt_column_list = ['Customer number', 'Identification ID', 'Identification Type', 'Expiry Date' ]

   
customer_details_data_list = insert_set_prep(customer_details_column_list, customer_feed, number_of_records)
customer_address_column_list = insert_set_prep(customer_address_column_list, customer_feed, number_of_records)
customer_conatct_column_list = insert_set_prep(customer_conatct_column_list, customer_feed, number_of_records)
customer_dcmnt_column_list = insert_set_prep(customer_dcmnt_column_list, customer_feed, number_of_records)

insert_into_table('CUSTOMER_DETAIL', customer_details_data_list)
insert_into_table('CUSTOMER_ADDRESS', customer_address_column_list)
insert_into_table('CUSTOMER_CONTACT', customer_conatct_column_list)
insert_into_table('CUSTOMER_DCMNT', customer_details_data_list)