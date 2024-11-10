
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time

# Set up your credentials
subscription_key = ""  # Replace with your API key
endpoint = ""  # Replace with your endpoint URL

# Authenticate client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Function to extract text from an image
def extract_text_from_image(image_path):
    with open(image_path, "rb") as image_stream:
        # Call the API to recognize printed or handwritten text in the image
        read_response = computervision_client.read_in_stream(image_stream, raw=True)
    
    # Get the operation location (ID) from the response
    operation_location = read_response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    # Wait for the result
    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break
        time.sleep(1)

    # Print the results
    if result.status == OperationStatusCodes.succeeded:
        for text_result in result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)

# Test block
if __name__ == "__main__":
    # Provide the path to your image
    image_path = "/Users/admin/workspace/nash-happs/backend/temp/2024-08-12_16-56-30_UTC.jpg"
    
    if os.path.exists(image_path):
        extract_text_from_image(image_path)
    else:
        print(f"Image file {image_path} not found.")
