import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
api_version=os.getenv('API_VERSION'),
api_key=os.getenv('AZURE_OPENAI_API_KEY'))

# Set up your Azure OpenAI credentials
  # You can also directly assign your API key here

# Define the deployment name (the model you've deployed in Azure OpenAI)
deployment_name = ""  # Replace with your deployment name

response = client.chat.completions.create(
    model=deployment_name, # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content)