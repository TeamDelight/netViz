
#script to prepare data sets for insert into database from excel
#reference: 3

def insert_set_prep(table_column_list, data_dict, num_of_rec):
    data_list = []
    for row in range(0,num_of_rec):
        list_record = []
            
        for column in table_column_list:
            list_record.append(data_dict[column][row]) 
            tuple_record = tuple(list_record)
        data_list.append(tuple_record)
    return data_list