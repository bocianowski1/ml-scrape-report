# https://platform.openai.com/docs/api-reference/completions/create

import os
import openai


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