import streamlit as st
from gtts import gTTS
import requests
import uuid
import tempfile
import speech_recognition as sr
from agent import run_agent

# ---------------- CONFIG ----------------
st.set_page_config(page_title="JARVIS AI", layout="wide")

UNSPLASH_KEY = "YOUR_UNSPLASH_KEY_HERE"

# ---------------- SESSION ----------------
if "last_user" not in st.session_state:
    st.session_state.last_user = ""

if "last_bot" not in st.session_state:
    st.session_state.last_bot = ""

if "mode" not in st.session_state:
    st.session_state.mode = ""

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

if "bg_url" not in st.session_state:
    st.session_state.bg_url = "https://images.unsplash.com/photo-1502082553048-f009c37129b9"

# ---------------- KEYWORD ----------------
def extract_keyword(text):
    words = text.lower().split()
    stop = ["what", "is", "the", "about", "tell", "me", "hi", "i", "am"]
    words = [w for w in words if w not in stop]
    return " ".join(words[:2]) if words else text

# ---------------- UNSPLASH ----------------
def get_background(query):
    try:
        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": query,
            "orientation": "landscape",
            "client_id": UNSPLASH_KEY
        }
        res = requests.get(url, params=params, timeout=10).json()

        if "urls" in res:
            return res["urls"]["regular"]
    except Exception:
        pass

    return st.session_state.bg_url

# ---------------- APPLY BACKGROUND ----------------
st.markdown(f"""
<style>
.stApp {{
    background-image: url("{st.session_state.bg_url}");
    background-size: cover;
    background-position: center;
}}

.title {{
    text-align: center;
    font-size: 40px;
    color: #00f7ff;
}}

.chat {{
    max-width: 700px;
    margin: 30px auto;
    background: rgba(0,0,0,0.7);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
}}

.mode {{
    text-align: center;
    font-size: 20px;
    color: yellow;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🤖 JARVIS AI</div>", unsafe_allow_html=True)

# ---------------- MODE ----------------
if st.session_state.mode:
    st.markdown(
        f"<div class='mode'>⚡ Mode: {st.session_state.mode}</div>",
        unsafe_allow_html=True
    )

# ---------------- CHAT ----------------
if st.session_state.last_user:
    st.markdown(f"""
    <div class='chat'>
        <b>You:</b> {st.session_state.last_user}<br><br>
        <b>Jarvis:</b> {st.session_state.last_bot}
    </div>
    """, unsafe_allow_html=True)

# ---------------- AUDIO OUTPUT ----------------
if st.session_state.audio_file:
    st.audio(st.session_state.audio_file)

# ---------------- TTS ----------------
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    gTTS(text=text).save(filename)
    return filename

# ---------------- STT FROM AUDIO FILE ----------------
def transcribe_audio_file(audio_bytes):
    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        temp_path = tmp.name

    try:
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except Exception:
        return ""

# ---------------- PROCESS ----------------
def process_query(query):
    with st.spinner("🤖 Thinking..."):
        answer, keyword, mode = run_agent(query)

    st.session_state.last_user = query
    st.session_state.last_bot = answer
    st.session_state.mode = mode

    search = extract_keyword(query)
    st.session_state.bg_url = get_background(search)

    st.session_state.audio_file = speak(answer)

# ---------------- TEXT INPUT ----------------
col1, col2 = st.columns([8, 1])

text_input = col1.text_input("Ask...", label_visibility="collapsed")
send = col2.button("➤")

if send and text_input.strip():
    process_query(text_input.strip())
    st.rerun()

# ---------------- VOICE INPUT USING BROWSER MIC ----------------
st.markdown("### 🎤 Speak to Jarvis")
audio_value = st.audio_input("Record your voice")

if audio_value is not None:
    st.audio(audio_value)

    voice_text = transcribe_audio_file(audio_value.read())

    if voice_text:
        st.success(f"You said: {voice_text}")
        process_query(voice_text)
        st.rerun()
    else:
        st.error("Could not understand the audio. Please try again.")
