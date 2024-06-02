from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax

# Load the pre-trained tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('gooohjy/suicidal-electra')
model = AutoModelForSequenceClassification.from_pretrained('gooohjy/suicidal-electra', num_labels=2)

# Define a function to predict the class label for a given text
def predict_class(text):
    # Prepare the input tensors
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Perform inference using the model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

    # Calculate the softmax probabilities for the output logits
    scores = softmax(logits[0].detach().numpy(), axis=0)

    # Map class index to label
    class_labels = ["non-suicidal", "suicidal"]
    class_probs = {label: float(score) for label, score in zip(class_labels, scores)}

    # Return the predicted class label and scores
    return predicted_class, class_probs
