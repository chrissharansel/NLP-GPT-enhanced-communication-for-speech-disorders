import speech_recognition as sr

def record_live_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for your voice...")

        # Continuously listen for the user's voice until stopped
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing speech...")
        speech_text = recognizer.recognize_google(audio)
        print(f"User said: {speech_text}")
        return audio, speech_text

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None, None

    except sr.RequestError:
        print("Sorry, could not request results from the service.")
        return None, None
