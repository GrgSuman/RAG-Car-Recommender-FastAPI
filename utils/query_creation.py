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

    # Start with a base query
    query_parts.append("Looking for a nice car")

    # 1. Add preference signals if preferences exist
    if preferences:
        # Budget - Extend range below min and above max
        if preferences.budgetMin and preferences.budgetMax:
            # If min is 0, only extend the max
            if preferences.budgetMin == 0:
                strict_min = 0
                strict_max = preferences.budgetMax + 5000
            else:
                # Extend 2k below min and 5k above max
                strict_min = max(0, preferences.budgetMin - 2000)
                strict_max = preferences.budgetMax + 5000
            
            query_parts.append(
                f"between ${strict_min:,} and ${strict_max:,}")

        # Car Types
        if preferences.carTypes and len(preferences.carTypes) > 0:
            query_parts.append(f"Prefer {' or '.join(preferences.carTypes)}")

        # Fuel Types
        if preferences.fuelTypes and len(preferences.fuelTypes) > 0:
            query_parts.append(f"that run on {' or '.join(preferences.fuelTypes)} fuel")

        # Brand
        if preferences.brand and len(preferences.brand) > 0:
            query_parts.append(f"Brands I like include {', '.join(preferences.brand)}")

        # Features
        if preferences.features and len(preferences.features) > 0:
            query_parts.append(f"Key features I want are {', '.join(preferences.features)}")

        # Primary Use
        if preferences.primarilyUse and len(preferences.primarilyUse) > 0:
            query_parts.append(f"The car should be great for {' and '.join(preferences.primarilyUse)}")

        # Top Priorities
        if preferences.topPriorities and len(preferences.topPriorities) > 0:
            query_parts.append(f"My top priorities are {', '.join(preferences.topPriorities)}")

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
            query_parts.append(f"I liked cars such as the {', '.join(sorted(seen_cars))}")

        if search_terms:
            query_parts.append(f"I've searched for {' and '.join(set(search_terms))}")

    # 3. Add saved vehicles as part of the context, not as a direct match
    if savedVehicles:
        query_parts.append(f"Similar to what I've saved before")  # More general reference

    return " ".join(query_parts) if query_parts else "Show all vehicles"