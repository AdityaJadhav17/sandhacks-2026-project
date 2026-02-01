# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Analyst Agent - The "Brain" of the Trip Planner swarm.

Role: Applies constraints and logic to filter and rank flight options.
Input: A FLIGHT_OPTIONS message from the Scout containing raw flight data.
Output: Sends a FILTERED_OPTIONS message with the top 2 approved flights.
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

logger = logging.getLogger("lungo.trip_planner.analyst")


class NodeStates:
    """Node names for the Analyst agent graph."""
    ANALYST = "analyst"


class GraphState(MessagesState):
    """State passed between nodes in the graph."""
    pass


@agent(name="analyst_agent")
class AnalystAgent:
    """
    The Analyst Agent filters and ranks flight options.
    
    It applies budget constraints, sorts by price, and selects
    the best options for the user.
    """
    
    def __init__(self):
        """Initialize the AnalystAgent with a LangGraph workflow."""
        self.app = self._build_graph()
    
    def _filter_by_budget(
        self, flights: List[FlightOption], budget: int
    ) -> List[FlightOption]:
        """
        Filter flights to only include those within budget.
        
        Args:
            flights: List of flight options to filter.
            budget: Maximum price allowed.
            
        Returns:
            List of flights where price <= budget.
        """
        filtered = [f for f in flights if f.price <= budget]
        logger.info(
            f"Filtered {len(flights)} flights to {len(filtered)} within budget ${budget}"
        )
        return filtered
    
    def _sort_by_price(self, flights: List[FlightOption]) -> List[FlightOption]:
        """
        Sort flights by price, lowest first.
        
        Args:
            flights: List of flight options to sort.
            
        Returns:
            Sorted list of flights (lowest price first).
        """
        return sorted(flights, key=lambda f: f.price)
    
    def _select_top_n(
        self, flights: List[FlightOption], n: int = 2
    ) -> List[FlightOption]:
        """
        Select the top N flight options.
        
        Args:
            flights: List of flight options (should be pre-sorted).
            n: Number of options to select.
            
        Returns:
            Top N flight options.
        """
        return flights[:n]
    
    def _analyst_node(self, state: GraphState) -> dict:
        """
        Main node for the Analyst agent.
        
        Processes FLIGHT_OPTIONS messages and produces FILTERED_OPTIONS.
        """
        messages = state["messages"]
        if isinstance(messages, list) and messages:
            last = messages[-1]
            text = getattr(last, "content", str(last))
        else:
            text = str(messages)
        
        raw = text.strip()
        status = extract_trip_status(raw)
        
        # Validate we received FLIGHT_OPTIONS
        if status != TripPlannerStatus.FLIGHT_OPTIONS:
            return {
                "messages": [
                    AIMessage(
                        "Analyst Agent: Expected FLIGHT_OPTIONS message. "
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
                    AIMessage("Analyst Agent: Unable to extract trip request from message.")
                ]
            }
        
        if not flights:
            return {
                "messages": [
                    AIMessage("Analyst Agent: No flight options found in message.")
                ]
            }
        
        logger.info(f"Analyst processing {len(flights)} flights for budget ${trip_request.budget}")
        
        # Step 1: Filter by budget
        budget_filtered = self._filter_by_budget(flights, trip_request.budget)
        
        if not budget_filtered:
            return {
                "messages": [
                    AIMessage(
                        f"Analyst Agent: No flights found within budget ${trip_request.budget}. "
                        "Consider increasing your budget."
                    )
                ]
            }
        
        # Step 2: Sort by price (lowest first)
        sorted_flights = self._sort_by_price(budget_filtered)
        
        # Step 3: Select top 2 options
        top_flights = self._select_top_n(sorted_flights, n=2)
        
        # Build summary of filtering
        dropped_count = len(flights) - len(budget_filtered)
        details = (
            f"Analyzed {len(flights)} options, dropped {dropped_count} over budget. "
            f"Selected top {len(top_flights)} best-value flights."
        )
        
        # Build the FILTERED_OPTIONS message
        msg = build_trip_message(
            status=TripPlannerStatus.FILTERED_OPTIONS,
            sender="Analyst",
            receiver="Planner",
            trip_request=trip_request,
            flights=top_flights,
            details=details,
        )
        
        return {"messages": [AIMessage(msg)]}
    
    @graph(name="analyst_graph")
    def _build_graph(self):
        """Build and compile the LangGraph workflow."""
        workflow = StateGraph(GraphState)
        
        # Add single node
        workflow.add_node(NodeStates.ANALYST, self._analyst_node)
        
        # Set entry point
        workflow.set_entry_point(NodeStates.ANALYST)
        
        # Add edge to END
        workflow.add_edge(NodeStates.ANALYST, END)
        
        return workflow.compile()
    
    async def ainvoke(self, user_message: str) -> str:
        """
        Invoke the graph with a user message.
        
        Args:
            user_message: The FLIGHT_OPTIONS message from Scout.
            
        Returns:
            The FILTERED_OPTIONS message to send to the Planner.
        """
        inputs = {"messages": [user_message]}
        result = await self.app.ainvoke(inputs)
        
        messages = result.get("messages", [])
        if not messages:
            raise RuntimeError("No messages found in the graph response.")
        
        # Find the last AIMessage with non-empty content
        for message in reversed(messages):
            if isinstance(message, AIMessage) and message.content.strip():
                logger.debug(f"Analyst output: {message.content.strip()[:100]}...")
                return message.content.strip()
        
        return messages[-1].content.strip()
