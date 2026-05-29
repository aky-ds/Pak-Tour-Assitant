from dotenv import load_dotenv

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from states import TravelState
from src.components.Mtools import tavily_search
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


PAKISTAN_CITIES = [
    "Hunza",
    "Skardu",
    "Swat",
    "Murree",
    "Naran",
    "Neelum Valley",
    "Fairy Meadows",
    "Lahore",
    "Islamabad",
]


# ─────────────────────────────────────────────
# TOURISM AGENT
# ─────────────────────────────────────────────
def tourism_agent(state: TravelState):

    query = f"""
    Best tourism destinations in Pakistan for:
    {state['user_query']}
    """

    tourism_results = tavily_search(query)

    city_text = " ".join(
        [f"- {city}" for city in PAKISTAN_CITIES]
    )

    return {
        "suggested_places": PAKISTAN_CITIES,
        "messages": [
            AIMessage(
                content=f"""
# 🇵🇰 Pakistan Tourism Suggestions

Popular tourism cities:

{city_text}

---

Tourism Search Results:

{tourism_results}

---

Please type the city name you want to visit.
"""
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# ─────────────────────────────────────────────
# CITY SELECTION AGENT
# ─────────────────────────────────────────────
def city_selection_agent(state: TravelState):

    latest_message = state["messages"][-1].content.strip()

    matched_city = None

    for city in PAKISTAN_CITIES:

        if city.lower() in latest_message.lower():
            matched_city = city
            break

    # Invalid city
    if not matched_city:

        city_text = " ".join(
            [f"- {city}" for city in PAKISTAN_CITIES]
        )

        return {
            "messages": [
                AIMessage(
                    content=f"""
❌ Please select a valid city.

Available cities:

{city_text}
"""
                )
            ]
        }

    return {
        "selected_city": matched_city,
        "messages": [
            AIMessage(
                content=f"""
✅ Great choice.

Planning your Pakistan trip to:

# {matched_city}
"""
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
# ─────────────────────────────────────────────
# BUS ROUTE AGENT
# ─────────────────────────────────────────────
def bus_route_agent(state: TravelState):

    city = state["selected_city"]

    query = f"""
    Best bus routes to {city} Pakistan.

    Include:
    - Faisal Movers
    - Daewoo Express
    - Niazi Express

    Also include:
    - Ticket prices
    - Travel duration
    - Departure cities
    """

    routes = tavily_search(query)

    return {
        "bus_routes": routes,
        "messages": [
            AIMessage(
                content="🚌 Bus routes fetched successfully."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }

# ─────────────────────────────────────────────
# HOTEL AGENT
# ─────────────────────────────────────────────
def hotel_agent(state: TravelState):

    city = state["selected_city"]

    query = f"""
    Best budget hotels in {city} Pakistan.

    Include:
    - Tourist hotels
    - Budget stays
    - Family hotels
    - Room prices
    """

    hotels = tavily_search(query)

    return {
        "hotel_results": hotels,
        "messages": [
            AIMessage(
                content="🏨 Hotel recommendations fetched successfully."
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
# ─────────────────────────────────────────────
# EXPENSE AGENT
# ─────────────────────────────────────────────
def expense_agent(state: TravelState):

    prompt = f"""
    Estimate a Pakistan tourism trip budget.

    Destination:
    {state['selected_city']}

    Bus Routes:
    {state['bus_routes']}

    Hotels:
    {state['hotel_results']}

    Include:
    - Bus expenses
    - Hotel expenses
    - Food expenses
    - Local transport

    Give estimated budget in PKR.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "estimated_budget": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
# ─────────────────────────────────────────────
# ITINERARY AGENT
# ─────────────────────────────────────────────
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a detailed Pakistan tourism itinerary.

    Destination:
    {state['selected_city']}

    Bus Routes:
    {state['bus_routes']}

    Hotels:
    {state['hotel_results']}

    Budget:
    {state['estimated_budget']}

    Include:
    - Day-wise planning
    - Tourist attractions
    - Food recommendations
    - Safety tips
    - Travel advice
    """

    response = llm.invoke([
        SystemMessage(
            content="You are a Pakistan tourism expert"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
# ─────────────────────────────────────────────
# FINAL AGENT
# ─────────────────────────────────────────────
def final_agent(state: TravelState):

    final_response = f"""
# 🇵🇰 Pakistan Tourism Plan

## 📍 Destination
{state['selected_city']}

---

## 🚌 Bus Routes
{state['bus_routes']}

---

## 🏨 Hotels
{state['hotel_results']}

---

## 💰 Estimated Budget
{state['estimated_budget']}

---

## 🗓️ Itinerary
{state['itinerary']}
"""

    return {
        "messages": [
            AIMessage(content=final_response)
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }