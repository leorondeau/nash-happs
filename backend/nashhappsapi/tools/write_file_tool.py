import json
import os

class WriteFileTool:
    def __init__(self, output_directory='output'):
        """
        Initializes the WriteFileTool with an output directory.
        
        Args:
            output_directory (str): The directory where the JSON files will be saved.
        """
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def write_to_json(self, data, filename='output.json'):
        """
        Writes the given data to a JSON file.
        
        Args:
            data (dict or list): The data to write to the JSON file.
            filename (str): The name of the JSON file to create.
            
        Returns:
            str: The path to the written JSON file.
        """
        file_path = os.path.join(self.output_directory, filename)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"Data successfully written to {file_path}")
            return file_path
        except Exception as e:
            print(f"An error occurred while writing to JSON: {e}")
            return None
