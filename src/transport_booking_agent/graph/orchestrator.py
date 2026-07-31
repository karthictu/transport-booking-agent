from functools import partial
from ..agents.parsing_agent import ParsingAgent
from ..agents.filtering_agent import FilteringAgent
from ..agents.booking_agent import BookingAgent
from ..agents.user_profile_agent import UserProfileAgent
from ..agents.guardrail_agent import GuardrailAgent
from ..agents.recognition_agent import RecognitionAgent
from ..agents.search.flight_search_agent import FlightSearchAgent
from ..agents.search.train_search_agent import TrainSearchAgent
from ..agents.search.bus_search_agent import BusSearchAgent
from ..agents.search.cab_search_agent import CabSearchAgent
from ..agents.search.bike_search_agent import BikeSearchAgent
from ..models import AgentState
from .nodes import *
from langgraph.graph import StateGraph, END

# Initialize agents
query_parser = ParsingAgent()
filter_ranker = FilteringAgent()
booking_agent = BookingAgent()
user_profile_agent = UserProfileAgent()
guardrail_agent = GuardrailAgent()
mode_provider_recognition_agent = RecognitionAgent()
flight_search_agent = FlightSearchAgent()
train_search_agent = TrainSearchAgent()
bus_search_agent = BusSearchAgent()
cab_search_agent = CabSearchAgent()
bike_search_agent = BikeSearchAgent()

def create_graph_workflow():
    """Creates the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("get_user_profile", partial(get_user_profile_node, user_profile_agent=user_profile_agent))
    workflow.add_node("guardrail", partial(guardrail_node, guardrail_agent=guardrail_agent))
    workflow.add_node("recognize_mode_provider", partial(recognize_mode_provider_node, mode_provider_recognition_agent=mode_provider_recognition_agent))
    workflow.add_node("parse_query", partial(parse_query_node, query_parser=query_parser))
    workflow.add_node("flight_search", partial(flight_search_node, flight_search_agent=flight_search_agent))
    workflow.add_node("train_search", partial(train_search_node, train_search_agent=train_search_agent))
    workflow.add_node("bus_search", partial(bus_search_node, bus_search_agent=bus_search_agent))
    workflow.add_node("cab_search", partial(cab_search_node, cab_search_agent=cab_search_agent))
    workflow.add_node("bike_search", partial(bike_search_node, bike_search_agent=bike_search_agent))
    workflow.add_node("handle_unsupported_mode", handle_unsupported_mode_node)
    workflow.add_node("ask_for_provider", ask_for_provider_node)
    workflow.add_node("filter_and_rank", partial(filter_and_rank_node, filter_ranker=filter_ranker))
    workflow.add_node("present_results", present_results_node)
    workflow.add_node("book", partial(booking_node, booking_agent=booking_agent))

    # Define conditional logic
    def should_proceed_after_guardrail(state: AgentState) -> str:
        return "recognize_mode_provider" if state.get('guardrail_passed') else END

    def should_ask_for_provider(state: AgentState) -> str:
        return "ask_for_provider" if state.get('recognized_mode') and not state.get('recognized_provider') else "parse_query"

    def route_by_mode(state: AgentState) -> str:
        mode = state.get('recognized_mode')
        if mode in ['flight', 'train', 'bus', 'cab', 'bike']:
            return f'{mode}_search'
        return 'handle_unsupported_mode'

    def should_book(state: AgentState) -> str:
        return "book" if "book" in state.get('user_message', '').lower() else END

    # Define the edges
    workflow.set_entry_point("get_user_profile")
    workflow.add_edge("get_user_profile", "guardrail")
    workflow.add_conditional_edges("guardrail", should_proceed_after_guardrail)
    workflow.add_conditional_edges("recognize_mode_provider", should_ask_for_provider)
    workflow.add_conditional_edges("parse_query", route_by_mode)
    workflow.add_edge("flight_search", "filter_and_rank")
    workflow.add_edge("train_search", "filter_and_rank")
    workflow.add_edge("bus_search", "filter_and_rank")
    workflow.add_edge("cab_search", "filter_and_rank")
    workflow.add_edge("bike_search", "filter_and_rank")
    workflow.add_edge("handle_unsupported_mode", END)
    workflow.add_edge("ask_for_provider", END)
    workflow.add_edge("filter_and_rank", "present_results")
    workflow.add_conditional_edges("present_results", should_book)
    workflow.add_edge("book", END)

    return workflow.compile()

class GraphOrchestrator:
    def __init__(self):
        self.app = create_graph_workflow()

    async def handle_request(self, user_message: str, user_id: str) -> str:
        inputs = {"user_message": user_message, "user_id": user_id}
        result = self.app.invoke(inputs)
        return result['response']
