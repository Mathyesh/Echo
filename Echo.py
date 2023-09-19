import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

# Load your OpenAI API key from a .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = ""  //Enter OpenAI API key (obtain one from OpenAI)

# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    
# Test the text-to-speech functionality
text_to_speak = "Hello, I am Echo. How can I assist you today?"
SpeakText(text_to_speak)

# Initialize the recognizer
r = sr.Recognizer()

def record_text():
    while True:
        try:
            # Use the microphone as the source for input.
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                print("I'm listening")
                audio = r.listen(source)
                # Use Google's speech recognition to convert audio to text
                text = r.recognize_google(audio)
                return text
        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))
        except sr.UnknownValueError:
            print("Sorry, are you speaking?")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

# Initialize the conversation with a user greeting
messages = [{"role": "user", "content": "Please act like Echo."}]

while True:
    # Record user's voice input
    user_input = record_text()
    print(f"User: {user_input}")
    
    # Add user input to the conversation
    messages.append({"role": "user", "content": user_input})
    
    # Get a response from the assistant
    response = send_to_chatGPT(messages)
    
    # Speak the assistant's response using text-to-speech
    print(f"Assistant: {response}")
    SpeakText(f"Assistant: {response}")  # This line reads the assistant's response aloud
