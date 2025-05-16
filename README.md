# Car Recommendation API

A FastAPI-based car recommendation system that uses Google's Generative AI and vector embeddings to provide personalized car recommendations based on user preferences and activities.

## Features

- Vector-based car search using FAISS
- Integration with Google's Generative AI for embeddings and chat
- RESTful API endpoints for car recommendations
- API key authentication middleware
- CORS support
- Vector database conversion utility

## Prerequisites

- Python 3.8+
- Google API Key for Generative AI
- Python API Key for authentication

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
PYTHON_API_KEY=your_python_api_key
DATABASE_URL=your_db_url
```

## Project Structure

```
.
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models for request/response
├── data.py             # Data handling and vehicle information
├── requirements.txt    # Project dependencies
├── utils/             # Utility functions
│   ├── create_vector_db.py
│   └── query_creation.py
└── car_search_index_50/  # Vector store directory
```

## API Endpoints

### GET /
- Basic health check endpoint
- Returns a simple "Hello World" message

### POST /get-recommendations
- Requires API key authentication
- Accepts user preferences, activities, and saved vehicles
- Returns personalized car recommendations
- Uses vector similarity search to find matching vehicles

### POST /convert-to-vector
- Requires API key authentication
- Converts the vehicle database to vector embeddings
- Saves the vector store locally
- Returns conversion status and details

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

Key dependencies include:
- FastAPI
- LangChain
- Google Generative AI
- FAISS (Facebook AI Similarity Search)
- Python-dotenv
- Uvicorn

For a complete list of dependencies, see `requirements.txt`.

## Security

- API key authentication is implemented for sensitive endpoints
- CORS middleware is configured for cross-origin requests
- Environment variables are used for sensitive configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
