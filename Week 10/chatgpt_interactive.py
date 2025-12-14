import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
	 
#Initialize	conversation hisyory
messages=[ 
    	{"role":	"system",	"content":	"You	are	a	helpful	assistant"} 
]

print("ChatGPT Consle Chart (type 'quit' to exit)")
print("-"*50) 
	 
while True:
    #Get user input
    user_input = input("You: ")

    #Exit condition
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break

    #Add user message to history
    messages.append({"role": "user", "content": user_input})

    #Get AI response.
    completion = openai.api_key.chat.completions.create(
        model="gpt-40",
        messages=messages
    )

    #Extract response
    assistant_message = completion.choices[0].message['content']

    #Add assistant message to history
    messages.append({"role": "assistant", "content": assistant_message})

    #Display response
    print(f"AI: {assistant_message}\n")

    