# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Travel Supervisor Module

This supervisor agent handles travel planning requests by:
1. Parsing user input to extract trip parameters (origin, destination, dates)
2. Searching for flights and hotels via SerpAPI
3. Finding the cheapest combination that meets timing constraints
4. Returning an optimal travel plan to the user

The supervisor uses LangGraph for workflow orchestration and state management.
"""
