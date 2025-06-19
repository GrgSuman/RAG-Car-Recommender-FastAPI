# Car Recommendation API

A Car recommendation system built with FastAPI that uses Google's Generative AI and vector embeddings to provide personalized car recommendations based on user preferences, activities, and saved vehicles.

## How It Works

### 1. Recommendation Process

The system uses a multi-step process to generate personalized car recommendations:

1. **Query Generation**
   - Takes user preferences (budget, car types, brands, features, etc.)
   - Considers user activities (searches, viewed cars, compared cars)
   - Incorporates saved vehicles
   - Generates a natural language query that captures all requirements

2. **Vector Search**
   - Uses Google's Generative AI to convert the query into embeddings
   - Searches the FAISS vector database for similar cars
   - Initial search returns 15 potential matches

3. **Smart Filtering & Scoring**
   - Filters cars based on price range:
     - For min=0: range is 0 to max+5000
     - For other cases: range is (min-2000) to (max+5000)
   - Scores each car based on multiple factors:
     - Base score: 1.0
     - Car type match: +0.3
     - Brand match: +0.3
     - Feature matches: +0.1 per feature
     - Fuel type match: +0.2
     - Primary use match: +0.15 per match

4. **Final Selection**
   - Sorts cars by their relevance score
   - Returns top 6 most relevant recommendations

### 2. Key Components

#### Vector Database (`car_search_index_50/`)
- Stores vector embeddings of all cars
- Each car is represented by a rich text description including:
  - Basic details (year, make, model, color)
  - Specifications (body type, transmission, drive type)
  - Price and condition
  - Features and description
  - Technical details (fuel type, economy, etc.)

#### API Endpoints

1. **GET /**
   - Health check endpoint
   - Returns a simple "Hello World" message

2. **POST /get-recommendations**
   - Main recommendation endpoint
   - Accepts:
     ```json
     {
       "preferences": {
         "budgetMin": number,
         "budgetMax": number,
         "carTypes": string[],
         "fuelTypes": string[],
         "brand": string[],
         "features": string[],
         "primarilyUse": string[],
         "topPriorities": string[]
       },
       "activities": [
         {
           "action": string,
           "query": string,
           "carTitles": string[]
         }
       ],
       "savedVehicles": string[]
     }
     ```
   - Returns:
     ```json
     {
       "status": "success",
       "message": "Recommendations found",
       "query": string,
       "recommendations": [
         {
           "year": number,
           "make": string,
           "model": string,
           "price": number,
           "features": string[],
           // ... other car details
         }
       ]
     }
     ```

3. **POST /convert-to-vector**
   - Converts the car database to vector embeddings
   - Creates/updates the FAISS index
   - Returns conversion status and details

## Technical Architecture

### Dependencies
- FastAPI: Web framework
- FAISS: Vector similarity search
- Google Generative AI: Embeddings and text generation
- SQLAlchemy: Database operations
- Python-dotenv: Environment management

### Project Structure
```
.
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models for request/response
├── data.py             # Database operations
├── requirements.txt    # Project dependencies
├── utils/             # Utility functions
│   ├── create_vector_db.py  # Vector store creation
│   └── query_creation.py    # Query generation
└── car_search_index_50/  # Vector store directory
```

## Setup and Installation

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

4. Create a `.env` file with required variables:
```
GOOGLE_API_KEY=your_google_api_key
PYTHON_API_KEY=your_python_api_key
DATABASE_URL=your_db_url
```

5. Convert database to vectors:
```bash
curl -X POST http://localhost:8000/convert-to-vector
```

6. Start the server:
```bash
uvicorn main:app --reload
```

## Usage Example

```python
import requests

# Example recommendation request
response = requests.post(
    "http://localhost:8000/get-recommendations",
    json={
        "preferences": {
            "budgetMin": 20000,
            "budgetMax": 30000,
            "carTypes": ["SUV"],
            "fuelTypes": ["Electric"],
            "brand": ["Toyota"],
            "features": ["Bluetooth", "Backup Camera"],
            "primarilyUse": ["Family", "Commuting"]
        }
    }
)

# Get recommendations
recommendations = response.json()["recommendations"]
```

## Performance Considerations

- The system uses vector similarity search for fast matching
- Price filtering is applied after vector search
- Scoring system ensures relevant results
- Results are cached for similar queries
- Vector store is optimized for quick lookups

## Security

- API key authentication for sensitive endpoints
- CORS middleware for cross-origin requests
- Environment variables for sensitive configuration
- Input validation using Pydantic models
