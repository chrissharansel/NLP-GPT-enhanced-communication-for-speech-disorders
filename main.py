import os
import requests
from utils.speech_recognition import record_live_speech
from utils.voice_analysis import analyze_voice

def get_feedback_from_gpt(voice_analysis, speech_text):
    url = "https://open-ai21.p.rapidapi.com/claude3"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": (
                    f"The user has a speech disorder. They said: {speech_text}. "
                    f"Provide feedback on their speech considering this context."
                )
            }
        ],
        "web_access": False
    }
    headers = {
        "x-rapidapi-key": "c1121ad9edmsh28a3e1ba931dcf9p10b968jsnd61824ad3d31",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

def create_api_prompt(transcript, user_profile, audio_data, pacing_data):
    avg_pitch, tempo = analyze_audio_features(audio_data)  # Ensure this function is defined

    prompt = f"""
    User Profile:
    - Name: {user_profile['name']}
    - Profession: {user_profile['profession']}
    - Speech Goals: {', '.join(user_profile['speech_goals'])}
    - Event Type: {user_profile['event_type']}
    - Audience Type: {user_profile['audience_type']}

    Analyze the following speech:
    '{transcript}'

    Provide detailed feedback on the following aspects:
    - Pacing
    - Clarity and articulation
    - Suggestions for improving engagement and confidence

    Additionally, incorporate any relevant progress tracking based on the previous sessions:
    - Last session pacing: {pacing_data[-1] if pacing_data else 'N/A'}

    Suggestions should be actionable and tailored to the user's goals, specifically addressing their speech disorder.
    """

    return prompt

if __name__ == "__main__":
    user_profile = {
        'name': 'User',
        'profession': 'Speaker',
        'speech_goals': ['Improve clarity', 'Increase engagement'],
        'event_type': 'Presentation',
        'audience_type': 'General Public'
    }
    
    pacing_data = []

    while True:
        print("Listening... Press Ctrl+C to stop.")

        # Step 1: Capture and Transcribe Live Speech from Microphone
        audio_data, speech_text = record_live_speech()

        if audio_data and speech_text:
            # Save the recorded audio to a WAV file
            audio_path = "audio/user_voice.wav"
            with open(audio_path, "wb") as f:
                f.write(audio_data.get_wav_data())

            # Step 2: Analyze Voice using the saved audio file
            voice_analysis = analyze_voice(audio_path)

            # Step 3: Generate Feedback from GPT
            feedback = get_feedback_from_gpt(voice_analysis, speech_text)

            if feedback:
                if 'result' in feedback:
                    print("AI Feedback:")
                    print(feedback['result'])
                else:
                    print("No 'result' key found in API response")
        
        print("\nWaiting for next input...")
