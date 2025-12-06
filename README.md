# Across the Spectrum: Zohran Mamdani’s Media Coverage 

Collection of articles on Zohran Mamdani and tf-idf scores in each category of the annotated data.

### `scripts/collect_articles.py`
Main Python script that collects articles from The News API. 

### `scripts/news_outlets.json`
Configuration file containing a list of North American news outlets. Each outlet entry includes:
- `name`: News outlet name
- `domain`: Website domain (used for API filtering)
- `bias`: Political bias classification (Left/Center/Right)
- `country`: Country (USA/Canada)

The script uses these domains to filter articles from specific news sources.

### Output JSON Files
Generated article files named in the format:
- `data/zohran_mamdani_articles_MMDD-MMDD_X.json`

Where `MMDD-MMDD` represents the date range (e.g., `0814-1013` for August 14 to October 13, 2025), `X` represents the political orientation of the articles. 

Each file contains 250 articles.

### `scripts/json_to_csv.py`
Converts collected raw data to csv files ready for annotation.

### `scripts/tf_idf.py`
Computes the tf-idf scores for each category.




