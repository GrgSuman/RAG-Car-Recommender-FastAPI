# utils/query_creation.py
from typing import Optional, List
from models import Preferences, Activity

def generate_query(preferences: Optional[Preferences], activities: Optional[List[Activity]], savedVehicles: Optional[List[str]]) -> str:
    """
    Generates a natural language search query from preferences, activities, and saved vehicles

    Args:
        preferences: Preferences model containing user preferences
        activities: List of Activity models containing user activities
        savedVehicles: List of saved vehicle titles

    Returns:
        str: Generated natural language query
    """
    query_parts = []

    # Start with a more specific base query
    query_parts.append("I am looking for a vehicle that matches these specific requirements:")

    # 1. Add preference signals if preferences exist
    if preferences:
        # Prioritize preferences based on importance
        if preferences.topPriorities and len(preferences.topPriorities) > 0:
            query_parts.append(f"Most importantly, I need: {', '.join(preferences.topPriorities)}")

        # Budget - Extend range below min and above max
        if preferences.budgetMin and preferences.budgetMax:
            if preferences.budgetMin == 0:
                strict_min = 0
                strict_max = preferences.budgetMax + 5000
            else:
                strict_min = max(0, preferences.budgetMin - 2000)
                strict_max = preferences.budgetMax + 5000
            
            query_parts.append(
                f"The price should be between ${strict_min:,} and ${strict_max:,}")

        # Car Types
        if preferences.carTypes and len(preferences.carTypes) > 0:
            query_parts.append(f"I prefer these types of vehicles: {' or '.join(preferences.carTypes)}")

        # Brand
        if preferences.brand and len(preferences.brand) > 0:
            query_parts.append(f"I am interested in these brands: {', '.join(preferences.brand)}")

        # Features
        if preferences.features and len(preferences.features) > 0:
            query_parts.append(f"Must have these features: {', '.join(preferences.features)}")

        # Fuel Types
        if preferences.fuelTypes and len(preferences.fuelTypes) > 0:
            query_parts.append(f"Should run on: {' or '.join(preferences.fuelTypes)} fuel")

        # Primary Use
        if preferences.primarilyUse and len(preferences.primarilyUse) > 0:
            query_parts.append(f"The vehicle should be suitable for: {' and '.join(preferences.primarilyUse)}")

    # 2. Add activity signals if activities exist
    if activities:
        seen_cars = set()
        search_terms = []

        for activity in activities:
            if activity.action == "searched" and activity.query:
                search_terms.append(activity.query)
            elif activity.carTitles:
                seen_cars.update(activity.carTitles)

        if seen_cars:
            query_parts.append(f"I have shown interest in similar vehicles like: {', '.join(sorted(seen_cars))}")

        if search_terms:
            query_parts.append(f"I have previously searched for: {' and '.join(set(search_terms))}")

    if savedVehicles:
        query_parts.append(f"I have saved these vehicles before, so I'm interested in similar options")

    return " ".join(query_parts) if query_parts else "Show me all available vehicles"