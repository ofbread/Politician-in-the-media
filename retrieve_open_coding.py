import json
import csv 
import pandas as pd

def read_json(filename): 
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data["articles"]

def get_article_information(articles, article_number):

    rows = []

    for x in range(article_number):
        data = {
            "title": articles[x]["title"],
            "url": articles[x]["url"],
            "description" : articles[x]["description"], 
            "snippet": articles[x]["snippet"],
        }
        rows.append(data)

    header = ["title", "url", "description", "snippet"]

    with open("open_coding.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)   

def main(): 
    filename1 = "zohran_mamdani_articles_0101-1118_Left.json"
    filename2 = "zohran_mamdani_articles_0101-1118_Right.json"
    get_article_information(read_json(filename1), 250) 
    get_article_information(read_json(filename2), 250) 
     
    # df = pd.read_csv("open_coding.csv")
    # df.to_excel("open_coding.xlsx", index=False)


if __name__ == "__main__": 
    main() 
    