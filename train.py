from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments

# Training data
data = {
    "text": [
        # HAPPY
        "I feel amazing today",
        "This is the best day ever",
        "I am very happy",
        "Life is beautiful",

        # SAD
        "I feel very sad",
        "I am feeling down",
        "Today is not good",
        "I feel lonely",

        # ANGRY
        "This is frustrating",
        "I am very angry",
        "This makes me mad",
        "I hate this situation",

        # CALM
        "I feel peaceful",
        "I am relaxed",
        "Everything is calm",
        "I feel balanced",

        # EXCITED
        "I am so excited",
        "This is thrilling",
        "I can't wait for this",
        "This is awesome"
    ],
    "label": [
        0, 0, 0, 0,   # happy
        1, 1, 1, 1,   # sad
        2, 2, 2, 2,   # angry
        3, 3, 3, 3,   # calm
        4, 4, 4, 4    # excited
    ]
}

dataset = Dataset.from_dict(data)

model = SetFitModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

args = TrainingArguments(
    batch_size=4,
    num_epochs=1,
    num_iterations=20,
    output_dir="setfit-output",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset,
    column_mapping={"text": "text", "label": "label"}
)

trainer.train()
model.save_pretrained("model")

print("Model trained and saved successfully")