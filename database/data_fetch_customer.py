import sqlite3 as sql1

con = sql1.connect("netviz_dev.db")


def suggestion_data_fetch(search_string):
    query = "select * from search_suggestion_v where upper(cus_details) like '%" + str(search_string) + "%' limit 15;"
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data]
    
    return query_list 

def suggestion_cusid_fetch(search_string):
    query = "select cus_id from search_suggestion_v where upper(cus_details) like '%" + str(search_string) + "%' limit 15;"
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data]
    
    return query_list 


def search_fetch(cus_id):
    query = "select * from SEARCH_RESULT_V where cus_id = '" + str(cus_id) + "';"
    
    with con:
        query_data = con.execute(query)
    
    query_list = [row for row in query_data]
    
    return query_list 


def data_fetch(customer_id):   
    query = "select * from CUSTOMER_ALL_V where cus_id = '" + str(customer_id) + "';"
    
    with con:
        query_data = con.execute(query)
        
    query_list = [row for row in query_data] 
    
    return query_list