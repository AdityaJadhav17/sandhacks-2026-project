# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Planner Agent - The "Voice" of the Trip Planner swarm.

Role: Creates the final user experience with a beautiful, readable itinerary.
Input: A FILTERED_OPTIONS message from the Analyst with approved flights.
Output: A beautifully formatted trip summary (console print) and TRIP_FINALIZED message.
"""

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
    extract_trip_request,
    extract_flights,
)

logger = logging.getLogger("lungo.trip_planner.planner")


class NodeStates:
    """Node names for the Planner agent graph."""
    PLANNER = "planner"


class GraphState(MessagesState):
    """State passed between nodes in the graph."""
    pass


@agent(name="planner_agent")
class PlannerAgent:
    """
    The Planner Agent creates the final user-facing output.
    
    It formats the approved flight options into a beautiful,
    readable itinerary with savings calculations.
    """
    
    def __init__(self):
        """Initialize the PlannerAgent with a LangGraph workflow."""
        self.app = self._build_graph()
    
    def _format_flight_card(self, flight: FlightOption, rank: int) -> str:
        """
        Format a single flight option as a display card.
        
        Args:
            flight: The flight option to format.
            rank: The ranking (1 = best, 2 = second best, etc.)
            
        Returns:
            A formatted string for the flight.
        """
        rank_emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "✈️"
        
        card = f"""
    {rank_emoji} Option {rank}: {flight.airline}
    ┌─────────────────────────────────────────┐
    │  💰 Price: ${flight.price:,}                    
    │  🛫 Departure: {flight.departure_time}          
    │  🛬 Arrival: {flight.arrival_time}              
    │  ⏱️  Duration: {flight.duration}                
    │  🔄 Stops: {flight.stops}                       
    │  💺 Class: {flight.comfort_rating}              
    └─────────────────────────────────────────┘"""
        return card
    
    def _format_itinerary(
        self,
        trip_request: TripRequest,
        flights: List[FlightOption],
    ) -> str:
        """
        Create a beautiful, formatted itinerary.
        
        Args:
            trip_request: The original trip request.
            flights: The approved flight options.
            
        Returns:
            A beautifully formatted itinerary string.
        """
        # Calculate savings
        best_price = flights[0].price if flights else 0
        savings = trip_request.budget - best_price
        savings_pct = (savings / trip_request.budget * 100) if trip_request.budget > 0 else 0
        
        # Build the header
        header = f"""
╔══════════════════════════════════════════════════════════════╗
║                    ✈️  YOUR TRIP TO {trip_request.destination.upper():^12} ✈️                ║
╠══════════════════════════════════════════════════════════════╣
║  📅 Travel Date: {trip_request.dates:<20}                     ║
║  💵 Your Budget: ${trip_request.budget:,:<20}                     ║
╚══════════════════════════════════════════════════════════════╝
"""
        
        # Build flight cards
        flight_cards = "\n".join(
            self._format_flight_card(flight, i + 1)
            for i, flight in enumerate(flights)
        )
        
        # Build the savings summary
        savings_section = f"""
┌─────────────────────────────────────────────────────────────┐
│                      💰 SAVINGS SUMMARY 💰                   │
├─────────────────────────────────────────────────────────────┤
│  Your Budget:          ${trip_request.budget:,}                           │
│  Best Flight Price:    ${best_price:,}                           │
│  ─────────────────────────────────────                      │
│  💸 YOU SAVE:          ${savings:,} ({savings_pct:.1f}%)                      │
└─────────────────────────────────────────────────────────────┘
"""
        
        # Build recommendation
        if flights:
            best = flights[0]
            recommendation = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 OUR RECOMMENDATION 🎯                   ║
╠══════════════════════════════════════════════════════════════╣
║  Book {best.airline} for ${best.price:,}!                                 ║
║  Departs {best.departure_time}, arrives {best.arrival_time}              ║
║  Save ${savings:,} from your ${trip_request.budget:,} budget!                       ║
╚══════════════════════════════════════════════════════════════╝

🎉 Happy travels to {trip_request.destination}! 🎉
"""
        else:
            recommendation = "\n⚠️ No flights available within your budget.\n"
        
        return header + flight_cards + savings_section + recommendation
    
    def _planner_node(self, state: GraphState) -> dict:
        """
        Main node for the Planner agent.
        
        Processes FILTERED_OPTIONS messages and creates the final output.
        """
        messages = state["messages"]
        if isinstance(messages, list) and messages:
            last = messages[-1]
            text = getattr(last, "content", str(last))
        else:
            text = str(messages)
        
        raw = text.strip()
        status = extract_trip_status(raw)
        
        # Validate we received FILTERED_OPTIONS
        if status != TripPlannerStatus.FILTERED_OPTIONS:
            return {
                "messages": [
                    AIMessage(
                        "Planner Agent: Expected FILTERED_OPTIONS message. "
                        f"Received status: {status}"
                    )
                ]
            }
        
        # Extract trip request and flights from the message
        trip_request = extract_trip_request(raw)
        flights = extract_flights(raw)
        
        if not trip_request:
            return {
                "messages": [
                    AIMessage("Planner Agent: Unable to extract trip request from message.")
                ]
            }
        
        logger.info(f"Planner creating itinerary for {trip_request.destination}")
        
        # Format the beautiful itinerary
        itinerary = self._format_itinerary(trip_request, flights)
        
        # Print to console (the "Aha!" moment)
        print(itinerary)
        
        # Also build a TRIP_FINALIZED message for any downstream systems
        best_flight = flights[0] if flights else None
        savings = trip_request.budget - best_flight.price if best_flight else 0
        
        details = (
            f"Trip to {trip_request.destination} finalized! "
            f"Best option: {best_flight.airline} at ${best_flight.price}, "
            f"saving ${savings} from budget."
        ) if best_flight else "No suitable flights found."
        
        finalized_msg = build_trip_message(
            status=TripPlannerStatus.TRIP_FINALIZED,
            sender="Planner",
            receiver="User",
            trip_request=trip_request,
            flights=flights,
            details=details,
        )
        
        # Return both the formatted itinerary and the structured message
        combined_output = f"{itinerary}\n\n---\nStructured Output:\n{finalized_msg}"
        
        return {"messages": [AIMessage(combined_output)]}
    
    @graph(name="planner_graph")
    def _build_graph(self):
        """Build and compile the LangGraph workflow."""
        workflow = StateGraph(GraphState)
        
        # Add single node
        workflow.add_node(NodeStates.PLANNER, self._planner_node)
        
        # Set entry point
        workflow.set_entry_point(NodeStates.PLANNER)
        
        # Add edge to END
        workflow.add_edge(NodeStates.PLANNER, END)
        
        return workflow.compile()
    
    async def ainvoke(self, user_message: str) -> str:
        """
        Invoke the graph with a user message.
        
        Args:
            user_message: The FILTERED_OPTIONS message from Analyst.
            
        Returns:
            The formatted itinerary and TRIP_FINALIZED message.
        """
        inputs = {"messages": [user_message]}
        result = await self.app.ainvoke(inputs)
        
        messages = result.get("messages", [])
        if not messages:
            raise RuntimeError("No messages found in the graph response.")
        
        # Find the last AIMessage with non-empty content
        for message in reversed(messages):
            if isinstance(message, AIMessage) and message.content.strip():
                logger.debug(f"Planner output generated")
                return message.content.strip()
        
        return messages[-1].content.strip()
