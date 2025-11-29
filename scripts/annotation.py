import pandas as pd 
import re

def get_outlet(url): 
    news_url = url.split("/")
    clean_news_url = re.sub(r'^www\.', '', news_url[2])
    return clean_news_url

political_map = {
    "cbc.ca": "Left-Center",
    "theatlantic.com": "Left-Center",
    "newyorker.com": "Left",
    "washingtonpost.com": "Left-Center",
    "msnbc.com": "Left",
    "nytimes.com": "Left-Center",
    "vox.com": "Left",
    "rollingstone.com": "Left",
    "apnews.com": "Left-Center",
    "nypost.com": "Right-Center",
    "washingtontimes.com": "Right-Center",
    "foxnews.com": "Right"
}

csv_path = "./annotated_dataset.csv"

df = pd.read_csv(csv_path)

df["News Outlet"] = df["URL"].apply(get_outlet)

df["Political Stance"] = df["News Outlet"].map(political_map)

df = df.drop("Note", axis=1)

df.to_csv("final_dataset.csv", index=False)