""" Data Manager Class"""

import pandas as pd

class DataManager:
    def __init__(self):
        self.data = None #Placeholder for data

    def read_local_data(self, file_path):
        """Read data from local file and store in a data attribute."""
        try:
            self.data = pd.read_csv(file_path)
            return self.data
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def save_data_to_file(self, file_path):
        """Save the uploaded data to a CVS file locally."""
        if self.data is not None:
            try:
                self.data.to_csv(file_path, index=False)
                print(f"Data saved to {file_path}")
            except Exception as e:
                print(f"Error saving file: {e}")
            else:
                print("No data to save.")

    def merge_data(self, new_data):
        """Merge new data with existing data."""
        if self.data is None:
            self.data = new_data
        else:
            self.data = pd.concat([self.data, new_data], ignore_index=True)
        return self.data

    def get_data_summary(self):
        """Returns a summary of the current data."""
        if self.data is not None:
            return self.data.head()
        return "No data available"