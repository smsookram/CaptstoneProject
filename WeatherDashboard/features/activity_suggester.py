# activity_suggester.py

def suggest_activities(description, temperature, unit="C"):

    # Normalize to Celsius if needed
    if unit.upper() == "F":
        temperature = (temperature - 32) * 5 / 9  # Convert °F to °C

    suggestions = []

    description = description.lower()

    if "rain" in description:
        suggestions.append("Visit a museum")
        suggestions.append("Watch a movie indoors")
        suggestions.append("Go to a cozy cafe with a book")
    elif "snow" in description:
        suggestions.append("Go skiing or snowboarding")
        suggestions.append("Build a snowman")
        suggestions.append("Enjoy hot cocoa at home")
    elif "storm" in description or "thunder" in description:
        suggestions.append("Stay indoors and play board games")
        suggestions.append("Catch up on your favorite series")
    elif temperature > 29:  # ~85°F
        suggestions.append("Go swimming")
        suggestions.append("Visit a water park")
        suggestions.append("Stay cool indoors with an iced drink")
    elif 18 <= temperature <= 29:  # ~65–85°F
        suggestions.append("Go for a hike")
        suggestions.append("Have a picnic")
        suggestions.append("Visit a local park")
    elif 7 <= temperature < 18:  # ~45–65°F
        suggestions.append("Visit an indoor gallery or museum")
        suggestions.append("Take a brisk walk")
        suggestions.append("Try a new coffee shop")
    else:  # Cold weather
        suggestions.append("Visit a bookstore")
        suggestions.append("Bake something at home")
        suggestions.append("Enjoy a warm drink with a view")

    return suggestions
