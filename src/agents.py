import json

class QueryParsingAgent:
    """
    Parses the user's natural language message to extract structured data.
    """
    def parse(self, message: str) -> dict:
        """
        A simple keyword-based parser.
        In a real-world scenario, this would be a sophisticated NLU model.
        """
        structured_query = {
            "mode": "unknown",
            "destination": "unknown"
        }
        message_lower = message.lower()
        if "flight" in message_lower or "fly" in message_lower:
            structured_query["mode"] = "flight"
        elif "train" in message_lower:
            structured_query["mode"] = "train"
        
        # A very basic destination extractor
        if "to " in message_lower:
            structured_query["destination"] = message_lower.split("to ")[-1].strip()

        return structured_query

class OrchestratorAgent:
    """
    The main agent that coordinates the entire booking process.
    """
    def __init__(self):
        # Initialize the specialist agents
        self.query_parser = QueryParsingAgent()
        # Other agents (Search, Filter, Booking) will be initialized here later.

    def handle_message(self, message: str) -> str:
        # 1. Parse the user's request
        structured_query = self.query_parser.parse(message)

        # 2. For now, just confirm what was understood.
        # In the future, this will trigger the Search Agent.
        response = f"Planning to search for a {structured_query['mode']} to {structured_query['destination']}."
        return response