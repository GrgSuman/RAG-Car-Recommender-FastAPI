from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from utils.create_vector_db import build_vector_store
from utils.query_creation import generate_query
from data import get_all_vehicles
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv
from models import RecommendationRequest

# Load environment variables
load_dotenv()

app = FastAPI(title="Car Recommendation API")

# API Key Middleware
class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # check API key check for certain paths if needed
        if request.url.path in ["/get-recommendations", "/convert-to-vector"]:
            # Get API key from header
            api_key = request.headers.get("X-API-Key")

            # Get the expected API key from environment variable
            expected_api_key = os.getenv("PYTHON_API_KEY")

            print(expected_api_key, api_key)
            print(api_key == expected_api_key)

            # Check if API key is provided and valid
            if not api_key or (api_key != expected_api_key):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid or missing API key"
                )

        # If other paths, proceed with the request
        return await call_next(request)

# Adding the API key middleware
# app.add_middleware(APIKeyMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World2"}

@app.post("/get-recommendations")
async def get_recommendations(request: RecommendationRequest):

    query = generate_query(request.preferences, request.activities, request.savedVehicles)

    # Initialize embeddings 
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Load your index
    vector_store = FAISS.load_local("car_search_index_50", embeddings,allow_dangerous_deserialization=True)

    # execute query
    results = vector_store.similarity_search(query, k=6)

    # Extract only metadata from results
    car_recommendations = []
    for doc in results:
        car = doc.metadata
        car_recommendations.append(car)

    return {
        "status": "success",
        "message": "Recommendations found",
        "query": query,
        "recommendations": car_recommendations
    }

@app.post("/convert-to-vector")
async def convert_to_vector():
    try:
        # Build and save vector store
        vehicles = get_all_vehicles()
        vector_store = build_vector_store(vehicles)
        vector_store.save_local("car_search_index_50")  # More descriptive index name
        
        return {
            "status": "success",
            "message": "Successfully converted database to vectors",
            "details": {
                "total_vehicles": len(vehicles),
                "index_location": "car_search_index_50"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting to vectors: {str(e)}"
        )


