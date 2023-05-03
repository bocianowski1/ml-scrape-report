import matplotlib.pyplot as plt
import pandas as pd

from utils.constants import *

def create_lineplot(df: pd.DataFrame, x_column: str, y_column: str, title: str, 
                       xlabel: str = None, ylabel: str = None, show_plot: bool = False, save_plot: bool = True):
    
    _, ax = plt.subplots()
    ax.plot(df[x_column].values, df[y_column].values, color=colors_dict["Main Blue"]) 
    ax.set_title(title, fontweight="bold")
    ax.set_xticklabels(df[x_column].values, rotation=90)
    plt.xticks(df[x_column].values)

    if ylabel:
        ax.set_ylabel(ylabel) 
    if xlabel:
        ax.set_xlabel(xlabel)

    if save_plot:
        plt.savefig("images/plot.png", dpi=300, bbox_inches="tight", pad_inches=0)
    
    if show_plot:
        plt.show()


def create_piechart(df: pd.DataFrame, x_column: str, y_column: str, title: str, 
                       xlabel: str = None, ylabel: str = None, show_plot: bool = False, save_plot: bool = True):
    
    _, ax = plt.subplots()
    ax.pie(x=df[x_column], labels=df[y_column], autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis("equal")
    ax.set_title(title, fontweight="bold")
    
    if save_plot:
        plt.savefig("images/plot.png", dpi=300, bbox_inches="tight", pad_inches=0)

    if show_plot:
        plt.show()

