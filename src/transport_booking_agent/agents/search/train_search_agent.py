from ....models import StructuredQuery, TransportOption
from datetime import datetime, timedelta
from typing import List

class TrainSearchAgent:
    def search(self, query: StructuredQuery) -> List[TransportOption]:
        """
        Searches for trains based on the query.
        
        For now, this is a dummy implementation.
        """
        print(f"Searching for trains with query: {query}")
        
        # Create some dummy train options
        options = [
            TransportOption(
                type="train",
                provider="Dummy Rail",
                departure_time=datetime.now() + timedelta(hours=1),
                arrival_time=datetime.now() + timedelta(hours=4),
                price=100.0,
                booking_id="DR123"
            ),
            TransportOption(
                type="train",
                provider="Another Dummy Rail",
                departure_time=datetime.now() + timedelta(hours=1, minutes=30),
                arrival_time=datetime.now() + timedelta(hours=4, minutes=30),
                price=120.0,
                booking_id="ADR456"
            )
        ]
        return options