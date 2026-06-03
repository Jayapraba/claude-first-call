from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
##print(os.environ.get("ANTHROPIC_API_KEY"))

#Create client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Make your first API call
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello Claude! I am Jaya. I am learning AI. Give me one tip for success."}
    ]
)

# Print the response
print(response.content[0].text) 