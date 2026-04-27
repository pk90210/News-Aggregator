from flask import Flask, jsonify, request
from dotenv import load_dotenv
from scraper import fetch_articles
from database import db, init_db
from scheduler import start_scheduler
import os

load_dotenv()

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
init_db(app)

# Start the background scheduler
scheduler = start_scheduler(app)


@app.route("/news", methods=["GET"])
def get_news():
    from models import Article

    category = request.args.get("category", "general")

    fetch_articles(category)

    if category == "general":
        articles = Article.query.order_by(Article.published_at.desc()).limit(20).all()
    else:
        articles = Article.query.filter_by(category=category)\
                                .order_by(Article.published_at.desc())\
                                .limit(20).all()

    result = []
    for article in articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "url": article.url,
            "source": article.source,
            "category": article.category,
            "published_at": article.published_at.isoformat() if article.published_at else None
        })

    return jsonify({
        "category": category,
        "total": len(result),
        "articles": result
    })


@app.route("/news/search", methods=["GET"])
def search_news():
    from models import Article, SearchLog
    from database import db

    keyword = request.args.get("q", "")

    if not keyword:
        return jsonify({"error": "Please provide a search keyword e.g. /news/search?q=NSE"}), 400

    articles = Article.query.filter(
        db.or_(
            Article.title.ilike(f"%{keyword}%"),
            Article.description.ilike(f"%{keyword}%")
        )
    ).order_by(Article.published_at.desc()).limit(20).all()

    log = SearchLog(keyword=keyword.lower())
    db.session.add(log)
    db.session.commit()

    result = []
    for article in articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "url": article.url,
            "source": article.source,
            "category": article.category,
            "published_at": article.published_at.isoformat() if article.published_at else None
        })

    return jsonify({
        "keyword": keyword,
        "total": len(result),
        "articles": result
    })


@app.route("/subscriptions", methods=["POST"])
def create_subscription():
    from models import User, Subscription
    from database import db

    data = request.get_json()

    if not data or not data.get("username") or not data.get("topic"):
        return jsonify({"error": "Please provide username and topic"}), 400

    username = data["username"]
    topic = data["topic"]

    valid_topics = ["business", "technology", "sports", "health", "general"]
    if topic not in valid_topics:
        return jsonify({
            "error": f"Invalid topic. Choose from: {', '.join(valid_topics)}"
        }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, email=f"{username}@newsapp.com")
        db.session.add(user)
        db.session.flush()

    existing = Subscription.query.filter_by(
        user_id=user.id,
        topic=topic
    ).first()

    if existing:
        return jsonify({"message": f"{username} is already subscribed to {topic}"}), 200

    subscription = Subscription(user_id=user.id, topic=topic)
    db.session.add(subscription)
    db.session.commit()

    return jsonify({
        "message": f"{username} successfully subscribed to {topic}",
        "user_id": user.id,
        "topic": topic
    }), 201


@app.route("/digest/<int:user_id>", methods=["GET"])
def get_digest(user_id):
    from models import User, Subscription, Article

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": f"User {user_id} not found"}), 404

    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    if not subscriptions:
        return jsonify({"error": f"{user.username} has no subscriptions"}), 404

    topics = [sub.topic for sub in subscriptions]

    articles = Article.query.filter(
        Article.category.in_(topics)
    ).order_by(Article.published_at.desc()).limit(20).all()

    result = []
    for article in articles:
        result.append({
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "url": article.url,
            "source": article.source,
            "category": article.category,
            "published_at": article.published_at.isoformat() if article.published_at else None
        })

    return jsonify({
        "user": user.username,
        "subscribed_topics": topics,
        "total": len(result),
        "articles": result
    })


@app.route("/trending", methods=["GET"])
def get_trending():
    from models import SearchLog
    from database import db
    from datetime import date

    today = date.today()

    results = db.session.query(
        SearchLog.keyword,
        db.func.count(SearchLog.keyword).label("count")
    ).filter(
        db.func.date(SearchLog.searched_at) == today
    ).group_by(
        SearchLog.keyword
    ).order_by(
        db.desc("count")
    ).limit(5).all()

    trending = []
    for row in results:
        trending.append({
            "keyword": row.keyword,
            "searches_today": row.count
        })

    if not trending:
        return jsonify({"message": "No searches yet today", "trending": []}), 200

    return jsonify({
        "date": today.isoformat(),
        "trending": trending
    })


if __name__ == "__main__":
    app.run(debug=True)