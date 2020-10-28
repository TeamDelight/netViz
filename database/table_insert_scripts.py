
from app.db_integration.insert_script_customer import customer_data_list
from app.db_integration.insert_script_account import account_data_list
from app.db_integration.insert_script_transaction import transaction_data_list
import sqlite3 as sql1

con = sql1.connect("netviz_dev.db", check_same_thread=False)

def insert_into_table(table_name, data_list):   
    query = """PRAGMA table_info(""" + table_name + """)"""
    
    with con:
        query_data = con.execute(query)    
    
    column_list = [row[1] for row in query_data if row[1].upper() not in ('OPEN_DT','CLOSE_DT')]
    value_list = ['?'] * len(column_list)
    
    insert_sql = "insert into " + table_name + "(" + ','.join(column_list) + ") values (" + ','.join(value_list) + ")"
    
    with con:
        con.executemany(insert_sql, data_list)        

    
def customer_insert_script():
    customer_detail = customer_data_list()
    
    customer_details_data_list = customer_detail["customer_detail"]
    customer_address_column_list = customer_detail["customer_address"]
    customer_conatct_column_list= customer_detail["customer_contact"]
    customer_dcmnt_data_list = customer_detail["customer_document"]
    
    insert_into_table('CUSTOMER_DETAIL', customer_details_data_list)
    insert_into_table('CUSTOMER_ADDRESS', customer_address_column_list)
    insert_into_table('CUSTOMER_CONTACT', customer_conatct_column_list)
    insert_into_table('CUSTOMER_IDN_DOC', customer_dcmnt_data_list)


def account_insert_script():
    account_detail = account_data_list()
    
    account_details_data_list = account_detail["account_detail"]
    account_balance_data_list = account_detail["account_balance"]
    cus_acc_rltshp_data_list = account_detail["cus_acc_rltshp"]
    
    insert_into_table('ACCOUNT_DETAIL', account_details_data_list)
    insert_into_table('ACCOUNT_BALANCE', account_balance_data_list)
    insert_into_table('CUS_ACC_RLTSHP', cus_acc_rltshp_data_list)


def transaction_insert_script():
    transaction_detail = transaction_data_list()
    
    insert_into_table('TRANSACTION_DETAIL', transaction_detail)
    
transaction_insert_script()
