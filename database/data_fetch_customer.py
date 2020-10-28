import os
import sqlite3 as sql1

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "netviz_dev.db")


def suggestion_data_fetch(search_string):
    
    con = sql1.connect(db_path, check_same_thread=False)
    query = "select * from SEARCH_SUGGESTION_V where upper(cus_details) like '%" + str(search_string).upper() + "%' limit 15;"
    
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data]
    
    con.close() 
    
    return query_list 

def suggestion_cusid_fetch(search_string):
    
    con = sql1.connect(db_path, check_same_thread=False)
    query = "select cus_id from search_suggestion_v where upper(cus_details) like '%" + str(search_string).upper() + "%' limit 15;"
    
    with con:
        query_data = con.execute(query)    
    
    query_list = [row for row in query_data]
    
    con.close()
    
    return query_list 

def search_fetch(cus_id):
    
    con = sql1.connect(db_path, check_same_thread=False)
    query = "select * from SEARCH_RESULT_V where cus_id = '" + str(cus_id) + "';"
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data]
    
    con.close()
    
    return query_list 


def data_fetch(customer_id):
    
    con = sql1.connect(db_path, check_same_thread=False)    
    query = "select * from CUSTOMER_ALL_V where cus_id = '" + str(customer_id) + "';"
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data] 
    
    con.close()
    
    return query_list