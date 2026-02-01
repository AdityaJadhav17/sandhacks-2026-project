#!/usr/bin/env python3
# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Trip Planner Swarm - Main Entry Point

Run the complete trip planning pipeline with three specialized agents:
1. Scout Agent - Searches for flight options
2. Analyst Agent - Filters and ranks by budget
3. Planner Agent - Creates the final itinerary

Usage:
    python -m agents.trip_planner.main
    
    Or with custom parameters:
    python -m agents.trip_planner.main --destination Tokyo --budget 1000 --dates 2026-04-15
"""

import asyncio
import argparse
import logging

from agents.trip_planner import run_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Trip Planner Agent Swarm",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m agents.trip_planner.main
    python -m agents.trip_planner.main --destination Paris --budget 800 --dates 2026-03-10
    python -m agents.trip_planner.main -d Tokyo -b 1200 --dates 2026-05-01
        """
    )
    parser.add_argument(
        "-d", "--destination",
        type=str,
        default="Paris",
        help="Travel destination (default: Paris)"
    )
    parser.add_argument(
        "-b", "--budget",
        type=int,
        default=800,
        help="Maximum budget in dollars (default: 800)"
    )
    parser.add_argument(
        "--dates",
        type=str,
        default="2026-03-10",
        help="Travel date in YYYY-MM-DD format (default: 2026-03-10)"
    )
    return parser.parse_args()


async def main():
    """Main entry point for the trip planner swarm."""
    args = parse_args()
    
    print("\n" + "=" * 70)
    print("        ✈️  TRIP PLANNER AGENT SWARM  ✈️")
    print("=" * 70)
    print("\nThis demo shows a 3-agent pipeline working together:")
    print("  1. Scout Agent  - Searches for flights (simulated API)")
    print("  2. Analyst Agent - Filters by budget, sorts by price")
    print("  3. Planner Agent - Creates beautiful itinerary output")
    print("\n" + "-" * 70)
    
    # Run the pipeline
    result = await run_pipeline(
        destination=args.destination,
        budget=args.budget,
        dates=args.dates
    )
    
    print("\n" + "=" * 70)
    print("        ✨ PIPELINE COMPLETE ✨")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Pipeline interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        raise
