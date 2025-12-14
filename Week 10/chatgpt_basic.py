import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#Make a simple API call
competion = openai.api_key.chat.completions.create(
    model="gpt-40",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What is AI?"}

    ]
)

#Print the response.
print(competion.choices[0].message.content)