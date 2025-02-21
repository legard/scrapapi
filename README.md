# ScrapAPI

ScrapAPI is a FastAPI-based web service designed for scraping and analyzing web content. It utilizes Celery for task management and Redis as a message broker. The service allows users to submit URLs for scraping and retrieves structured data such as article titles, authors, publish dates, and more.

## Features

- **Web Scraping**: Extract structured data from web articles using `newspaper4k`.
- **Task Management**: Asynchronous task processing with Celery.
- **API Endpoints**: RESTful API for submitting scrape tasks and retrieving results.
- **Redis Integration**: Redis is used as a message broker for Celery tasks.
- **Flower Integration**: Monitor Celery tasks with Flower.

## Prerequisites

- Python 3.12
- Docker and Docker Compose

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/legard/scrapapi.git
   cd scrapapi
   ```

2. **Build and start the services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   - The FastAPI application will be available at `http://localhost:8000`.
   - The Flower monitoring tool will be available at `http://localhost:5555`.

## API Endpoints

### Submit a Scrape Task

- **URL**: `/api/v1/scrape`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "url": "https://example.com/article"
  }
  ```
- **Response**:
  ```json
  {
    "task_id": "task-id",
    "status": "PENDING"
  }
  ```

### Check Task Status

- **URL**: `/api/v1/tasks/{task_id}`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "task_id": "task-id",
    "status": "SUCCESS",
    "result": {
      "title": "Article Title",
      "authors": ["Author 1", "Author 2"],
      "publish_date": "2023-10-01T00:00:00",
      "text": "Article content...",
      "keywords": ["keyword1", "keyword2"],
      "summary": "Article summary...",
      "url": "https://example.com/article"
    }
  }
  ```

## Configuration

The application uses environment variables for configuration. The default settings are defined in `app/core/config.py`. You can override these settings by creating a `.env` file in the root directory.

## Development

To set up the development environment:

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run Celery worker**:
   ```bash
   celery -A app.core.celery.celery_app worker -Q main-queue --loglevel=info
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. 