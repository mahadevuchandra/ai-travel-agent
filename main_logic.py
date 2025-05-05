# travel_advisor.py

import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def get_weather(city, start_date):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if "list" not in data:
        return [{"dt_txt": "N/A", "main": {"temp": "N/A"}, "weather": [{"description": "No data"}]}]

    return data["list"][:5]  # Return first 5 forecast entries (can be refined)

def generate_prompt(destination, start_date, end_date, interests):
    interest_str = ", ".join(interests)
    return (
        f"Suggest a travel itinerary for someone visiting {destination} from {start_date} to {end_date}. "
        f"The traveler's interests include {interest_str}. "
        "Include sightseeing, dining, and local cultural tips."
    )

def get_travel_recommendation(destination, start_date, end_date, interests):
    prompt = generate_prompt(destination, start_date, end_date, interests)
    response = model.generate_content(prompt)
    itinerary = response.text
    weather = get_weather(destination, start_date)
    return itinerary, weather
