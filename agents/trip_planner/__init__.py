# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Trip Planner Agent Swarm

A three-agent pipeline for planning trips:
1. Scout Agent - Searches for flight options (mock API)
2. Analyst Agent - Filters and ranks options by budget
3. Planner Agent - Creates beautiful itinerary output

Usage:
    from agents.trip_planner import run_pipeline
    
    await run_pipeline(
        destination="Paris",
        budget=800,
        dates="2026-03-10"
    )
"""

from agents.trip_planner.states import (
    TripPlannerStatus,
    FlightOption,
    TripRequest,
)
from agents.trip_planner.scout.agent import ScoutAgent
from agents.trip_planner.analyst.agent import AnalystAgent
from agents.trip_planner.planner.agent import PlannerAgent

__all__ = [
    "TripPlannerStatus",
    "FlightOption",
    "TripRequest",
    "ScoutAgent",
    "AnalystAgent",
    "PlannerAgent",
    "run_pipeline",
]


async def run_pipeline(destination: str, budget: int, dates: str) -> str:
    """
    Run the complete trip planning pipeline.
    
    This orchestrates the three agents in sequence:
    Scout -> Analyst -> Planner
    
    Args:
        destination: Where you want to go (e.g., "Paris")
        budget: Maximum amount to spend (e.g., 800)
        dates: Travel date (e.g., "2026-03-10")
        
    Returns:
        The final formatted itinerary.
    """
    # Initialize agents
    scout = ScoutAgent()
    analyst = AnalystAgent()
    planner = PlannerAgent()
    
    # Build the initial request
    initial_request = f"Plan a trip to {destination} with budget ${budget} on {dates}"
    
    print(f"\n{'='*60}")
    print(f"🚀 Starting Trip Planning Pipeline")
    print(f"{'='*60}")
    print(f"📍 Destination: {destination}")
    print(f"💰 Budget: ${budget}")
    print(f"📅 Date: {dates}")
    print(f"{'='*60}\n")
    
    # Stage 1: Scout searches for flights
    print("📡 Stage 1: Scout Agent searching for flights...")
    scout_output = await scout.ainvoke(initial_request)
    print("✅ Scout found flight options\n")
    
    # Stage 2: Analyst filters and ranks
    print("🧠 Stage 2: Analyst Agent filtering options...")
    analyst_output = await analyst.ainvoke(scout_output)
    print("✅ Analyst selected best options\n")
    
    # Stage 3: Planner creates the final output
    print("📝 Stage 3: Planner Agent creating itinerary...")
    planner_output = await planner.ainvoke(analyst_output)
    print("✅ Planner completed!\n")
    
    return planner_output
