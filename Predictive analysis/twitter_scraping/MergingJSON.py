import json

# Function to append contents of one JSON file to another
def append_json(file_to_append, file_to_update):
    try:
        # Read the existing contents from the file to update
        with open(file_to_update, 'r') as f_update:
            existing_data = json.load(f_update)

        # Read the contents from the file to append
        with open(file_to_append, 'r') as f_append:
            append_data = json.load(f_append)

        # Initialize or update 'saree' key in existing_data
        if 'kurti' in existing_data:
            existing_data['#TRENDING'].update(append_data)
        else:
            existing_data['#TRENDING'] = append_data

        # Write the merged data back to the file to update
        with open(file_to_update, 'w') as f_update:
            json.dump(existing_data, f_update, indent=4)

        print(f"Appended contents of '{file_to_append}' to '{file_to_update}' successfully.")

    except Exception as e:
        print(f"Error appending JSON files: {str(e)}")

# Example usage:
if __name__ == "__main__":
    file_to_append = 'FILE_TO_APPEND.json'
    file_to_update = 'FILE_TO_UPDATE.json'

    append_json(file_to_append, file_to_update)
