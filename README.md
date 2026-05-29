
# 🇵🇰 Pakistan Tourism AI Assistant

A multi-agent AI travel planning system built with **LangGraph, Streamlit, and Groq LLM** that generates complete Pakistan travel plans including bus routes, hotels, budgets, and itineraries.

---

## ✨ Features

### 🧠 Multi-Agent System
- 🌍 Tourism Agent → Suggests Pakistan destinations
- 🚌 Bus Route Agent → Finds intercity bus routes
- 🏨 Hotel Agent → Recommends hotels
- 💰 Expense Agent → Estimates travel budget (PKR)
- 🗓️ Itinerary Agent → Builds day-wise travel plan
- 🧠 Final Agent → Combines everything into final report

---

## 🏗️ Workflow

```text
User Input (Streamlit)
        ↓
Tourism Agent (Tavily Search)
        ↓
User selects City
        ↓
Bus Route Agent
        ↓
Hotel Agent
        ↓
Expense Agent
        ↓
Itinerary Agent
        ↓
Final Agent
        ↓
Final Travel Plan