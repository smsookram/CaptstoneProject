import random
from datetime import datetime

def suggest_activities(description, temperature, unit="C", num_suggestions=3):
    # Normalize to Celsius if needed
    if unit.upper() == "F":
        temperature = (temperature - 32) * 5 / 9  # Convert °F to °C

    description = description.lower()
    hour = datetime.now().hour
    is_evening = hour >= 18 or hour <= 6

    suggestions = []

    if any(word in description for word in ["rain", "drizzle", "showers"]):
        suggestions += [
            "Visit a museum or art exhibit",
            "Watch a movie indoors or start a new series",
            "Relax at a cozy cafe with a good book",
            "Try out a new recipe or bake something",
            "Do a creative indoor hobby like painting or journaling"
        ]
    elif any(word in description for word in ["snow", "flurries"]):
        suggestions += [
            "Build a snowman or snow fort",
            "Go sledding or snowboarding",
            "Enjoy hot cocoa by the window",
            "Do a winter-themed craft at home"
        ]
    elif any(word in description for word in ["storm", "thunder", "lightning"]):
        suggestions += [
            "Stay indoors and play a board or card game",
            "Catch up on your favorite shows or YouTube channels",
            "Start a cozy DIY project"
        ]
    elif any(word in description for word in ["cloud", "overcast"]):
        suggestions += [
            "Go for a relaxed walk or jog",
            "Visit a greenhouse or botanical garden",
            "Check out a coffee tasting or local food spot"
        ]
    elif any(word in description for word in ["clear", "sunny"]):
        suggestions += [
            "Have a picnic in the park",
            "Go for a hike or bike ride",
            "Read a book outdoors",
            "Take photos around your city"
        ]

    # Temp-based general suggestions
    if temperature > 29:
        suggestions += [
            "Visit a swimming pool or beach",
            "Grab an iced drink and relax indoors",
            "Go to a shaded outdoor market"
        ]
    elif 18 <= temperature <= 29:
        suggestions += [
            "Explore a nearby trail",
            "Visit a farmers' market",
            "Try a new outdoor workout"
        ]
    elif 7 <= temperature < 18:
        suggestions += [
            "Walk around a museum or mall",
            "Try a new cafe or bakery",
            "Explore a bookstore or library"
        ]
    else:
        suggestions += [
            "Bundle up and visit a local exhibit",
            "Enjoy a warm drink with a scenic view",
            "Host a movie or game night at home"
        ]

    # Add time-of-day enhancements
    if is_evening:
        suggestions += [
            "Have a cozy movie night",
            "Try stargazing if it’s clear",
            "Visit a local jazz bar or night market"
        ]
    else:
        suggestions += [
            "Go to a brunch spot you’ve never tried",
            "Take a scenic walk or bike ride"
        ]

    # Avoid duplicates and select randomly
    unique_suggestions = list(set(suggestions))
    random.shuffle(unique_suggestions)

    return unique_suggestions[:num_suggestions]
