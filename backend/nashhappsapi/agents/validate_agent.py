import sys
import os
print(sys.path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from nashhappsapi.agents.base_agent import BaseAgent
from datetime import datetime

class ValidateAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.current_month = datetime.now().strftime("%B")  # e.g., 'March'
        self.current_date = datetime.now().strftime("%d")   # e.g., '08'
        self.date_str = str(int(self.current_date))  # Convert '08' -> '8' for more flexible matching

    def process(self, state):
        """
        Validates the text in the state for the current month and date.
        
        Args:
            state (ExtractState): The state object containing the extracted text.
            
        Returns:
            ExtractState: The updated state object with validation result and messages.
        """
        try:
            extracted_text = state.text
            if extracted_text:
                # Check if current month and date are present in the extracted text
                if self.current_month in extracted_text and (
                    self.current_date in extracted_text or self.date_str in extracted_text
                ):
                    validation_result = (
                        f"Validation successful: The text contains the current month ({self.current_month}) "
                        f"and date ({self.date_str})."
                    )
                    state.messages.append("Validation passed.")
                else:
                    validation_result = "Validation failed: The text does not contain the current month and date."
                    state.messages.append("Validation failed.")
                
                # Update state with the validation result
                state.validation_result = validation_result
            else:
                state.validation_result = "No text available for validation."
                state.messages.append("No text available for validation.")
            
            return state
        except Exception as e:
            state.validation_result = f"An error occurred during validation: {e}"
            state.messages.append(f"An error occurred during validation: {e}")
            return state
