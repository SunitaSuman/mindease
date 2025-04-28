# openai_integration.py
import openai

openai.api_key = "your_api_key"

def get_ai_response(user_input):
    response = openai.chat.Completion.create(
        model="gpt-3.5-turbo",  # You can change this to another model if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']
