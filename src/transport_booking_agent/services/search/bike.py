from typing import List
from ...models import StructuredQuery, TransportOption
import datetime

class BikeSearchService:
    """
    A service to search for bike rental options.
    This is a mock implementation.
    """
    def search(self, query: StructuredQuery) -> List[TransportOption]:
        # In a real implementation, this would call an external Bike Rental API
        print(f"Searching for bikes with query: {query}")
        
        # Mock response
        return [
            TransportOption(
                type='bike',
                provider='City Bikes',
                departure_time=datetime.datetime.now() + datetime.timedelta(minutes=5),
                arrival_time=datetime.datetime.now() + datetime.timedelta(minutes=25),
                price=8.00,
                booking_id='BIKE456'
            )
        ]