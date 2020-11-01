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


def get_contact_details(param):
    if param.isnumeric():
        return param
    else:
        return "N/A"


def get_email_details(param):
    if "@" in param:
        return param
    else:
        return "N/A"


def get_unique_dic_values(key, dic_param):
    return list({val[key]: val for val in dic_param}.values())


def get_base_json(key, param):
    description_message = "Hover on top of the linked items for more details.",
    return {
        "name": key,
        "Description": description_message,
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
        self.email_lists = []
        self.identification_doc_list = []
        self.contacts_lists = []
        self.name = "name"
        self.trans_type = "Transaction Type"
        self.trans_date = "Transaction Date"
        self.trans_amt = "Transaction Amount"

    def get_json_data(self):
        self.get_customer_details(self.graph_raw_data[0])
        for row in self.graph_raw_data:
            self.get_account_details(row)
            self.get_transaction_details(row)
            self.get_address_details(row)
            self.get_identification_doc_details(row)
            self.get_contact_details(row)

        self.account_list = get_unique_dic_values(self.name, self.account_list)
        self.transaction_list = get_unique_dic_values(
            self.name, self.transaction_list)
        self.address_list = get_unique_dic_values(self.name, self.address_list)
        graph_json = self.append_lists()
        print(graph_json)
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
            {self.name: data[10], "Account Type": data[11], "Available Balance": data[12]})

    def get_transaction_details(self, data):
        self.transaction_list.append(
            {"account_no": data[10], self.name: data[13], self.trans_type: data[14], self.trans_date: data[16],
             self.trans_amt: data[15]})

    def get_address_details(self, data):
        self.address_list.append(
            {self.name: get_residential_type(data[6]), "Detail Address": data[5]})

    def get_account_trans_list(self):
        count = 0
        for account in self.account_list:
            account_trans_list_temp = []
            for transaction in self.transaction_list:
                if account["name"] == transaction["account_no"]:
                    account_trans_list_temp.append(
                        self.get_account_trans_list_account_based(transaction))
            account["children"] = account_trans_list_temp
            self.account_trans_list.insert(count, account)
            count += 1

    def get_identification_doc_details(self, data):
        self.identification_doc_list.append(
            {self.name: (data[9]), "Identification Number": data[8]})

    def get_contact_details(self, data):
        self.contacts_lists.append(
            {self.name: "Phone", "Phone Number": get_contact_details(data[7])})
        self.contacts_lists.append(
            {self.name: "email", "eMail ID": get_email_details(data[7])})

    def append_lists(self):
        self.get_account_trans_list()
        self.child_json.append(get_base_json(
            "Accounts", self.account_trans_list))
        self.child_json.append(get_base_json("Address", self.address_list))
        self.child_json.append(get_base_json(
            "Documents", self.identification_doc_list))
        self.child_json.append(get_base_json("Contacts",
                                             self.contacts_lists + self.email_lists))
        self.network_json["children"] = self.child_json
        return self.network_json

    def update_account_trans_list(self, account_trans_list_temp):
        self.account_trans_list.append(account_trans_list_temp)

    def get_account_trans_list_account_based(self, transaction):
        account_trans_list_temp = {self.name: transaction["name"], self.trans_type: transaction[self.trans_type],
                                   self.trans_date: transaction[self.trans_date],
                                   self.trans_amt: transaction[self.trans_amt]}
        return account_trans_list_temp
