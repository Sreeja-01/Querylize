import openai

try:
    # Example OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}],
        max_tokens=100
    )
except openai.error.RateLimitError:
    print("Rate limit exceeded, please try again later.")
except openai.error.OpenAIError as e:
    print(f"OpenAI error occurred: {str(e)}")
except Exception as e:
    print(f"An unexpected error occurred: {str(e)}")
