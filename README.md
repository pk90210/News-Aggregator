# News Aggregator

A Flask-based REST API that aggregates and serves news articles from various sources. The application fetches articles from NewsAPI, stores them in a PostgreSQL database, and provides endpoints to retrieve, search, and subscribe to news by category.

## Features

- **News Aggregation**: Automatically fetches news articles from NewsAPI
- **Category Filtering**: Browse news by categories (general, business, technology, sports, health)
- **Search Functionality**: Search articles by keywords with search history tracking
- **User Subscriptions**: Users can subscribe to specific news topics
- **Background Scheduler**: Automatically updates news articles at regular intervals
- **RESTful API**: Clean endpoints for accessing news data

## Tech Stack

- **Backend Framework**: Flask 3.1.3
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Task Scheduler**: APScheduler 3.11.2
- **HTTP Client**: httpx 0.28.1
- **Environment Management**: python-dotenv 1.2.2

## Project Structure

```
.
├── app.py           # Main Flask application and API routes
├── models.py        # SQLAlchemy database models
├── database.py      # Database initialization and configuration
├── scraper.py       # NewsAPI integration and article fetching
├── scheduler.py     # Background task scheduler
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- NewsAPI key (get one free at [newsapi.org](https://newsapi.org))

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd "News Aggregator"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` file** in the project root with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/news_aggregator
   NEWS_API_KEY=your_newsapi_key_here
   FLASK_ENV=development
   ```

6. **Initialize the database**
   ```bash
   python -c "from app import app, init_db; init_db(app)"
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Get News by Category

**GET** `/news`

Retrieve the latest 20 articles for a specific category.

**Query Parameters:**
- `category` (optional): Filter by category - `general`, `business`, `technology`, `sports`, `health` (default: `general`)

**Example:**
```bash
curl "http://localhost:5000/news?category=business"
```

**Response:**
```json
{
  "category": "business",
  "total": 20,
  "articles": [
    {
      "id": 1,
      "title": "Kenya's Economy Grows",
      "description": "Article description...",
      "url": "https://example.com/article",
      "source": "News Source",
      "category": "business",
      "published_at": "2026-04-27T10:30:00"
    }
  ]
}
```

### Search Articles

**GET** `/news/search`

Search articles by keyword.

**Query Parameters:**
- `q` (required): Search keyword

**Example:**
```bash
curl "http://localhost:5000/news/search?q=NSE"
```

**Response:**
```json
{
  "keyword": "nse",
  "total": 5,
  "articles": [...]
}
```

### Create User Subscription

**POST** `/subscriptions`

Subscribe a user to a specific news topic.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "topic": "Kenya technology"
}
```

## Database Models

### Article
- `id`: Primary key
- `title`: Article title
- `description`: Article content
- `url`: Link to the article
- `category`: News category
- `source`: News source
- `published_at`: Publication timestamp
- `created_at`: When article was saved

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `created_at`: Account creation date
- `subscriptions`: Relationship to subscriptions

### Subscription
- `id`: Primary key
- `user_id`: Foreign key to User
- `topic`: Subscription topic
- `created_at`: Subscription date

### SearchLog
- `id`: Primary key
- `keyword`: Search keyword
- `searched_at`: Search timestamp

## Configuration

Key configuration options in `app.py`:

- `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection string
- `SQLALCHEMY_TRACK_MODIFICATIONS`: SQLAlchemy modification tracking (disabled for performance)

## Development

### Running Tests
```bash
python -m pytest
```

### Code Style
The project follows PEP 8 Python style guidelines.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the terms specified in the LICENSE file.

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` in `.env` is correct
- Check database credentials

### No Articles Being Fetched
- Verify `NEWS_API_KEY` is correct and valid
- Check internet connection
- Ensure NewsAPI quota hasn't been exceeded

### Scheduler Not Running
- Ensure APScheduler is properly installed
- Check Flask app context is properly initialized

## Future Enhancements

- User authentication and authorization
- Email notifications for subscriptions
- Advanced filtering and recommendations
- Caching layer for improved performance
- Webhook support for real-time updates
- Mobile app integration

## Support

For issues and questions, please open an issue on the project repository.
