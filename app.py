import openai  # Corrected OpenAI import
from apikey import api_data
import os
import speech_recognition as sr  # Converts voice commands to text
import pyttsx3  # Reads text output as voice
import webbrowser

# Set up OpenAI API
openai.api_key = api_data
model = "gpt-4"

# Function to get AI response
def reply(question):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': "system", "content": "You are a helpful assistant."},
                {'role': 'user', 'content': question}
            ],
            max_tokens=200
        )
        answer = completion.choices[0].message.content
        return answer
    except Exception as e:
        print("Error in OpenAI API call:", e)
        return "I'm sorry, I couldn't process your request."

# Text-to-speech setup
engine = pyttsx3.init('nsss')  # Use 'nsss' for macOS
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Speech-to-text function
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # Wait for 1 second before considering a pause
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that. Please try again.")
            return "none"
        except sr.RequestError as e:
            print(f"Speech Recognition error: {e}")
            return "none"

# Main loop
if __name__ == '__main__':
    speak("Hello! How can I assist you today?")
    while True:
        query = take_command()
        if query == 'none':
            continue

        if "bye" in query:
            speak("Goodbye! Have a great day!")
            break

        # Get AI response and speak it out
        ans = reply(query)
        print(ans)
        speak(ans)

        # Specific browser-related tasks
        if "open youtube" in query:
            webbrowser.open('https://www.youtube.com')
        elif "open google" in query:
            webbrowser.open('https://www.google.com')
