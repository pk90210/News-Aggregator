from apscheduler.schedulers.background import BackgroundScheduler
from scraper import fetch_articles


def start_scheduler(app):
    """Start the background scheduler to fetch articles automatically."""

    scheduler = BackgroundScheduler()

    def fetch_all_categories():
        """Fetch articles for all categories and save to DB."""
        categories = ["business", "technology", "sports", "health", "general"]

        with app.app_context():
            for category in categories:
                print(f"Fetching articles for category: {category}")
                fetch_articles(category)

    # Run immediately on startup
    with app.app_context():
        fetch_all_categories()

    # Then run every 6 hours automatically
    scheduler.add_job(
        func=fetch_all_categories,
        trigger="interval",
        hours=6,
        id="fetch_articles_job"
    )

    scheduler.start()
    print("Scheduler started — fetching articles every 6 hours")

    return scheduler 
