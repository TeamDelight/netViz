import sqlite3 as sql1

con = sql1.connect("netviz_dev.db")

def insert_into_table(table_name, data_list):   
    query = """PRAGMA table_info(""" + table_name + """)"""
    
    with con:
        query_data = con.execute(query)    
    
    column_list = [row[1] for row in query_data if row[1].upper() not in ('OPEN_DT','CLOSE_DT')]
    value_list = ['?'] * len(column_list)
    
    insert_sql = "insert into " + table_name + "(" + ','.join(column_list) + ") values (" + ','.join(value_list) + ")"
    
    with con:
        con.executemany(insert_sql, data_list)