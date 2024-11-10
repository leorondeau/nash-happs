from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = ""
endpoint = ""

# Authenticate the client
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Basic test to verify the connection
def test_connection():
    try:
        # Test the connection by sending a request to describe an image
        print("Testing the connection...")
        remote_image_url = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"
        description_results = computervision_client.describe_image(remote_image_url)

        if description_results.captions:
            print("Connection successful! Description:", description_results.captions[0].text)
        else:
            print("Connection successful, but no description found.")
    except Exception as e:
        print(f"Error: {e}")

# Run the test
test_connection()
