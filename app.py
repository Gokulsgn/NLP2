import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64

# Sidebar for settings
st.sidebar.title("Settings")
dark_mode = st.sidebar.checkbox("Enable Dark Mode")

# Custom CSS for light and dark modes
def set_background_color(dark_mode):
    if dark_mode:
        st.markdown("""
            <style>
                body {
                    background-color: #2e3b4e;
                    color: white;
                }
                .stButton > button {
                    background-color: #27B7A6;
                    color: white;
                    border-radius: 5px;
                }
                .stTextArea {
                    background-color: #2e3b4e;
                    color: white;
                    border: 1px solid #4a4f54;
                    border-radius: 5px;
                }
                h1, h2, h3, h4 {
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                body {
                    background-color: #f0f4f8;
                }
                .stButton > button {
                    background-color: #27B7A6;
                    color: white;
                    border-radius: 5px;
                }
                .stTextArea {
                    background-color: #fff;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                h1, h2, h3, h4 {
                    color: black;
                }
            </style>
        """, unsafe_allow_html=True)

# Apply the selected background color scheme
set_background_color(dark_mode)

# Speech-to-Text function using live microphone input
def live_speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            st.info("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source)
            st.info("Listening for speech...")
            audio = recognizer.listen(source)

            st.info("Processing speech...")

            try:
                # Convert speech to text using Google's speech recognition
                text = recognizer.recognize_google(audio)
                st.success(f"You said: {text}")
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
            except sr.RequestError as e:
                st.error(f"Error connecting to the speech recognition service: {e}")
    except OSError:
        st.error("Microphone not found or audio input not supported in this environment.")

# Text-to-Speech function (Using BytesIO to avoid saving files directly)
def text_to_speech(text, language):
    if text:
        tts = gTTS(text=text, lang=language)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        # Play audio in Streamlit
        st.audio(audio_bytes, format="audio/mp3")
        
        # Downloadable speech file
        b64 = base64.b64encode(audio_bytes.read()).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="speech.mp3">Download Speech</a>'
        st.markdown(href, unsafe_allow_html=True)

# Streamlit app layout
st.title("Live Speech-to-Text and Text-to-Speech App 🎤")

# Select mode
mode = st.selectbox("Choose a mode", ["Live Speech-to-Text", "Text-to-Speech"])

# Live Speech-to-Text Mode
if mode == "Live Speech-to-Text":
    st.header("Convert Live Speech to Text")
    
    if st.button("Start Listening"):
        with st.spinner("Listening..."):
            live_speech_to_text()

# Text-to-Speech Mode with language selection
if mode == "Text-to-Speech":
    st.header("Convert Text to Speech")
    user_input = st.text_area("Enter text to convert into speech:")
    
    # Select language for Text-to-Speech
    language = st.selectbox("Choose language for speech", 
                            ["English (en)", "Spanish (es)", "French (fr)", "German (de)", "Chinese (zh-CN)"])
    
    language_code = language.split(" ")[-1].strip('()')

    if st.button("Convert to Speech"):
        if user_input.strip():
            with st.spinner("Converting..."):
                text_to_speech(user_input, language_code)
        else:
            st.warning("Please enter some text to convert into speech.")

# Footer section
st.markdown("---")
st.markdown("Developed by [Gokulnath S](https://github.com/Gokulsgn/NLP2)")
st.markdown("🔊 Enhance your text and audio experiences!")
