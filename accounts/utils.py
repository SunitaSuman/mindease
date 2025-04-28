import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_ai_response(user_input):
    try:
        # Make a request to OpenAI's GPT model
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose other models like "gpt-3.5-turbo" too
            prompt=user_input,
            max_tokens=150,  # You can adjust the number of tokens as needed
            temperature=0.7  # Controls the randomness of the response (0.0 to 1.0)
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
