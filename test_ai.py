import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

print("🤖 Connecting to AI server... Please wait...\n")

# 3. Send a message to an active Llama model
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Tell me in one energetic sentence why a Global AI Career Agent is the future of job hunting.",
        }
    ],
    model="llama-3.1-8b-instant", # Active and highly performant Groq model
)

# 4. Print the AI response to the terminal (Added [0] to fix the list bug)
print("🔥 AI Response:")
print(chat_completion.choices[0].message.content)

