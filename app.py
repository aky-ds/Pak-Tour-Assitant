import streamlit as st
from langchain_core.messages import HumanMessage

from src.components.nodes import tourism_agent
from src.components.graph import app

st.set_page_config(
    page_title="Pakistan Tourism AI Assistant",
    page_icon="🇵🇰",
    layout="wide"
)

st.title("🇵🇰 Pakistan Tourism AI Assistant")

# ─────────────────────────────────────
# STEP 1: USER INPUT
# ─────────────────────────────────────
user_query = st.text_area(
    "Describe your trip",
    placeholder="Plan a 6-day trip to northern Pakistan"
)

if "cities" not in st.session_state:
    st.session_state.cities = []

if "tourism" not in st.session_state:
    st.session_state.tourism = ""

# ─────────────────────────────────────
# STEP 1 BUTTON
# ─────────────────────────────────────
if st.button("🔍 Find Destinations"):

    result = tourism_agent({
        "user_query": user_query,
        "messages": [HumanMessage(content=user_query)],
        "llm_calls": 0,
    })

    st.session_state.cities = result["suggested_places"]
    st.session_state.tourism = result["tourism_results"]

# SHOW RESULTS
if st.session_state.cities:

    st.markdown("## 🌍 Suggested Cities")
    st.markdown(st.session_state.tourism)

    selected_city = st.selectbox(
        "Select City",
        st.session_state.cities
    )

    # ─────────────────────────────────────
    # STEP 2 BUTTON
    # ─────────────────────────────────────
    if st.button("🚀 Generate Full Travel Plan"):

        collected = {
            "bus_routes": "",
            "hotel_results": "",
            "estimated_budget": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        for chunk in app.stream(
            {
                "user_query": user_query,
                "selected_city": selected_city,
                "messages": [HumanMessage(content=user_query)],
                "bus_routes": "",
                "hotel_results": "",
                "estimated_budget": "",
                "itinerary": "",
                "final_response": "",
                "llm_calls": 0,
            },
            stream_mode="updates",
        ):

            for node, state in chunk.items():

                if node == "bus_route_agent":
                    collected["bus_routes"] = state.get("bus_routes", "")

                elif node == "hotel_agent":
                    collected["hotel_results"] = state.get("hotel_results", "")

                elif node == "expense_agent":
                    collected["estimated_budget"] = state.get("estimated_budget", "")

                elif node == "itinerary_agent":
                    collected["itinerary"] = state.get("itinerary", "")

                elif node == "final_agent":
                    collected["final_response"] = state.get("final_response", "")

        st.markdown("## 🧠 Final Travel Plan")
        st.markdown(collected["final_response"])