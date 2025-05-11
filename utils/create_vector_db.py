import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from data import vehicles  

# Load environment variables
load_dotenv()

def prepare_car_for_embedding(car):
    """Format car data into a rich text description for embedding"""
    fuel_economy = (f"{car['fuelConsumptionCombined']}L/100km" 
                   if car['fuelConsumptionCombined'] else "N/A")
    
    price = f"${car['price']/100:,.2f}"  # Convert cents to dollars
    
    return f"""
    {car['year']} {car['make']} {car['model']} ({car['color']})
    Body Type: {car['bodyType']}
    Price: {price}
    Condition: {car['condition']}
    Odometer: {car['odometer']:,} km
    Fuel Type: {car['fuelType']}
    Transmission: {car['transmission']}
    Drive Type: {car['driveType']}
    Combined Fuel Economy: {fuel_economy}
    Doors: {car['doors']}
    Seats: {car['seats']}
    Features: {', '.join(car['features'])}
    Description: {car['description']}
    """

def build_vector_store(vehicles):
    """Create vector embeddings for all vehicles"""
    # Prepare texts and metadata
    texts = [prepare_car_for_embedding(car) for car in vehicles]
    metadatas = vehicles
    
    # Initialize embeddings - using Google's as in your original setup
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create and save vector store
    vector_store = FAISS.from_texts(
        texts=texts, 
        embedding=embeddings, 
        metadatas=metadatas
    )
    return vector_store

# if __name__ == "__main__":
#     # Build and save the vector store when script is run
#     vector_store = build_vector_store(vehicles)
#     print("Vector store created and saved successfully!")