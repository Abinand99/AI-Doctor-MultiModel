
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
import base64 # The base64 module in Python is used to encode and decode data using the Base64 encoding scheme.

def encode_image(image_path):
    image_file = open(image_path,'rb')
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image



def image_query(query, model,encoded_image):
    client = Groq()
    messages = [
            {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":query
                },
                {
                    "type":"image_url",
                    "image_url":{
                    "url":f"data:image/jpeg;base64,{encoded_image}",
                    },

                },
            ],
            }
        ]
    chat_completion =client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content