from agents.query_parsing_agent import QueryParsingAgent
from agents.search_agent import SearchAgent
from agents.filtering_ranking_agent import FilteringRankingAgent
from agents.booking_agent import BookingAgent
from agents.user_profile_agent import UserProfileAgent
from agents.models import StructuredQuery, TransportOption, BookingConfirmation
from typing import List

class OrchestratorAgent:
    def __init__(self):
        self.query_parser = QueryParsingAgent()
        self.search_agent = SearchAgent()
        self.filter_ranker = FilteringRankingAgent()
        self.booking_agent = BookingAgent()
        self.user_profile_agent = UserProfileAgent()

    async def handle_request(self, user_message: str, user_id: str) -> str:
        # 1. Receive user message and get user profile
        print(f"Orchestrator received message: '{user_message}' for user: {user_id}")
        user_profile = self.user_profile_agent.get_user_profile(user_id)
        print(f"User profile: {user_profile}")

        # 2. Delegate to QueryParsingAgent to structure the request
        structured_query: StructuredQuery = self.query_parser.parse_query(user_message)
        print(f"Structured Query: {structured_query.dict()}")

        # 3. Based on the structured query, delegate to SearchAgent
        # Incorporate user preferences into the structured query for search
        if user_profile.get("preferences"):
            structured_query.preferences = list(set(structured_query.preferences or []) | set(user_profile["preferences"]))
        
        transport_options: List[TransportOption] = self.search_agent.search_transport(structured_query)
        print(f"Found {len(transport_options)} transport options.")

        # 4. Delegate to Filtering & RankingAgent to process search results
        # For now, just pass the preferences from the structured query
        filtered_ranked_options: List[TransportOption] = self.filter_ranker.filter_and_rank(
            transport_options, structured_query.preferences or []
        )
        print(f"Filtered and ranked {len(filtered_ranked_options)} options.")

        # 5. Present results to the user (simplified for now)
        if not filtered_ranked_options:
            return "No transport options found for your request."

        response_message = "Here are some options:
"
        for i, option in enumerate(filtered_ranked_options[:3]): # Show top 3 options
            response_message += (
                f"{i+1}. {option.type} with {option.provider} from "
                f"{option.departure_time.strftime('%H:%M')} to {option.arrival_time.strftime('%H:%M')} "
                f"for ${option.price:.2f}
"
            )
        response_message += "Which one would you like to book? (e.g., 'Book option 1')"

        # This part assumes a subsequent user message will trigger booking
        # For a full implementation, this would involve session management and state.
        
        return response_message

    async def handle_booking_request(self, user_message: str, user_id: str, selected_option: TransportOption) -> str:
        user_profile = self.user_profile_agent.get_user_profile(user_id)
        user_details = user_profile.get("personal_info", {})

        booking_confirmation: BookingConfirmation = self.booking_agent.book_transport(selected_option, user_details)
        
        if booking_confirmation.status == "Confirmed":
            return f"Your flight is booked! {booking_confirmation.message} Booking ID: {booking_confirmation.booking_id}"
        else:
            return f"Booking failed: {booking_confirmation.message}"

