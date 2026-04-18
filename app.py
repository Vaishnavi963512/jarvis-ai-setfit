import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import requests
import uuid
from agent import run_agent

# ---------------- CONFIG ----------------
st.set_page_config(page_title="JARVIS AI", layout="wide")

UNSPLASH_KEY = "LqMACiaTdEZP-yPPrPb8hR89W_OmxEhDp6oIuIAwkxs"

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
    stop = ["what","is","the","about","tell","me","hi","i","am"]
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
        res = requests.get(url, params=params).json()

        if "urls" in res:
            return res["urls"]["regular"]

    except:
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
    text-align:center;
    font-size:40px;
    color:#00f7ff;
}}

.chat {{
    max-width:700px;
    margin:30px auto;
    background: rgba(0,0,0,0.7);
    padding:20px;
    border-radius:10px;
    color:white;
    text-align:center;
}}

.mode {{
    text-align:center;
    font-size:20px;
    color:yellow;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🤖 JARVIS AI</div>", unsafe_allow_html=True)

# ---------------- MODE ----------------
if st.session_state.mode:
    st.markdown(f"<div class='mode'>⚡ Mode: {st.session_state.mode}</div>", unsafe_allow_html=True)

# ---------------- CHAT ----------------
if st.session_state.last_user:
    st.markdown(f"""
    <div class='chat'>
        <b>You:</b> {st.session_state.last_user}<br><br>
        <b>Jarvis:</b> {st.session_state.last_bot}
    </div>
    """, unsafe_allow_html=True)

# ---------------- AUDIO ----------------
if st.session_state.audio_file:
    st.audio(st.session_state.audio_file)

# ---------------- VOICE ----------------
def listen():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening...")
            audio = r.listen(source, timeout=5)
        return r.recognize_google(audio)
    except:
        return ""

# ---------------- TTS ----------------
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    gTTS(text=text).save(filename)
    return filename

# ---------------- INPUT ----------------
col1, col2, col3 = st.columns([6,1,1])

text_input = col1.text_input("Ask...", label_visibility="collapsed")
send = col2.button("➤")
mic = col3.button("🎤")

# ---------------- PROCESS ----------------
def process_query(query):
    with st.spinner("🤖 Thinking..."):
        answer, keyword, mode = run_agent(query)

    # Save
    st.session_state.last_user = query
    st.session_state.last_bot = answer
    st.session_state.mode = mode

    # Background
    search = extract_keyword(query)
    st.session_state.bg_url = get_background(search)

    # Voice
    st.session_state.audio_file = speak(answer)

# TEXT INPUT
if send and text_input:
    process_query(text_input)
    st.rerun()

# VOICE INPUT (FIXED)
if mic:
    voice = listen()
    if voice:
        process_query(voice)
        st.rerun()