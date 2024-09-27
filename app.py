import streamlit as st
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
st.title("Text-to-Speech App 🎤")

# Text-to-Speech Mode with language selection
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
