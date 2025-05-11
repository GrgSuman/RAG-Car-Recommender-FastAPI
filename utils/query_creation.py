# utils/query_creation.py
from typing import Optional, List
from models import Preferences, Activity

def generate_query(preferences: Optional[Preferences], activities: Optional[List[Activity]]) -> str:
    """
    Generates a search query from preferences and activities

    Args:
        preferences: Preferences model containing user preferences
        activities: List of Activity models containing user activities

    Returns:
        str: Generated search query
    """
    query_parts = []

    # 1. Add preference filters if preferences exist
    if preferences:
        # Budget
        if preferences.budgetMin and preferences.budgetMax:
            query_parts.append(
                f"${preferences.budgetMin/100:,.0f}-${preferences.budgetMax/100:,.0f}")

        # Other preferences
        pref_to_label = {
            "carTypes": "Type",
            "fuelTypes": "Fuel",
            "brand": "Brand",
            "features": "Features",
            "primarilyUse": "Use",
            "topPriorities": "Priority"
        }

        for pref_key, label in pref_to_label.items():
            pref_value = getattr(preferences, pref_key)
            if pref_value and len(pref_value) > 0:
                query_parts.append(f"{label}: {', '.join(pref_value)}")

    # 2. Add activity signals if activities exist
    if activities:
        seen_cars = set()
        search_terms = []

        for activity in activities:
            if activity.action == "searched" and activity.query:
                search_terms.append(activity.query)
            elif activity.carIds:
                seen_cars.update(activity.carIds)

        if seen_cars:
            query_parts.append(f"Like: {', '.join(sorted(seen_cars))}")

        if search_terms:
            query_parts.append(f"Searched: {', '.join(set(search_terms))}")

    return " | ".join(query_parts) if query_parts else "Show all vehicles"