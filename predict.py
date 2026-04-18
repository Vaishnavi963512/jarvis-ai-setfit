from setfit import SetFitModel

model = SetFitModel.from_pretrained("model")

labels = {
    0: "happy",
    1: "sad",
    2: "angry",
    3: "calm",
    4: "excited"
}

def predict_emotion(text):
    pred = model.predict([text])[0]
    return labels[int(pred)]