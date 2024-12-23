import requests 
import json 

#6c420424-62ad-4218-8b1f-d6cf2115facd
#https://docs.python.org/3/library/json.html


class jsnDrop(object):

    def __init__(self, tok = None, url = None) -> None:
        self.tok = tok
        self.url = url
        self.jsnStatus = ""
        self.jsnResult = {}

        # Setting up data structures for storing JsnDrop Commands
        self.decode = json.JSONDecoder().decode
        self.encode = json.JSONEncoder().encode

        self.jsnDropRecord = self.decode('{"tok":"","cmd":{}}')
        self.jsnDropCreate = self.decode('{"CREATE":"aTableName","EXAMPLE":{}}')
        self.jsnDropStore  = self.decode('{"STORE":"aTableName","VALUE":[]}')
        self.jsnDropAll    = self.decode('{"ALL":"aTableName"}')
        self.jsnDropSelect = self.decode('{"SELECT":"aTableName","WHERE":"aField = b"}')
        self.jsnDropDelete = self.decode('{"DELETE":"aTableName","WHERE":"aField = b"}')
        self.jsnDropDrop   = self.decode('{"DROP":"aTableName"}')

    def jsnDropApi(self,command):
        api_call  = self.jsnDropRecord
        api_call["tok"] = self.tok
        api_call["cmd"] = command
        payload = {'tok': self.encode(api_call)}

        # Feedback to check it works
        # print(f"API CALL PAYLOAD= {payload}")

        # Request to the API - LOOK UP calls to requests.get() ARE they Synchronous or Asynchronous?
        r = requests.get(self.url, payload)

        # Update the status and result
        jsnResponse = r.json()
        self.jsnStatus = jsnResponse["JsnMsg"]
        self.jsnResult = jsnResponse["Msg"]

        # Feedback to check it works
        print(f"Status = {self.jsnStatus} , Result = {self.jsnResult}")
        return self.jsnResult 

    
    def create(self,table_name, example):
        command = self.jsnDropCreate
        command["CREATE"] = table_name
        command["EXAMPLE"] = example
        return self.jsnDropApi(command)
        
    def store(self, table_name, value_list):
        command = self.jsnDropStore
        command["STORE"] = table_name
        command["VALUE"] = value_list
        return self.jsnDropApi(command)

    def all(self, table_name):
        command = self.jsnDropAll
        command["ALL"] = table_name
        return self.jsnDropApi(command)

    def select(self, table_name, where):
        command = self.jsnDropSelect
        command["SELECT"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)

    def delete(self,table_name, where):
        command = self.jsnDropDelete
        command["DELETE"] = table_name
        command["WHERE"] = where
        return self.jsnDropApi(command)

    def drop(self,table_name):
        command = self.jsnDropDrop
        command["DROP"] = table_name
        return self.jsnDropApi(command)

    def upload_data_source(self, table_name, data):
        """Upload data source to the JsnDrop database"""
        try:
            result = self.store(table_name, data)
            if result:
                return "Data source uploaded successfully."
            return "Failed to upload data source."
        except Exception as e:
            return f"Error uploading data source: {str(e)}"

    def fetch_data_source(self, table_name):
        """Retrieve data source from JsnDrop database"""
        try:
            data = self.all(table_name)
            if data:
                return data
            return []
        except Exception as e:
            return f"Error fetching data source: {str(e)}"

    def schema(self, table_name):
        """Fetch and display the schema of the given table."""
        try:
            print(f"Attempting to infer schema for table '{table_name}'...")
            all_records = self.all(table_name)  # Fetch all data to infer schema
            if all_records and isinstance(all_records, list):
                # Infer schema from the first record if data exists
                first_record = all_records[0] if all_records else {}
                inferred_schema = {key: type(value).__name__ for key, value in first_record.items()}
                print(f"Inferred Schema: {inferred_schema}")
                return inferred_schema
            else:
                print(f"No records found in '{table_name}' to infer schema.")
                return {}
        except Exception as e:
            print(f"Error inferring schema: {str(e)}")
            return {}        


