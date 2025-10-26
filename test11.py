import os
from openai import AzureOpenAI

# Set up Azure OpenAI client
client = AzureOpenAI(
    api_key="3618f0a0e24c437485a987152044bd28",  
    api_version="2023-05-15",
    azure_endpoint="https://poccopilot.openai.azure.com/"
)

# Function to get AI response
def get_ai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # or your deployed model name
        messages=[
            {"role": "system", "content": "You are a silly dad."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Main conversation loop
print("Welcome! Type 'exit' to end the conversation.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    ai_response = get_ai_response(user_input)
    print("AI:", ai_response)