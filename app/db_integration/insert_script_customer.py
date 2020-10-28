
import pandas as pd
from netViz.config.data_prep_script import insert_set_prep


def customer_data_list():
    customer_df = pd.read_excel('Data Sheet.xlsx', sheet_name="customer")
    
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
    customer_dcmnt_column_list = ['Customer number', 'Identification ID', 'Identification Type', 'Expiry Date', 'Email id' ]
    
       
    customer_details_data_list = insert_set_prep(customer_details_column_list, customer_feed, number_of_records)
    customer_address_data_list = insert_set_prep(customer_address_column_list, customer_feed, number_of_records)
    customer_contact_data_list = insert_set_prep(customer_conatct_column_list, customer_feed, number_of_records)
    customer_dcmnt_data_list = insert_set_prep(customer_dcmnt_column_list, customer_feed, number_of_records)
    
    customer_detail = {
        "customer_detail" : customer_details_data_list,
        "customer_address" : customer_address_data_list,
        "customer_contact" : customer_contact_data_list,
        "customer_document" : customer_dcmnt_data_list
        }
    
    return customer_detail



