import librosa
import numpy as np

def analyze_voice(audio_file):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=None)
    
    # Extract fundamental frequency using librosa's yin function
    # Set minimum and maximum frequencies for human speech
    fmin = librosa.note_to_hz('C2')  # Lower limit of the pitch (about 65 Hz)
    fmax = librosa.note_to_hz('C7')  # Upper limit of the pitch (about 2093 Hz)
    
    f0 = librosa.yin(y, fmin=fmin, fmax=fmax, sr=sr)

    # Compute average pitch (median) to avoid outliers
    pitch = np.median(f0)
    
    # Calculate the root mean square energy for volume level
    volume = np.mean(librosa.feature.rms(y=y)) * 1000
    
    print(f"Pitch: {pitch} Hz")
    print(f"Volume: {volume}")

    return {
        "pitch": pitch,
        "volume": volume
    }
