# SQLAlchemy for high-level database operations
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv


load_dotenv()
# psycopg2-binary handles the actual PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)


engine = create_engine(DATABASE_URL)

def get_all_vehicles():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM \"Vehicle\""))
        # Get column names from the result
        columns = result.keys()
        # Convert each row to a dictionary using column names as keys
        return [dict(zip(columns, row)) for row in result]

# # You can test it by calling it directly
# if __name__ == "__main__":
#     vehicles = get_all_vehicles()
#     print(len(vehicles))
#     # for vehicle in vehicles:
#     #     print(vehicle)  # Now each vehicle will be a dictionary with named keys