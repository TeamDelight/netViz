import sys
sys.path.append("C://Users\hExaG0n//My Documents//LiClipse Workspace//")
from netViz_Dev.database.data_fetch_customer import search_fetch, suggestion_data_fetch, suggestion_cusid_fetch
import time


def search_suggestion(search_string):
    suggestion_list = [row[1] for row in suggestion_data_fetch(search_string)]
    
    return suggestion_list


def search_result_data_fetch1(search_string):
    search_result_list = suggestion_cusid_fetch(search_string)    
    cus_id_list = [row[0] for row in search_result_list]
    cus_id_list = list(set(cus_id_list))
    cus_id_list.sort()
        
    return cus_id_list


def search_result_data_fetch2(cus_id):
    string = ""    
    search_result_fetch = search_fetch(cus_id)    
    
    string = list(search_result_fetch[0])    
    
    for row in search_result_fetch:        
        if string[2] != row[2]:               
            string[2] += "|" + str(row[2])
        elif string[3] != row[3]:                
            string[3] += "|" + str(row[3])  
        elif string[4] != row[4]:                
            string[4] += "|" + str(row[4])  
    
    return string
    

def search_result_data_fetch3(search_string):
    cus_id_list = search_result_data_fetch1(search_string)
    search_result_dict = []
    temp = {}
    
    for cus_id in cus_id_list:
        search_result_list = search_result_data_fetch2(cus_id)
        
        temp = {
            "id" : search_result_list[0], 
            "name" : search_result_list[1], 
            "phone" : search_result_list[3], 
            "address" : search_result_list[2], 
            "account" : search_result_list[4]
        }
        
        search_result_dict.append(temp)
                
    return search_result_dict