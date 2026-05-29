
from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from src.components.states import TravelState

from src.components.nodes import (
    tourism_agent,
    bus_route_agent,
    hotel_agent,
    expense_agent,
    itinerary_agent,
    final_agent,
)

graph = StateGraph(TravelState)

# Nodes
graph.add_node(
    "tourism_agent",
    tourism_agent
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

# Entry Flow
graph.add_edge(
    START,
    "tourism_agent"
)

graph.add_edge(
    "tourism_agent",
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

app = graph.compile()
