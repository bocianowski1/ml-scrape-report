import pandas as pd
from utils.visualize import *


df = pd.read_csv("data/test_data/rtps.csv", sep=",")

create_piechart(df.head(8), "% Chg", "Sector", "sectors.png", title="Sectors", show_plot=True)
