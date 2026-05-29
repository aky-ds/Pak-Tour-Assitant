from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from src.components.states import TravelState

from nodes import (
    tourism_agent,
    city_selection_agent,
    bus_route_agent,
    hotel_agent,
    expense_agent,
    itinerary_agent,
    final_agent,
)
# Router
# Checks whether city already selected

def city_router(state: TravelState):

    if state.get("selected_city"):
        return "bus_route_agent"

    return "city_selection_agent"


# Graph
graph=StateGraph(TravelState)

graph.add_node(
    "city_selection_agent",
    city_selection_agent
)

graph.add_node(
    "bus_route_agent",
    bus_route_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "expense_agent",
    expense_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)

# Flow

graph.add_edge(
    START,
    "tourism_agent"
)

graph.add_conditional_edges(
    "tourism_agent",
    city_router
)

graph.add_edge(
    "city_selection_agent",
    "bus_route_agent"
)

graph.add_edge(
    "bus_route_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "expense_agent"
)

graph.add_edge(
    "expense_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)


app=graph.compile()