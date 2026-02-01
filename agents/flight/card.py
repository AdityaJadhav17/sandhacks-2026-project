# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Flight Search Agent Card

A2A Agent Card that describes the Flight Search Agent's capabilities
and connection information for the A2A protocol.
"""

from a2a.types import AgentCard, AgentCapabilities, AgentSkill

# Agent Card for the Flight Search Agent
# This is used by other agents to discover and communicate with this agent
AGENT_CARD = AgentCard(
    name="Flight Search Agent",
    description="An AI agent that searches for flights using SerpAPI Google Flights.",
    url="http://flight-agent:9001",  # Docker service URL
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="search_flights",
            name="Search Flights",
            description="Search for flights between two locations using SerpAPI.",
            tags=["travel", "flights", "search"],
        )
    ],
)
