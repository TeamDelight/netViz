import sys
sys.path.append("C://Users\hExaG0n//My Documents//LiClipse Workspace//")
from netViz_Dev.database.data_fetch_customer import data_fetch
import json


def network_json_gen(cus_id):
    network_list = data_fetch(cus_id)
    network_json = {}
    string = list(network_list[0])
    string[15] = str(string[15])
    
    #compiling all records in a list
    for row in network_list:
        if string[5] != row[5]:
            string[5] += "|" + str(row[5])
            string[6] += "|" + str(row[6])        
        if string[7] != row[7]:
            string[7] += "|" + str(row[7])
        if string[8] != row[8]:
            string[8] += "|" + str(row[8])
        if string[9] != row[9]:
            string[9] += "|" + str(row[9])
        if string[10] != row[10]:
            string[10] += "|" + str(row[10])    
            string[11] += "|" + str(row[11])
        if string[13] != row[13]:
            string[13] += "|" + str(row[13])        
            string[14] += "|" + str(row[14])         
        if string[15] != str(row[15]):
            string[15] += "|" + str(row[15])         
        if string[16] != row[16]:
            string[16] += "|" + str(row[16])
    
    #separating customer type
    if string[3] == "IND":
        cus_type = "Individual"
    elif string[3] == "ORG":
        cus_type = "Organization"
        
    #json config
    network_json1 = {
        "name" : "Customer",
        "Customer Name" : string[1],  
        "Gender" : string[2],
        "Customer Type" : cus_type,      
        "dob" : string[4],
        "city" : "who cares?",
        "Country": "Australia"        
        }
    
    network_json2 = {
        "children" : ""
        }
    
    #account data
    network_account_json = {
        "name" : "Account",
        "desc" : "List of all accounts linked. Click for further details.",
        "children" : ""
        }
    
    account_list1 = [{"name": row} for row in string[10].split("|")]
    account_list2 = [{"account_type": row} for row in string[11].split("|")]
    
    for i in range(0, len(account_list1)):
        account_list1[i].update(account_list2[i]) 
    
    network_account_json["children"] = account_list1
    
    #transaction data
    network_transaction_json = {
        "name" : "transaction",
        "desc" : "List of all transaction linked. Click for further details.",
        "children" : ""
        }    
    
    transaction_list1 = [{"reference_num": row} for row in string[13].split("|")]
    transaction_list2 = [{"transaction_type": row} for row in string[14].split("|")]
    transaction_list3 = [{"transaction_amount": row} for row in string[15].split("|")]
    transaction_list4 = [{"transaction_date": row} for row in string[16].split("|")]    
    
    for i in range(0, len(transaction_list1)):
        transaction_list1[i].update(transaction_list2[i])
        transaction_list1[i].update(transaction_list3[i])
        transaction_list1[i].update(transaction_list4[i])  
    
    network_transaction_json["children"] = transaction_list1
   
    #address
    network_address_json = {
        "name" : "address",
        "desc" : "List of all address linked. Click for further details.",
        "children" : ""
        }    
    
    address_list1 = [{"address_type": row} for row in string[6].split("|")]
    address_list2 = [{"address_desc": row} for row in string[5].split("|")]
    
    for i in range(0, len(address_list1)):
        address_list1[i].update(address_list2[i])
    
    network_address_json["children"] = address_list1
    
    network_json2_list = [network_account_json, network_transaction_json, network_address_json]
    network_json2["children"] = network_json2_list    
    network_json1.update(network_json2)
    
    return json.dumps(network_json1)