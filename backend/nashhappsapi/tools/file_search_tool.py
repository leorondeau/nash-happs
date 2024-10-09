import os
from langchain_core.tools import tool

# Define a file search tool
@tool
def file_search(directory: str, filename: str):
    """Search for a file in the specified directory."""
    # List to store paths of found files
    result_files = []

    # Walk through the directory to search for the file
    for root, dirs, files in os.walk(directory):
        if filename in files:
            result_files.append(os.path.join(root, filename))
    
    if result_files:
        return f"Found file(s): {result_files}"
    else:
        return f"No files named {filename} found in {directory}."

# Use it in your LangGraph setup
tools = [file_search]
