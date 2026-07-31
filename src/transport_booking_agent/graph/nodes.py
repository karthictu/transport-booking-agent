from typing import List
from ..models import AgentState, StructuredQuery, TransportOption, BookingConfirmation

# Node functions

def get_user_profile_node(state: AgentState, user_profile_agent) -> AgentState:
    print("---GET USER PROFILE---")
    user_profile = user_profile_agent.get_user_profile(state['user_id'])
    state['user_profile'] = user_profile
    return state

def guardrail_node(state: AgentState, guardrail_agent) -> AgentState:
    print("---CHECKING GUARDRAILS---")
    guardrail_passed = guardrail_agent.check_guardrails(state['user_message'], state['user_profile'])
    state['guardrail_passed'] = guardrail_passed
    if not guardrail_passed:
        state['response'] = "Your request has been blocked by our safety guardrails."
    return state

def recognize_mode_provider_node(state: AgentState, mode_provider_recognition_agent) -> AgentState:
    print("---RECOGNIZING MODE AND PROVIDER---")
    mode, provider = mode_provider_recognition_agent.recognize(state['user_message'], state['user_profile'])
    state['recognized_mode'] = mode
    state['recognized_provider'] = provider
    return state

def parse_query_node(state: AgentState, query_parser) -> AgentState:
    print("---PARSE QUERY---")
    structured_query: StructuredQuery = query_parser.parse_query(
        state['user_message'],
        recognized_mode=state.get('recognized_mode'),
        recognized_provider=state.get('recognized_provider'))
    state['structured_query'] = structured_query
    return state

def flight_search_node(state: AgentState, flight_search_agent) -> AgentState:
    print("---SEARCHING FOR FLIGHTS---")
    transport_options: List[TransportOption] = flight_search_agent.search(state['structured_query'])
    state['transport_options'] = transport_options
    return state

def train_search_node(state: AgentState, train_search_agent) -> AgentState:
    print("---SEARCHING FOR TRAINS---")
    transport_options: List[TransportOption] = train_search_agent.search(state['structured_query'])
    state['transport_options'] = transport_options
    return state

def bus_search_node(state: AgentState, bus_search_agent) -> AgentState:
    print("---SEARCHING FOR BUSES---")
    transport_options: List[TransportOption] = bus_search_agent.search(state['structured_query'])
    state['transport_options'] = transport_options
    return state

def handle_unsupported_mode_node(state: AgentState) -> AgentState:
    print("---HANDLING UNSUPPORTED MODE---")
    state['response'] = "Sorry, I can only handle flight, train, and bus requests at the moment."
    return state

def ask_for_provider_node(state: AgentState) -> AgentState:
    print("---ASKING FOR PROVIDER---")
    mode = state.get('recognized_mode', 'transport')
    state['response'] = f"Which {mode} provider are you looking for?"
    return state

def filter_and_rank_node(state: AgentState, filter_ranker) -> AgentState:
    print("---FILTER AND RANK---")
    filtered_ranked_options: List[TransportOption] = filter_ranker.filter_and_rank(
        state['transport_options'], state['structured_query'].preferences or []
    )
    state['filtered_transport_options'] = filtered_ranked_options
    return state

def present_results_node(state: AgentState) -> AgentState:
    print("---PRESENT RESULTS---")
    if not state['filtered_transport_options']:
        state['response'] = "No transport options found for your request."
        return state

    response_message = "Here are some options:\n"
    for i, option in enumerate(state['filtered_transport_options'][:3]): # Show top 3 options
        response_message += (
            f"{i+1}. {option.type} with {option.provider} from "
            f"{option.departure_time.strftime('%H:%M')} to {option.arrival_time.strftime('%H:%M')} "
            f"for ${option.price:.2f}\n"
        )
    response_message += "Which one would you like to book? (e.g., 'Book option 1')"
    state['response'] = response_message
    return state

def booking_node(state: AgentState, booking_agent) -> AgentState:
    print("---BOOKING---")
    # This is a simplified version. In a real scenario, we would have a way to select an option.
    selected_option = state['filtered_transport_options'][0]
    user_profile = state['user_profile']
    user_details = user_profile.get("personal_info", {})

    booking_confirmation: BookingConfirmation = booking_agent.book_transport(selected_option, user_details)
    
    if booking_confirmation.status == "Confirmed":
        state['response'] = f"Your flight is booked! {booking_confirmation.message} Booking ID: {booking_confirmation.booking_id}"
    else:
        state['response'] = f"Booking failed: {booking_confirmation.message}"
    return state