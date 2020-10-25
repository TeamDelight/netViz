import sys
sys.path.append("C://Users\hExaG0n//My Documents//LiClipse Workspace//")
from netViz_Dev.database.data_fetch_customer import data_fetch

"""cus_id = ""
for row1 in data_fetch(1001):
    for row2 in data_fetch(1001):
        if row1[0] == row2[0]:"""
            
for row in data_fetch(1001):
    print(row)
