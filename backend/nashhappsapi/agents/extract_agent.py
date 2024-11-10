from base_agent import BaseAgent
from backend.nashhappsapi.tools import ExtractTextTool, FileSearchTool, WriteFileTool

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
