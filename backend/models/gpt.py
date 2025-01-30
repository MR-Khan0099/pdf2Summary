import openai
from backend.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_with_gpt(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following text in bullet points:\n\n{text}",
        max_tokens=200
    )
    return response['choices'][0]['text'].strip()
