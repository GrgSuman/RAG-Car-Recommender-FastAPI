# models.py
from typing import List, Optional
from pydantic import BaseModel

class Preferences(BaseModel):
    budgetMin: Optional[int] = 0
    budgetMax: Optional[int] = 0
    carTypes: Optional[List[str]] = []
    fuelTypes: Optional[List[str]] = []
    brand: Optional[List[str]] = []
    features: Optional[List[str]] = []
    primarilyUse: Optional[List[str]] = []
    topPriorities: Optional[List[str]] = []

class Activity(BaseModel):
    action: str
    carTitles: Optional[List[str]] = []
    query: Optional[str] = None

class RecommendationRequest(BaseModel):
    preferences: Optional[Preferences] = None
    activities: Optional[List[Activity]] = None
    savedVehicles: Optional[List[str]] = []
