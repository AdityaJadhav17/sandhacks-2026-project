# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Travel Agent Module

This module contains the travel agent implementation for searching flights and hotels
using SerpAPI, and finding the cheapest travel plan with timing constraints.

Key components:
- serpapi_tools: Functions to search flights and hotels via SerpAPI
- travel_logic: Business logic for filtering hotels and finding optimal plans
"""

from agents.travel.serpapi_tools import search_flights, search_hotels
from agents.travel.travel_logic import (
    extract_arrival_datetime,
    filter_valid_hotels,
    find_cheapest_plan,
)

__all__ = [
    "search_flights",
    "search_hotels",
    "extract_arrival_datetime",
    "filter_valid_hotels",
    "find_cheapest_plan",
]
