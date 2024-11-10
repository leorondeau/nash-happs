import sys
import os
print(sys.path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from nashhappsapi.agents.base_agent import BaseAgent
from nashhappsapi.tools.extract_text_tool import ExtractTextTool
from nashhappsapi.tools.file_search_tool import FileSearchTool
from nashhappsapi.tools.write_file_tool import WriteFileTool

class ExtractAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.extract_tool = ExtractTextTool()
        self.file_search_tool = FileSearchTool()
        self.write_file_tool = WriteFileTool()

    def process(self, input_data):
        """
        Process method that receives input data (e.g., image file path) and extracts text using the tool. Use tools to generate json file of chunked text.
        """
        try:
            extracted_text = self.tool.extract(input_data)
            if extracted_text:
                print("Text extracted successfully.")
                return extracted_text
            else:
                print("No text was extracted.")
                return None
        except Exception as e:
            print(f"An error occurred during text extraction: {e}")
            return None
