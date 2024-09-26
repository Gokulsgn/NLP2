import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from gtts import gTTS
from io import BytesIO

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
        }
        .stButton > button {
            background-color: #27B7A6; /* Green */
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #27B7A6;
        }
        .stTextArea {
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Speech-to-Text function using sounddevice for recording
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        fs = 44100  # Sample rate
        duration = 5  # Duration in seconds
        st.info("Recording for 5 seconds...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until the recording is finished
        write('output.wav', fs, recording)  # Save as WAV file

        # Now use SpeechRecognition to process the WAV file
        with sr.AudioFile('output.wav') as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                st.success(f"You said: {text}")
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
            except sr.RequestError as e:
                st.error(f"Error connecting to the speech recognition service: {e}")
    except OSError:
        st.error("Microphone not found. Please ensure your device has a microphone or you have the required permissions.")

# Text-to-Speech function (Using BytesIO to avoid saving files directly)
def text_to_speech(text):
    if text:
        tts = gTTS(text=text, lang='en')
        audio_bytes = BytesIO()  # Create a BytesIO object to hold the audio
        tts.write_to_fp(audio_bytes)  # Write audio to BytesIO object
        audio_bytes.seek(0)  # Move cursor to the start of the BytesIO object
        st.audio(audio_bytes, format="audio/mp3")

# Streamlit app layout
st.title("Speech-to-Text and Text-to-Speech App")

# Select mode
mode = st.selectbox("Choose a mode", ["Speech-to-Text", "Text-to-Speech"])

# Speech-to-Text Mode
if mode == "Speech-to-Text":
    st.header("Convert Speech to Text")
    if st.button("Start Recording"):
        with st.spinner("Listening..."):
            speech_to_text()

# Text-to-Speech Mode
if mode == "Text-to-Speech":
    st.header("Convert Text to Speech")
    user_input = st.text_area("Enter text to convert into speech:")
    if st.button("Convert to Speech"):
        if user_input.strip():  # Check if user entered something
            with st.spinner("Converting..."):
                text_to_speech(user_input)
        else:
            st.warning("Please enter some text to convert into speech.")
