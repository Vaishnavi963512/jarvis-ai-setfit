

https://github.com/user-attachments/assets/4cbd97bc-3dbf-459d-a199-0a8e531909ad

# 🤖 Jarvis AI Assistant with SetFit Emotion Detection

## 🚀 Overview

This project is an intelligent **AI Assistant (Jarvis)** built using **Streamlit**, capable of understanding user input, detecting emotions using **SetFit (Deep Learning)**, and generating smart responses using an LLM.

It supports **voice input**, **text-to-speech output**, and **agent-based decision making**.

---

## ✨ Features

* 🧠 Emotion Detection using **SetFit (HuggingFace)**
* 🎤 Voice Input (Speech Recognition)
* 🔊 Text-to-Speech Response (gTTS)
* 🤖 LLM Integration (Groq API)
* 🧩 Agent-based Routing (Emotion / Tools / LLM)
* 🎨 Interactive UI using Streamlit

---

## 🛠️ Tech Stack

* Python
* Streamlit
* SetFit
* PyTorch
* Sentence Transformers
* SpeechRecognition
* gTTS
* Groq API

---

## 📂 Project Structure

```
voice-ai-pro/
│
├── app.py          # Streamlit UI
├── agent.py        # Decision logic (routes tasks)
├── predict.py      # Emotion detection using SetFit
├── train.py        # Model training script
├── requirements.txt
└── model/          # Trained SetFit model
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Vaishnavi963512/jarvis-ai-setfit.git
cd jarvis-ai-setfit
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the model (only first time)

```bash
python train.py
```

### 5. Run the application

```bash
streamlit run app.py
```

---

## 💡 Example Inputs

* "I am very happy today"
* "I feel sad and lonely"
* "I am angry"
* "What is the time?"

---

## 🧠 How It Works

1. User gives input (text or voice)
2. Agent analyzes input
3. If emotion detected → SetFit model predicts emotion
4. If tool request → executes utility (e.g., time)
5. Otherwise → LLM generates response
6. Output is displayed and spoken using TTS

---

## ⚠️ Notes

* The model is trained on a small custom dataset (demo purpose)
* You can extend dataset for better accuracy
* Requires internet for LLM API (Groq)

---

## 📌 Future Improvements

* Add more emotions and larger dataset
* Improve UI/UX with animations
* Add multi-language support
* Deploy on cloud (Streamlit Cloud / Render)

---

## 👩‍💻 Author

**Vaishnavi Brundavanam**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub
