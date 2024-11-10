import os
from langchain_core.tools import tool

class FileSearchTool:
    def __init__(self):
        """Initialize the FileSearchTool."""
        pass

    @tool
    def search_file(self, directory: str, filename: str):
        """
        Search for a file in the specified directory.
        
        Args:
            directory (str): The directory to search in.
            filename (str): The name of the file to search for.
            
        Returns:
            str: A message indicating whether the file was found or not, with paths if found.
        """
        result_files = []

        # Walk through the directory to search for the file
        for root, dirs, files in os.walk(directory):
            if filename in files:
                result_files.append(os.path.join(root, filename))

        if result_files:
            return f"Found file(s): {result_files}"
        else:
            return f"No files named {filename} found in {directory}."
