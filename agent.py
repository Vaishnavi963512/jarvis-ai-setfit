import requests
import datetime
from predict import predict_emotion

GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"

def run_agent(user_input):
    print("\n==============================")
    print("[AGENT INPUT]:", user_input)

    text = user_input.lower()

    # ---------------- EMOTION (SETFIT) ----------------
    emotion_trigger_words = [
        "happy", "sad", "angry", "excited", "calm",
        "good", "bad", "upset", "frustrated", "peaceful",
        "relaxed", "lonely", "mad", "amazing", "awesome",
        "depressed", "hurt", "glad", "thrilled", "annoyed"
    ]

    if any(word in text for word in emotion_trigger_words):
        print("[AGENT] USING: SETFIT")

        emotion = predict_emotion(user_input)

        responses = {
            "happy": "That's wonderful 😊 Keep smiling!",
            "sad": "Stay strong 💙 Everything will be okay.",
            "angry": "Take a deep breath 🔥 You got this.",
            "excited": "That's awesome 🚀 Keep the energy!",
            "calm": "Stay peaceful 🌿"
        }

        return responses.get(emotion, "You're doing great"), emotion, "SETFIT"

    # ---------------- TOOL ----------------
    elif "time" in text:
        print("[AGENT] USING: TOOL")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"Current time is {current_time}", "clock", "TOOL"

    # ---------------- LLM ----------------
    else:
        print("[AGENT] USING: LLM")

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            answer = data["choices"][0]["message"]["content"]
            return answer, "general", "LLM"

        except Exception as e:
            print("[ERROR]:", e)
            return "Error getting AI response", "general", "LLM"