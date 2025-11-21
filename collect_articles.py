import requests
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NEWS_OUTLETS_FILE = "news_outlets.json"

def load_domains_from_outlets(bias: str = None, filename: str = NEWS_OUTLETS_FILE):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    outlets = data.get("outlets", [])
    outlets = [outlet for outlet in outlets if outlet.get("bias") == bias]
    domains = [outlet.get("domain") for outlet in outlets if outlet.get("domain")]
    print(f"Loaded {len(domains)} domains from {filename}" + (f" (bias: {bias})" if bias else ""))
    return domains


class NewsAPICollector:
    
    BASE_URL = "https://api.thenewsapi.com/v1/news/all"
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = requests.Session()
        self.articles = []
        self.published_after = None
        self.published_before = None
        self.bias = None
        
    def fetch_articles_page(self, search_term: str, domains: list[str],
                           language: str = "en", limit: int = 25, 
                           page: int = 1):
        params = {
            "api_token": self.api_token,
            "search": search_term,
            "published_before": self.published_before,
            "published_after": self.published_after,
            "domains": ",".join(domains),
            "language": language,
            "limit": limit,
            "page": page
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def collect_articles(self, search_term: str, target_count: int = 170,
                        language: str = "en", limit: int = 25, 
                        delay: float = 1.0,
                        published_after: str = "2025-01-01",
                        published_before: str = "2025-11-18",
                        bias: str = None):
        self.articles = []
        self.published_after = published_after
        self.published_before = published_before
        self.bias = bias
        page = 1
        total_collected = 0
        
        print(f"Starting collection of {target_count} articles about '{search_term}'...")
        print("-" * 60)
        
        domains = load_domains_from_outlets(bias=bias)
        
        time.sleep(delay)
        
        while total_collected < target_count:
            print(f"Fetching page {page}...", end=" ")
            
            data = self.fetch_articles_page(
                search_term=search_term,
                domains=domains,
                language=language,
                limit=limit,
                page=page
            )
            
            if not data:
                print("Failed to fetch page")
                break
            
            articles_in_page = data.get("data", [])
            
            if not articles_in_page:
                print(f"No more articles found (collected {total_collected} so far)")
                break
            
            for article in articles_in_page:
                if total_collected >= target_count:
                    break
                self.articles.append(article)
                total_collected += 1
            
            print(f"Collected {len(articles_in_page)} articles (Total: {total_collected}/{target_count})")
            
            if total_collected >= target_count:
                break
            
            meta = data.get("meta", {})
            found = meta.get("found", 0)
            
            if total_collected >= found:
                print(f"Reached end of available articles (found: {found})")
                break
            
            page += 1
            
            time.sleep(delay)
        
        return self.articles
    
    def save_to_json(self, filename: str = None):
        if not filename:
            if self.published_after and self.published_before:
                after_date = datetime.strptime(self.published_after, "%Y-%m-%d")
                before_date = datetime.strptime(self.published_before, "%Y-%m-%d")
                after_str = after_date.strftime("%m%d")
                before_str = before_date.strftime("%m%d")
                bias_suffix = f"_{self.bias}" 
                filename = f"zohran_mamdani_articles_{after_str}-{before_str}{bias_suffix}.json"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"zohran_mamdani_articles_{timestamp}.json"
        
        output = {
            "metadata": {
                "search_term": "Zohran Mamdani",
                "total_articles": len(self.articles),
                "collection_date": datetime.now().isoformat(),
                "locale": "us,ca",
                "language": "en"
            },
            "articles": self.articles
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return filename
    

def main():
    api_token = os.getenv("NEWS_API_TOKEN")
    
    collector = NewsAPICollector(api_token)
    
    articles = collector.collect_articles(
        search_term="Zohran Mamdani",
        target_count=250,
        language="en",
        limit=25,
        delay=1.0,
        bias="Right"
    )
    
    if articles:
        json_file = collector.save_to_json()
        
        print(f"\nSummary:")
        print(f"- Total articles collected: {len(articles)}")
        print(f"- JSON file: {json_file}")
        
        if articles:
            print(f"\nSample article:")
            sample = articles[0]
            print(f"  Title: {sample.get('title', 'N/A')}")
            print(f"  Source: {sample.get('source', 'N/A')}")
            print(f"  Published: {sample.get('published_at', 'N/A')}")
            print(f"  URL: {sample.get('url', 'N/A')}")
        
    else:
        print("No articles were collected")


if __name__ == "__main__":
    main()


