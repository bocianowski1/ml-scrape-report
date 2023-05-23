from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import openai
import torch
import pandas as pd
import os
from typing import Tuple

from ..utils.constants import CSV_PATH
from ..utils.helpers import random_id
from preprocessing import preprocess_text


def load_model() -> Tuple[AutoModelForSequenceClassification, AutoTokenizer, list[str]]:
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    labels = ["Negative", "Neutral", "Positive"]
    return model, tokenizer, labels

def get_sentiment(text: str, model, tokenizer, labels) -> Tuple[str, float]:
    encoded_text = tokenizer(preprocess_text(text), return_tensors="pt")
    output = model(**encoded_text)

    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)

    return labels[scores.argmax()], scores.max()

def analyze_dataframe(df: pd.DataFrame, content: str, model, tokenizer, labels, save_df: bool = False) -> None:
    texts = df[content].tolist()

    sentiments = []
    confidences = []

    batch_size = 32
    for i in range(0, len(texts), batch_size):
        print(f"{i}/{len(texts)}")
        batch_texts = texts[i:i+batch_size]
        encoded_texts = tokenizer.batch_encode_plus(
            batch_texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        )
        outputs = model(**encoded_texts)
        logits = outputs.logits

        batch_scores = softmax(logits, axis=1)
        batch_preds = torch.argmax(batch_scores, dim=1)

        for j, pred in enumerate(batch_preds):
            print(f"{j}/{len(batch_preds)}")
            sentiment = labels[pred]
            confidence = batch_scores[j][pred].item()
            sentiments.append(sentiment)
            confidences.append(confidence)

    df["Sentiment"] = sentiments
    df["Confidence"] = confidences

    if save_df:
        df.to_csv(f"{CSV_PATH}/sentiment-{random_id()}.csv", index=False)

class Term:
    SHORT = "short"
    LONG = "long"

def create_sentiment_prompt(headline: str, company_name: str, term: str = Term.SHORT) -> str:
    return f"""
        Forget all your previous instructions. Pretend you are a financial expert. 
        You are a financial expert with stock recommendation experience. 
        Answer “YES” if good news, “NO” if bad news, or “UNKNOWN” if uncertain in the first line. 
        Then elaborate with one short and concise sentence on the next line. 
        Is this headline good or bad for the stock price of {company_name} in the {term} term?
        Headline: {headline}
    """

def create_response(prompt: str) -> str:
    if len(prompt) > 2048:
        return "ERROR: Prompt too long. Max length is 2048."
    if len(prompt) < 1:
        return "ERROR: Prompt too short. Min length is 1."
    if os.environ.get("OPENAI_API_KEY") is None:
        return "ERROR: No OpenAI API key found."
    
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    try:
        response = openai.Completion.create(
            model="text-davinci-003", # gpt-3.5-turbo
            prompt=prompt,
            temperature=0,
        )
        return response["choices"][0]["text"]
    except Exception as e:
        return f"ERROR: {e}"

# For testing
headline = "Rimini Street Fined $630,000 in Case Against Oracle"
company_name = "Oracle"

# prompt = create_sentiment_prompt(headline, company_name)
# response = create_response(prompt)
# print(response)