# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Shared states and message utilities for the Trip Planner agent swarm.
Defines message types and helper functions for agent communication.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import json
import re


class TripPlannerStatus(str, Enum):
    """Status enum for trip planning workflow states."""
    PLAN_TRIP = "PLAN_TRIP"
    FLIGHT_OPTIONS = "FLIGHT_OPTIONS"
    FILTERED_OPTIONS = "FILTERED_OPTIONS"
    TRIP_FINALIZED = "TRIP_FINALIZED"


@dataclass
class FlightOption:
    """Represents a single flight option."""
    airline: str
    price: int
    departure_time: str
    arrival_time: str
    duration: str
    stops: int
    comfort_rating: str  # "Economy", "Premium", "Luxury"
    
    def to_dict(self) -> dict:
        return {
            "airline": self.airline,
            "price": self.price,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "duration": self.duration,
            "stops": self.stops,
            "comfort_rating": self.comfort_rating,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FlightOption":
        return cls(
            airline=data["airline"],
            price=data["price"],
            departure_time=data["departure_time"],
            arrival_time=data["arrival_time"],
            duration=data["duration"],
            stops=data["stops"],
            comfort_rating=data["comfort_rating"],
        )


@dataclass
class TripRequest:
    """Represents a trip planning request."""
    destination: str
    budget: int
    dates: str
    
    def to_dict(self) -> dict:
        return {
            "destination": self.destination,
            "budget": self.budget,
            "dates": self.dates,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "TripRequest":
        return cls(
            destination=data["destination"],
            budget=data["budget"],
            dates=data["dates"],
        )


def build_trip_message(
    status: TripPlannerStatus,
    sender: str,
    receiver: str,
    trip_request: Optional[TripRequest] = None,
    flights: Optional[List[FlightOption]] = None,
    details: str = "",
) -> str:
    """
    Build a structured message for trip planner agent communication.
    
    Format: STATUS | Sender -> Receiver: {JSON payload}
    """
    payload = {
        "details": details,
    }
    
    if trip_request:
        payload["trip_request"] = trip_request.to_dict()
    
    if flights:
        payload["flights"] = [f.to_dict() for f in flights]
    
    return f"{status.value} | {sender} -> {receiver}: {json.dumps(payload)}"


def extract_trip_status(message: str) -> Optional[TripPlannerStatus]:
    """Extract the status from a trip planner message."""
    for status in TripPlannerStatus:
        if message.strip().startswith(status.value):
            return status
    return None


def extract_trip_payload(message: str) -> dict:
    """Extract the JSON payload from a trip planner message."""
    try:
        # Find the JSON part after the colon
        match = re.search(r':\s*(\{.*\})\s*$', message, re.DOTALL)
        if match:
            return json.loads(match.group(1))
    except (json.JSONDecodeError, AttributeError):
        pass
    return {}


def extract_trip_request(message: str) -> Optional[TripRequest]:
    """Extract TripRequest from message payload."""
    payload = extract_trip_payload(message)
    if "trip_request" in payload:
        return TripRequest.from_dict(payload["trip_request"])
    return None


def extract_flights(message: str) -> List[FlightOption]:
    """Extract list of FlightOptions from message payload."""
    payload = extract_trip_payload(message)
    if "flights" in payload:
        return [FlightOption.from_dict(f) for f in payload["flights"]]
    return []


def parse_plan_trip_request(message: str) -> Optional[TripRequest]:
    """
    Parse a natural language trip request.
    
    Expected format examples:
    - "Plan a trip to Paris with budget $800 on 2026-03-10"
    - "PLAN_TRIP | User -> Scout: {destination: Paris, budget: 800, dates: 2026-03-10}"
    """
    # First try to extract from structured message
    trip_request = extract_trip_request(message)
    if trip_request:
        return trip_request
    
    # Try to parse natural language
    message_lower = message.lower()
    
    # Extract destination
    dest_patterns = [
        r'trip to (\w+)',
        r'destination[:\s]+(\w+)',
        r'fly to (\w+)',
        r'going to (\w+)',
    ]
    destination = None
    for pattern in dest_patterns:
        match = re.search(pattern, message_lower)
        if match:
            destination = match.group(1).capitalize()
            break
    
    # Extract budget
    budget_patterns = [
        r'budget[:\s]*\$?(\d+)',
        r'\$(\d+)',
        r'(\d+)\s*dollars',
    ]
    budget = None
    for pattern in budget_patterns:
        match = re.search(pattern, message_lower)
        if match:
            budget = int(match.group(1))
            break
    
    # Extract dates
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',
        r'on (\w+ \d+)',
        r'dates?[:\s]+(\S+)',
    ]
    dates = None
    for pattern in date_patterns:
        match = re.search(pattern, message)
        if match:
            dates = match.group(1)
            break
    
    if destination and budget and dates:
        return TripRequest(destination=destination, budget=budget, dates=dates)
    
    return None
