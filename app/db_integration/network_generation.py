from database.data_fetch_customer import data_fetch
import json


def get_gender(param):
    if param == "F":
        return "Female"
    elif param == "M":
        return "Male"
    else:
        return "N/A"


def get_customer_type(param):
    if param == "IND":
        return "Individual"
    elif param == "ORG":
        return "Organization"
    else:
        return "Not available"


def get_field_value(param):
    if param == "IND":
        return "DOB"
    else:
        return "Established"


def get_residential_type(param):
    if param == "RES":
        return "Residential"
    elif param == "BUS":
        return "Business"
    elif param == "POS":
        return "Postal"
    else:
        return "N/A"


def get_unique_dic_values(key, dic_param):
    return list({val[key]: val for val in dic_param}.values())


def address_base(param):
    return {
        "name": "address",
        "desc": "List of all address linked. Click for further details.",
        "children": param
    }


def transaction_base(param):
    return {
        "name": "transaction",
        "desc": "List of all transaction linked. Click for further details.",
        "children": param
    }


def account_base(param):
    return {
        "name": "Account",
        "desc": "List of all accounts linked. Click for further details.",
        "children": param
    }


class NetworkGeneration:

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.graph_raw_data = data_fetch(self.customer_id)
        self.child_json = []
        self.customer_details = {}
        self.network_json = {}
        self.account_list = []
        self.transaction_list = []
        self.account_trans_list = []
        self.address_list = []
        self.name = "name"

    def get_json_data(self):
        self.get_customer_details(self.graph_raw_data[0])
        for row in self.graph_raw_data:
            self.get_account_details(row)
            self.get_transaction_details(row)
            self.get_address_details(row)

        self.account_list = get_unique_dic_values(self.name, self.account_list)
        self.transaction_list = get_unique_dic_values(
            self.name, self.transaction_list)
        self.address_list = get_unique_dic_values(self.name, self.address_list)
        graph_json = self.append_lists()
        return json.dumps(graph_json)

    def get_customer_details(self, data):
        self.network_json = {
            self.name: "Customer",
            "Customer Name": data[1],
            "Customer ID": data[0],
            "Gender": get_gender(data[2]),
            "Customer Type": get_customer_type(data[3]),
            get_field_value(data[3]): data[4][:10],
            "Country": "Australia"
        }

    def get_account_details(self, data):
        self.account_list.append(
            {self.name: data[10], "account_type": data[11]})

    def get_transaction_details(self, data):
        self.transaction_list.append(
            {"account_no": data[10], self.name: data[13], "transaction_type": data[14], "transaction_date": data[16],
             "transaction_amount": data[15]})

    def get_address_details(self, data):
        self.address_list.append(
            {self.name: get_residential_type(data[6]), "Detail_Address": data[5]})

    def get_account_trans_list(self):
        count = 0
        for account in self.account_list:
            account_trans_list_temp = []
            for transaction in self.transaction_list:
                if account["name"] == transaction["account_no"]:
                    account_trans_list_temp.append(
                        self.get_account_trans_list_account_based(transaction))
                # self.account_trans_list = self.account_trans_list + account_trans_list
            account["children"] = account_trans_list_temp
            self.account_trans_list.insert(count, account)
            count += 1

    def append_lists(self):
        self.get_account_trans_list()
        self.child_json.append(account_base(self.account_trans_list))
        self.child_json.append(address_base(self.address_list))
        # self.child_json.append(transaction_base(self.transaction_list))
        self.network_json["children"] = self.child_json
        return self.network_json

    def update_account_trans_list(self, account_trans_list_temp):
        self.account_trans_list.append(account_trans_list_temp)

    def get_account_trans_list_account_based(self, transaction):
        account_trans_list_temp = {self.name: transaction["name"], "transaction_type": transaction["transaction_type"],
                                   "transaction_date": transaction["transaction_date"],
                                   "transaction_amount": transaction["transaction_amount"]}
        return account_trans_list_temp
