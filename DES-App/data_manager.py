""" Data Manager Class """
from jsn_drop_service import jsnDrop
import pandas as pd

class DataManager:
    def __init__(self, jsn_drop_service):
        self.jsn_drop_service = jsn_drop_service
        self.local_data = None
        self.remote_data = None  # Placeholder for remote data

        self.create_table()

    def create_table(self):
        """Creates the 'des_data_sources' table dynamically based on local data."""
        try:
            schema = {
                "id": "int",
                "name": "string(255)",
                "type": "string(50)",
                "data": "text",  # Storing raw CSV as text
                "timestamp": "datetime"
            }
            result = self.jsn_drop_service.create("des_data_sources", schema)

            print("Create Table Response:", result)

            if isinstance(result, dict) and result.get("Status") == "SUCCESS.CREATE":
                print("Table 'des_data_sources' created successfully.")
            else:
                print(f"Table 'des_data_sources' skipped or failed: {result}")
        except Exception as e:
            print(f"Error creating table 'des_data_sources': {str(e)}")

    def read_local_data(self, file_path):
        """Read data from local file and store in a local_data attribute."""
        try:
            self.local_data = pd.read_csv(file_path)
            return self.local_data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def save_data_to_file(self, file_path):
        """Save the local data to a CSV file."""
        if self.local_data is not None:
            try:
                self.local_data.to_csv(file_path, index=False)
                print(f"Data saved to {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print("No data to save.")

    def merge_data(self, new_data):
        """Merge new data (local or remote) with existing local data."""
        if new_data is not None:
            if self.local_data is None:
                self.local_data = new_data
            else:
                self.local_data = pd.concat([self.local_data, new_data], ignore_index=True)
            return self.local_data
        return "No new data to merge."

    def get_data_summary(self):
        """Returns a summary of the current data."""
        if self.local_data is not None:
            return self.local_data.head()
        return "No data available"

    def upload_to_remote(self, table_name, dataset_name, dataset_type, file_path):
        """Upload the current .csv file content to the remote database."""
        try:
            # Read the .csv file content
            with open(file_path, "r") as file:
                csv_content = file.read()

            record = {
                "name": dataset_name,
                "type": dataset_type,
                "data": csv_content,
                "timestamp": pd.Timestamp.now().isoformat()
            }

            result = self.jsn_drop_service.store(table_name, [record])
            if isinstance(result, dict) and result.get("Status") == "SUCCESS.STORE":
                return "Data source uploaded successfully."
            return f"Failed to upload data source: {result.get('Result', 'Unknown error')}"
        except Exception as e:
            return f"Error uploading data source: {str(e)}"

    def fetch_from_remote(self, table_name, dataset_name):
        """Fetch the .csv file content from the remote database."""
        try:
            result = self.jsn_drop_service.select(table_name, {"name": dataset_name})
            if isinstance(result, dict) and result.get("Status") == "SUCCESS.SELECT":
                record = result.get("Result")[0]  # Assuming the name is unique
                csv_content = record["data"]

                # Save the .csv content to a local file
                local_file_path = f"{dataset_name}.csv"
                with open(local_file_path, "w") as file:
                    file.write(csv_content)

                # Load the fetched data into local_data
                self.local_data = pd.read_csv(local_file_path)
                return f"Data fetched, saved as {local_file_path}, and loaded locally."
            return f"Failed to fetch data source: {result.get('Result', 'Unknown error')}"
        except Exception as e:
            return f"Error fetching data source: {str(e)}"

    def get_remote_data_summary(self):
        """Returns a summary of the remote data source."""
        if self.remote_data is not None:
            return self.remote_data.head()
        return "No remote data available."
