import os
from openbb_terminal.sdk import openbb
import pandas as pd


def login() -> None:
    print("Logging in...")
    try:
        openbb.login("pelagianalytics@gmail.com", os.environ.get("OPENBB_PASSWORD"))
    except:
        print("Login failed. Please check your credentials and try again.")

def logout() -> None:
    print("Logging out...")
    openbb.logout()

def get_indices() -> pd.DataFrame:
    indices = openbb.economy.indices()
    indices.rename(columns={" ": "Name"}, inplace=True)
    return indices

def get_economy_events() -> pd.DataFrame:
    return openbb.economy.events()

def get_performance_sectors() -> pd.DataFrame:
    return openbb.economy.rtps()

def get_news(about: str) -> pd.DataFrame:
    df = openbb.news(str(about))
    return df