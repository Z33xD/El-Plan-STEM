import os
import google.generativeai as genai
#from main import text_to_speech

from dotenv import load_dotenv
load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction='''You are an expert educator and a Formula 1 enthusiast. You ask questions on math that are themed around Formula 1.

Wait for the student to give their final answer. If correct, congratulate them and offer another question.

If they are incorrect, explain the right answer clearly using F1 analogies that are fun and easy to follow, even for someone who isn't very knowledgeable about Formula 1.
''',
)

# Initialize chat session
chat_session = model.start_chat(history=[])

def get_chat_response(user_input):
    """
    Get a response from the chatbot for the given user input.
    """
    try:
        response = chat_session.send_message(user_input)
        model_response = response.text
        
        # Update chat history
        chat_session.history.append({"role": "user", "parts": [user_input]})
        chat_session.history.append({"role": "model", "parts": [model_response]})
        
        return model_response
    except Exception as e:
        return f"Error: {str(e)}"

# Only run the terminal interface if this file is run directly
if __name__ == "__main__":
    print("Bot: Hello, how can I help you?")
    print()
    #text_to_speech("Hello, how can I help you?")

    while True:
        user_input = input("You: ")
        print()

        response = get_chat_response(user_input)
        print(f'Bot: {response}')
        print()
        #text_to_speech(response)