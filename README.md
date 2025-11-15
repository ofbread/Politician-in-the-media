# News Article Collector

A Python script to collect a total of 600 news articles about Zohran Mamdani from North American news outlets using The News API.

### `collect_articles.py`
Main Python script that collects articles from The News API. 

### `news_outlets.json`
Configuration file containing a list of North American news outlets. Each outlet entry includes:
- `name`: News outlet name
- `domain`: Website domain (used for API filtering)
- `bias`: Political bias classification (Left/Center/Right)
- `country`: Country (USA/Canada)

The script uses these domains to filter articles from specific news sources.

### Output JSON Files
Generated article files named in the format:
- `zohran_mamdani_articles_MMDD-MMDD.json`

Each file contains 300 articles
Where `MMDD-MMDD` represents the date range (e.g., `0814-1013` for August 14 to October 13, 2025).



