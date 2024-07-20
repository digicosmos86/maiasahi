import os

from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

client = openai.OpenAI()
