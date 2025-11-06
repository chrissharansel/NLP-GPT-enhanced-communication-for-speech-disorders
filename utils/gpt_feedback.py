import requests

def get_feedback_from_gpt(voice_analysis, speech_text):
    url = "https://open-ai21.p.rapidapi.com/claude3"
    
    # Generate prompt for GPT feedback based on voice analysis
    content = f"The user's speech text is: {speech_text}. The voice analysis data is: {voice_analysis}. Please provide feedback on what is wrong with the speech and how it can be improved."

    payload = {
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "web_access": False
    }

    headers = {
        "x-rapidapi-key": "c1121ad9edmsh28a3e1ba931dcf9p10b968jsnd61824ad3d31",
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None
