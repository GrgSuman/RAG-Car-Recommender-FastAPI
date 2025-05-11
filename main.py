from http.client import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.create_vector_db import build_vector_store
from utils.query_creation import generate_query
from data import vehicles
import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


app = FastAPI(title="Car Recommendation API")

from models import RecommendationRequest


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Node.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World2"}

@app.post("/get-recommendations")
async def get_recommendations(request: RecommendationRequest):

    # if request.preferences:
    #     print("\nPreference Details:")
    #     print(f"Budget Range: ${request.preferences.budgetMin/100:.2f} - ${request.preferences.budgetMax/100:.2f}")
    #     print(f"Car Types: {request.preferences.carTypes}")
    #     print(f"Fuel Types: {request.preferences.fuelTypes}")
    #     print(f"Brands: {request.preferences.brand}")
    #     print(f"Features: {request.preferences.features}")
    #     print(f"Primary Use: {request.preferences.primarilyUse}")
    #     print(f"Top Priorities: {request.preferences.topPriorities}")
    
    # if request.activities:
    #     print("\nActivity Details:")
    #     for activity in request.activities:
    #         print(f"Action: {activity.action}")
    #         print(f"Car IDs: {activity.carIds}")
    #         print(f"Query: {activity.query}")
    
    query = generate_query(request.preferences, request.activities)

    # Initialize embeddings 
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Load your index
    vector_store = FAISS.load_local("car_search_index", embeddings,allow_dangerous_deserialization=True)

    # execute query
    results = vector_store.similarity_search(query, k=1)

    # Extract only metadata from results
    car_recommendations = []
    for doc in results:
        car = doc.metadata
        # Format the price for better readability
        car['price'] = f"${car['price']/100:,.2f}"
        car_recommendations.append(car)

    return {
        "message": "Recommendations found",
        "query": query,
        "recommendations": car_recommendations
    }

@app.post("/convert-to-vector")
async def convert_to_vector():
    try:
        # Build and save vector store
        vector_store = build_vector_store(vehicles)
        vector_store.save_local("car_search_index")  # More descriptive index name
        
        return {
            "message": "Successfully converted database to vectors",
            "status": "success",
            "details": {
                "total_vehicles": len(vehicles),
                "index_location": "car_search_index"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting to vectors: {str(e)}"
        )


def print_results(results):
    """Prints search results in a user-friendly format"""
    if not results:
        print("No matching vehicles found")
        return

    print(f"\n{'='*50}")
    print(f"FOUND {len(results)} MATCHING VEHICLES")
    print(f"{'='*50}\n")

    for i, doc in enumerate(results, 1):
        car = doc.metadata  # Access the car metadata
        price = f"${car['price']/100:,.2f}"  # Convert cents to dollars
        
        # Main header
        print(f"{i}. {car['year']} {car['make']} {car['model']}")
        print(f"{'-'*60}")
        
        # Key specs
        print(f"   • Price: {price}")
        print(f"   • Color: {car['color']}")
        print(f"   • Body: {car['bodyType']} | Fuel: {car['fuelType']}")
        print(f"   • Transmission: {car['transmission']} | Drive: {car['driveType']}")
        
        # Condition and mileage
        condition = f"{car['condition']} ({car['odometer']:,} km)" 
        print(f"   • Condition: {condition}")
        
        # Features (show first 5)
        features = car['features'][:5]
        print(f"   • Features: {', '.join(features)}" + 
              ("..." if len(car['features']) > 5 else ""))
        
        # Description (truncated)
        print(f"\n   Description: {car['description'][:150]}...")
        
        # Additional info
        print(f"{'='*50}\n")



