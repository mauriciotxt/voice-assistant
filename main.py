# Import the required libraries and modules
import speech_recognition as sr # for speech recognition
import pyttsx3 # for text to speech
import requests # for web requests
import os

# Initialize the speech recognizer and the text to speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

api_endpoint = "https://api.openai.com/v1/chat/completions"
api_key = os.environ['api_key']

# Set initial context to allow AI to understand better the requests
messages = [
    {"role": "system", "content": "You are the the best voice assistant for the Google CEO."},
]

# print(api_key) - Print your API Key in case you wanna check if it is set

def get_gpt3_response(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "max_tokens": 50
    }

    response = requests.post(api_endpoint, headers=headers, json=payload, stream=False)
    print('res:', response)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code)
        return None

# TO BE USED FOR BING (NOT TESTED YET)
# Define a function to get the Bing response for a query
# def get_bing_response(query):
#     # Set the Bing search API endpoint and the subscription key
#     endpoint = "https://api.bing.microsoft.com/v7.0/search"
#     subscription_key = "YOUR_SUBSCRIPTION_KEY" # replace with your own key

#     # Set the headers and parameters for the request
#     headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
#     params = {"q": query, "textFormat": "plain", "safeSearch": "Strict"}

#     # Send the request and get the response
#     response = requests.get(endpoint, headers=headers, params=params)
#     response.raise_for_status() # raise an exception if there is an error

#     # Parse the JSON data and get the first web result
#     data = response.json()
#     web_results = data["webPages"]["value"]
#     if web_results:
#         first_result = web_results[0]
#         title = first_result["name"]
#         snippet = first_result["snippet"]
#         url = first_result["url"]
#         # Return a formatted string with the result
#         return f"The first web result for {query} is {title}. {snippet}. You can visit the website at {url}."
#     else:
#         # Return a message if there are no web results
#         return f"Sorry, I could not find any web results for {query}."

# Define a function to listen to the user's voice and return the text
def listen():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust the ambient noise level
        recognizer.adjust_for_ambient_noise(source)
        # Listen to the user's voice
        print("Listening...")
        audio = recognizer.listen(source)
        # Recognize the speech using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except:
            # Handle the exceptions
            print("Sorry, I could not understand what you said.")
            return None

def speech_to_text():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Say something...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError as e:
        return f"Error: {e}"

# Define a function to speak the text to the user
def speak(text):
    # Set the voice properties
    engine.setProperty("rate", 200) # speech speed
    engine.setProperty("volume", 0.8) # speech volume
    voices = engine.getProperty("voices") # get the available voices
    engine.setProperty("voice", voices[1].id) # use the second voice (female)
    # Say the text
    print(f"Chat GPT response: {text}")
    engine.say(text)
    # Wait for the speech to finish
    engine.runAndWait()

# Start the main loop
while True:
    # Listen to the user's voice and get the text
    user_text = listen()
    # Check if the user said anything
    if user_text:
        # Check if the user wants to exit the app
        if user_text.lower() in ["exit", "quit", "stop", "bye"]:
            # Say goodbye and break the loop
            speak("Goodbye, have a nice day!")
            break
        else:
            # Get the Bing response for the user's query
            chat_gpt_text = get_gpt3_response(user_text)
            # Speak the Bing response to the user
            speak(chat_gpt_text)
    else:
        # Ask the user to repeat
        speak("Please say something or say exit to quit.")
