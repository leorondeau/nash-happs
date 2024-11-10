import re
from datetime import datetime
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import time
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from dotenv import load_dotenv

load_dotenv()

VISION_ENDPOINT = os.environ["VISION_ENDPOINT"]
VISION_KEY = os.environ["VISION_KEY"]

# Authenticate client
computervision_client = ComputerVisionClient(VISION_ENDPOINT, CognitiveServicesCredentials(VISION_KEY))


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

    # Collect extracted text lines
    extracted_lines = []
    if result.status == OperationStatusCodes.succeeded:
        for text_result in result.analyze_result.read_results:
            for line in text_result.lines:
                extracted_lines.append(line.text)

    return extracted_lines

# Function to check if the current date is within the date range
def is_current_week(text_lines):
    current_date = datetime.now().date()

    # Regex to capture date ranges like "September 3RD-7TH" or "August 26-September 2"
    date_range_pattern = re.compile(r'(\b[A-Za-z]+\s\d{1,2}(?:st|nd|rd|th)?\b)\s*-\s*(\b[A-Za-z]*\s?\d{1,2}(?:st|nd|rd|th)?\b)')

    for line in text_lines:
        # Check if the line contains a date range
        match = date_range_pattern.search(line)
        if match:
            start_date_str, end_date_str = match.groups()

            try:
                # Parse the start date
                start_date = datetime.strptime(f"{start_date_str} {current_date.year}", "%B %d %Y").date()

                # If the end date doesn't have a month, assume it's the same as the start month
                if not end_date_str.split()[0].isalpha():  # If the end date doesn't contain a month
                    end_date_str = f"{start_date.strftime('%B')} {end_date_str}"

                # Parse the end date
                end_date = datetime.strptime(f"{end_date_str} {current_date.year}", "%B %d %Y").date()

                # Check if the current date falls within the range
                if start_date <= current_date <= end_date:
                    return True
            except ValueError as e:
                # Print error for debugging
                print(f"Error parsing date: {e} in line '{line}'")
    
    return False
