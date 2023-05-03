import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

from data.helpers import random_id

def preprocess_text(text: str) -> str:
    words = []
    for word in text.split(" "):
        if word.startswith("@") and len(word) > 1:
            word = "@user"
        if word.startswith("http"):
            word = "http"
        words.append(word)
    return " ".join(words)

def get_sentiment(text: str, max_prob_only: bool = True) -> dict[str, float]:
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    labels = ["Negative", "Neutral", "Positive"]

    encoded_text = tokenizer(preprocess_text(text), return_tensors="pt")
    output = model(**encoded_text)

    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    if max_prob_only:
        return {labels[scores.argmax()]: scores.max()}
    else:
        return {labels[i]: scores[i] for i in range(len(scores))}
    
def get_prediction_label(text: str) -> str:
    return list(get_sentiment(text).keys())[0]

def get_prediction_score(text: str) -> float:
    return list(get_sentiment(text).values())[0]

def analyze_dataframe(df: pd.DataFrame, content: str, save_df: bool = False) -> None:
    df["Sentiment"] = [get_prediction_label(text) for text in df[content]]
    df["Confidence"] = [get_prediction_score(text) for text in df[content]]
    if save_df:
        df.to_csv(f"sentiment-{random_id()}.csv", index=False)

