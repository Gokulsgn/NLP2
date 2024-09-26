import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import streamlit_audiorec as audiorec

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

# Speech-to-Text function
def speech_to_text(audio_data):
    recognizer = sr.Recognizer()
    audio_bytes = audio_data.get_wav_data()
    audio_file = sr.AudioFile(BytesIO(audio_bytes))

    with audio_file as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the audio.")
        except sr.RequestError as e:
            st.error(f"Error connecting to the speech recognition service: {e}")

# Text-to-Speech function
def text_to_speech(text):
    if text:
        tts = gTTS(text=text, lang='en')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format="audio/mp3")

# Streamlit app layout
st.title("Speech-to-Text and Text-to-Speech App")

# Select mode
mode = st.selectbox("Choose a mode", ["Speech-to-Text", "Text-to-Speech"])

# Speech-to-Text Mode
if mode == "Speech-to-Text":
    st.header("Convert Speech to Text")
    audio_data = audiorec.record(text="Press to start recording", sampling_rate=16000)
    if audio_data is not None:
        speech_to_text(audio_data)

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
