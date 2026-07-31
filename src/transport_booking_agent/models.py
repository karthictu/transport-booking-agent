from pydantic import BaseModel
from typing import List, Optional, TypedDict, Any
from datetime import datetime

class StructuredQuery(BaseModel):
    origin: str
    destination: str
    date: str
    passengers: int
    mode: str
    preferences: Optional[List[str]] = None
    provider: Optional[str] = None

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

class AgentState(TypedDict):
    user_message: str
    user_id: str
    structured_query: Optional[StructuredQuery]
    transport_options: Optional[List[TransportOption]]
    filtered_transport_options: Optional[List[TransportOption]]
    booking_confirmation: Optional[BookingConfirmation]
    response: str
    user_profile: Optional[Dict[str, Any]]
    guardrail_passed: Optional[bool]
    recognized_mode: Optional[str]
    recognized_provider: Optional[str]
