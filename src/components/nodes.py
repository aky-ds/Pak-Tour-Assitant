import os
from dotenv import load_dotenv

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from src.components.states import TravelState
from src.components.Mtools import tavily_search

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
# TOURISM AGENT (Step 1 only)
# ─────────────────────────────────────────────
def tourism_agent(state: TravelState):

    query = f"""
    Best tourism destinations in Pakistan for:
    {state['user_query']}
    """

    tourism_results = tavily_search(query)

    city_list = "\n".join([f"- {c}" for c in PAKISTAN_CITIES])

    return {
        "suggested_places": PAKISTAN_CITIES,
        "tourism_results": tourism_results,
        "messages": [
            AIMessage(content=f"""
🇵🇰 Pakistan Tourism Suggestions

{city_list}

---

{tourism_results}

👉 Select a city to continue planning.
""")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# ─────────────────────────────────────────────
# BUS ROUTE AGENT
# ─────────────────────────────────────────────
def bus_route_agent(state: TravelState):

    city = state["selected_city"]

    query = f"""
    Best bus routes from major cities to {city}, Pakistan.

    Include:
    - Faisal Movers
    - Daewoo Express
    - Niazi Express
    - Ticket prices
    - Duration
    """

    routes = tavily_search(query)

    return {
        "bus_routes": routes,
        "messages": [AIMessage(content=f"🚌 Bus routes found for {city}")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# ─────────────────────────────────────────────
# HOTEL AGENT
# ─────────────────────────────────────────────
def hotel_agent(state: TravelState):

    city = state["selected_city"]

    query = f"""
    Best hotels in {city} Pakistan:
    budget hotels, luxury hotels, family stays with prices
    """

    hotels = tavily_search(query)

    return {
        "hotel_results": hotels,
        "messages": [AIMessage(content=f"🏨 Hotels found in {city}")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }


# ─────────────────────────────────────────────
# EXPENSE AGENT
# ─────────────────────────────────────────────
def expense_agent(state: TravelState):

    prompt = f"""
    Estimate travel cost in Pakistan.

    City: {state['selected_city']}

    Bus Routes:
    {state['bus_routes']}

    Hotels:
    {state['hotel_results']}

    Include:
    - Transport cost
    - Hotel cost
    - Food cost
    - Daily budget

    Return total in PKR.
    """

    response = llm.invoke([HumanMessage(content=prompt)])

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
    Create a 6-day Pakistan travel itinerary.

    City: {state['selected_city']}

    Bus Routes:
    {state['bus_routes']}

    Hotels:
    {state['hotel_results']}

    Budget:
    {state['estimated_budget']}

    Include:
    - Day-wise plan
    - Attractions
    - Food spots
    - Travel tips
    """

    response = llm.invoke([
        SystemMessage(content="You are a Pakistan travel expert"),
        HumanMessage(content=prompt),
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

    final = f"""
🇵🇰 Pakistan Travel Plan

📍 City: {state['selected_city']}

🚌 Bus Routes:
{state['bus_routes']}

🏨 Hotels:
{state['hotel_results']}

💰 Budget:
{state['estimated_budget']}

🗓️ Itinerary:
{state['itinerary']}
"""

    return {
        "final_response": final,
        "messages": [AIMessage(content=final)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }