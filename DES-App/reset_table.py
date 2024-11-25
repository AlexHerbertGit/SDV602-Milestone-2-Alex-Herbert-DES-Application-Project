from jsn_drop_service import jsnDrop


def reset_user_table(jsn_drop_service):
    try:
        print("Deleting existing table...")
        jsn_drop_service.delete("des_data_sources", "*")

        print("Recreating des_data_sources table...")
        schema = {
            "id": "int",
            "name": "string(255)",
            "type": "string(50)",       # Include the 'type' field
            "data": "string(5000)",     # Increase size to 5000 characters
            "timestamp": "datetime"
        }
        result = jsn_drop_service.create("des_data_sources", schema)
        print("Create Table Response:", result)
    except Exception as e:
        print("Error resetting table:", str(e))
    
def check_table_schema(jsn_drop_service):
    try:
        print("Fetching table schema...")
        schema = jsn_drop_service.schema("des_data_sources")
        print("Table Schema:", schema)
    except Exception as e:
        print("Error fetching table schema:", str(e))

def insert_test_record(jsn_drop_service):
    try:
        print("Inserting a test record...")
        test_record = {
            "id": 1,
            "name": "Test",
            "type": "Line Chart",   # Include the 'type' field
            "data": '{"X": [1, 2, 3], "Y": [10, 20, 30]}',
            "timestamp": "2024-11-25T12:00:00Z"
        }
        result = jsn_drop_service.store("des_data_sources", [test_record])
        print("Test Record Insertion Response:", result)
    except Exception as e:
        print("Error inserting test record:", str(e))
                
def main():
    token = "39d0f8d6-bb55-4158-b364-72a33642e8ef"
    url = "https://newsimland.com/~todd/JSON/#"

    jsn_drop_service = jsnDrop(tok=token, url=url)

    reset_user_table(jsn_drop_service)
    insert_test_record(jsn_drop_service)
    check_table_schema(jsn_drop_service)

if __name__ == "__main__":
    main()

    