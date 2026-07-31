from agents.models import StructuredQuery
from datetime import datetime

class QueryParsingAgent:
    def parse_query(self, user_message: str) -> StructuredQuery:
        # Dummy implementation for now.
        # This will be replaced with actual NLP parsing later.
        print(f"Parsing user message: {user_message}")
        return StructuredQuery(
            origin="current_location",
            destination="Paris",
            date=datetime.now().isoformat(),
            passengers=1,
            mode="flight",
            preferences=["cheapest"]
        )
