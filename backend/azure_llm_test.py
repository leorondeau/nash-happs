import os
import openai

# Set up your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = os.getenv('AZURE_GPT4_ENDPOINT')
openai.api_version = os.getenv('MODEL')
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")  # You can also directly assign your API key here

# Define the deployment name (the model you've deployed in Azure OpenAI)
deployment_name = "gpt4"  # Replace with your deployment name

try:
    # Test prompt
    prompt = "What is the capital of France?"

    # Send the request to the Azure OpenAI model using the new API format
    response = openai.ChatCompletion.create(
        engine=deployment_name,  # The deployment name of your model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )

    # Print the response from the model
    print("Response:", response['choices'][0]['message']['content'].strip())

except Exception as e:
    print("Error:", e)