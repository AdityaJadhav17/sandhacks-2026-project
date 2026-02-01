# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Scout Agent - The "Eyes & Ears" of the Trip Planner swarm.

Role: Interfaces with the outside world (APIs) to fetch flight options.
Input: A PLAN_TRIP message containing destination, budget, and dates.
Output: Sends a FLIGHT_OPTIONS message with 5 mock flight options.
"""

import asyncio
import logging
from typing import List

from langchain_core.messages import AIMessage
from langgraph.graph import MessagesState, StateGraph, END

from ioa_observe.sdk.decorators import agent, graph

from agents.trip_planner.states import (
    TripPlannerStatus,
    FlightOption,
    TripRequest,
    build_trip_message,
    extract_trip_status,
    parse_plan_trip_request,
)

logger = logging.getLogger("lungo.trip_planner.scout")


class NodeStates:
    """Node names for the Scout agent graph."""
    SCOUT = "scout"


class GraphState(MessagesState):
    """State passed between nodes in the graph."""
    pass


@agent(name="scout_agent")
class ScoutAgent:
    """
    The Scout Agent searches for flight options.
    
    It simulates API calls to flight search services and generates
    mock flight options for demonstration purposes.
    """
    
    def __init__(self):
        """Initialize the ScoutAgent with a LangGraph workflow."""
        self.app = self._build_graph()
    
    async def _simulate_api_call(self, destination: str, dates: str) -> List[FlightOption]:
        """
        Simulate an API call to flight search services.
        
        Adds a 1-second delay to simulate network latency and returns
        5 mock flight options with varying prices and characteristics.
        """
        logger.info(f"Searching flights to {destination} on {dates}...")
        
        # Simulate API latency
        await asyncio.sleep(1)
        
        # Generate 5 mock flight options
        mock_flights = [
            # 1. Cheap & Good
            FlightOption(
                airline="Delta",
                price=450,
                departure_time="08:00 AM",
                arrival_time="04:30 PM",
                duration="8h 30m",
                stops=1,
                comfort_rating="Economy",
            ),
            # 2. Expensive (Over Budget for most requests)
            FlightOption(
                airline="Emirates",
                price=1200,
                departure_time="10:00 AM",
                arrival_time="06:00 PM",
                duration="8h 00m",
                stops=0,
                comfort_rating="Premium",
            ),
            # 3. Moderate
            FlightOption(
                airline="United",
                price=600,
                departure_time="02:00 PM",
                arrival_time="10:30 PM",
                duration="8h 30m",
                stops=1,
                comfort_rating="Economy",
            ),
            # 4. Very Cheap (Uncomfortable)
            FlightOption(
                airline="Spirit",
                price=150,
                departure_time="05:30 AM",
                arrival_time="05:00 PM",
                duration="11h 30m",
                stops=2,
                comfort_rating="Economy",
            ),
            # 5. Way Over Budget (Private Jet)
            FlightOption(
                airline="Private Jet Charter",
                price=5000,
                departure_time="Flexible",
                arrival_time="Flexible",
                duration="6h 00m",
                stops=0,
                comfort_rating="Luxury",
            ),
        ]
        
        logger.info(f"Found {len(mock_flights)} flight options")
        return mock_flights
    
    def _scout_node(self, state: GraphState) -> dict:
        """
        Main node for the Scout agent.
        
        Processes incoming PLAN_TRIP messages and generates FLIGHT_OPTIONS responses.
        Note: This is a sync wrapper that schedules the async work.
        """
        messages = state["messages"]
        if isinstance(messages, list) and messages:
            last = messages[-1]
            text = getattr(last, "content", str(last))
        else:
            text = str(messages)
        
        raw = text.strip()
        
        # Parse the trip request
        trip_request = parse_plan_trip_request(raw)
        
        if not trip_request:
            return {
                "messages": [
                    AIMessage(
                        "Scout Agent: Unable to parse trip request. "
                        "Please provide destination, budget, and dates."
                    )
                ]
            }
        
        # Run the async API simulation synchronously for the node
        loop = asyncio.new_event_loop()
        try:
            flights = loop.run_until_complete(
                self._simulate_api_call(trip_request.destination, trip_request.dates)
            )
        finally:
            loop.close()
        
        # Build the FLIGHT_OPTIONS message
        msg = build_trip_message(
            status=TripPlannerStatus.FLIGHT_OPTIONS,
            sender="Scout",
            receiver="Analyst",
            trip_request=trip_request,
            flights=flights,
            details=f"Found {len(flights)} flights to {trip_request.destination}",
        )
        
        return {"messages": [AIMessage(msg)]}
    
    @graph(name="scout_graph")
    def _build_graph(self):
        """Build and compile the LangGraph workflow."""
        workflow = StateGraph(GraphState)
        
        # Add single node
        workflow.add_node(NodeStates.SCOUT, self._scout_node)
        
        # Set entry point
        workflow.set_entry_point(NodeStates.SCOUT)
        
        # Add edge to END
        workflow.add_edge(NodeStates.SCOUT, END)
        
        return workflow.compile()
    
    async def ainvoke(self, user_message: str) -> str:
        """
        Invoke the graph with a user message.
        
        Args:
            user_message: The trip request message.
            
        Returns:
            The FLIGHT_OPTIONS message to send to the Analyst.
        """
        inputs = {"messages": [user_message]}
        result = await self.app.ainvoke(inputs)
        
        messages = result.get("messages", [])
        if not messages:
            raise RuntimeError("No messages found in the graph response.")
        
        # Find the last AIMessage with non-empty content
        for message in reversed(messages):
            if isinstance(message, AIMessage) and message.content.strip():
                logger.debug(f"Scout output: {message.content.strip()[:100]}...")
                return message.content.strip()
        
        return messages[-1].content.strip()
