import json
import csv 

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
        }
        rows.append(data)

    header = ["title", "url"]

    with open("open_coding.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)   

def main(): 
    filename1 = "zohran_mamdani_articles_0814-1013.json"
    filename2 = "zohran_mamdani_articles_1014-1115.json"
    get_article_information(read_json(filename1), 100) 
    get_article_information(read_json(filename2), 100) 

if __name__ == "__main__": 
    main() 
    