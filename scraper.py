import httpx
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def fetch_articles(category="general"):
    """Fetch Kenya-related articles from NewsAPI and save to database."""

    category_keywords = {
        "business": "Kenya business OR Nairobi stocks OR NSE",
        "technology": "Kenya technology OR Nairobi tech",
        "sports": "Kenya sports OR Kenyan athletes",
        "health": "Kenya health OR Nairobi hospital",
        "general": "Kenya news OR Nairobi"
    }

    keyword = category_keywords.get(category, "Kenya news")

    params = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    try:
        response = httpx.get(BASE_URL, params=params)
        data = response.json()

        if data["status"] != "ok":
            print(f"NewsAPI error: {data['message']}")
            return []

        # Save articles to the database
        save_articles(data["articles"], category)

        return data["articles"]

    except Exception as e:
        print(f"Failed to fetch articles: {e}")
        return []


def save_articles(articles, category):
    """Save fetched articles to the database, skipping duplicates."""
    from database import db
    from models import Article

    try:
        saved = 0
        for item in articles:
            if not item.get("title") or not item.get("url"):
                continue
            exists = Article.query.filter_by(url=item["url"]).first()
            if exists:
                continue

            published_at = None
            if item.get("publishedAt"):
                published_at = datetime.strptime(
                    item["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )

            article = Article(
                title=item.get("title", "No title"),
                description=item.get("description", ""),
                url=item["url"],
                category=category,
                source=item.get("source", {}).get("name", "Unknown"),
                published_at=published_at
            )

            db.session.add(article)
            saved += 1

        db.session.commit()
        print(f"Saved {saved} new articles to the database")

    except Exception as e:
        db.session.rollback()
        print(f"Error saving articles: {e}")