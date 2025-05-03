# app.py

import streamlit as st
from main_logic import get_travel_recommendation

st.set_page_config(page_title="AI Travel Advisor", layout="centered")

st.title("🧳 AI Travel Advisor")
st.markdown("Plan smarter trips with AI-generated itineraries and weather forecasts!")

destination = st.text_input("Enter your destination")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
interests = st.multiselect("What are you interested in?", [
    "Beaches", "Mountains", "History", "Adventure", "Food", "Shopping", "Culture", "Nightlife"
])

if st.button("Plan My Trip"):
    if destination and interests:
        with st.spinner("Generating your travel itinerary..."):
            itinerary, weather = get_travel_recommendation(destination, start_date, end_date, interests)

            st.subheader("✈️ AI-Generated Travel Plan")
            st.markdown(itinerary)

            st.subheader("🌦️ 5-Day Weather Forecast")
            for entry in weather:
                dt = entry.get("dt_txt", "N/A")
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"]
                st.write(f"**{dt}**: {temp}°C, {desc}")
    else:
        st.warning("Please fill in both destination and interests.")
