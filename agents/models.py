from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StructuredQuery(BaseModel):
    origin: str
    destination: str
    date: str
    passengers: int
    mode: str
    preferences: Optional[List[str]] = None

class TransportOption(BaseModel):
    type: str
    provider: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    booking_id: Optional[str] = None

class BookingConfirmation(BaseModel):
    booking_id: str
    status: str
    message: str
