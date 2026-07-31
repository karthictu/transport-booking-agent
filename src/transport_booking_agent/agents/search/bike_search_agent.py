from typing import List
from ...models import StructuredQuery, TransportOption
import datetime

class BikeSearchAgent:
    """
    An agent to search for motorcycle rental options.
    This is a mock implementation.
    """
    def search(self, query: StructuredQuery) -> List[TransportOption]:
        # In a real implementation, this would call an external Motorcycle Rental API
        print(f"Searching for motorcycles with query: {query}")
        
        # Mock response
        return [
            TransportOption(
                type='bike',
                provider='City Motorcycles',
                departure_time=datetime.datetime.now() + datetime.timedelta(minutes=5),
                arrival_time=datetime.datetime.now() + datetime.timedelta(minutes=25),
                price=8.00,
                booking_id='BIKE456'
            )
        ]