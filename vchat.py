import openai
import pyttsx3
import speech_recognition as sr

openai.api_key = "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"
engine = pyttsx3.init()

def transcribe(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("skip")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    print("Listening...")  
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            print(f"You said: {transcription}")
            if transcription.lower() == "interupt":
                speak_text("Waiting for next command.")
                return None
            return transcription
        except sr.UnknownValueError:
            speak_text("SorryCould you please repeat?")
        except sr.RequestError as e:
            print(f"Error: {e}")

def main():
    speak_text("Hello! How can I assist you today?")  
    while True:
        user_input = listen_for_command()
        if user_input is None:
            continue
        if user_input.lower() == "stop":
            speak_text("Goodbye!")  
            break  

        response = generate_response(user_input)
        print(f"Bot: {response}")

        if len(response) > 100:
            speak_text("Your answer is below. Check it out.")
        else:
            speak_text(response)  

if __name__ == "__main__":
    main()
