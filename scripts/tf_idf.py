import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

csv_file = "dataset_final.csv"
stop_words_file = "stop_words.txt"

# Load stop words from file
with open(stop_words_file, "r", encoding="utf-8") as f:
    stop_words = f.read().splitlines()

# Load the CSV file
df = pd.read_csv(csv_file)

# 1. Combine text fields into one column
df['Content'] = (
    df['Title'].fillna('') + ' ' +
    df['Description'].fillna('') + ' ' +
    df['Snippet'].fillna('')
)


# 2. Group by category -> one big doc per category
cat_text = df.groupby('Type')['Content'].apply(lambda x: ' '.join(x))

# cat_text is a Series: index = category, value = big text string
categories = cat_text.index.tolist()

# 3. Compute TF-IDF over these category-documents
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),       # unigrams + bigrams (optional)
    stop_words=stop_words      # drop "the", "and", etc
)

X = vectorizer.fit_transform(cat_text)  # shape: (num_categories, num_terms)
terms = vectorizer.get_feature_names_out()


def top_terms_for_category(cat_index, top_n=20):
    row = X[cat_index].toarray().ravel()
    top_idx = row.argsort()[::-1][:top_n]
    return list(zip(terms[top_idx], row[top_idx]))

# Example: print top 20 words for each category
for i, cat in enumerate(categories):
    print(f"\n=== {cat} ===")
    for term, score in top_terms_for_category(i, top_n=10):
        print(f"{term:25s} {score:.4f}")