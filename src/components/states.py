from typing import List, Annotated, TypedDict
from langchain.messages import AnyMessage
import operator


class TravelState(TypedDict):
    messages:Annotated[List[AnyMessage],operator.add]
    user_query:str
    suggested_cities:List
    selected_city:str
    bus_routes:str
    hotel_results:str
    estimated_budget:str
    itinerary:str
    llm_calls:int
