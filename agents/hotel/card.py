# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Hotel Search Agent Card

A2A Agent Card that describes the Hotel Search Agent's capabilities
and connection information for the A2A protocol.
"""

from a2a.types import AgentCard, AgentCapabilities, AgentSkill

# Agent Card for the Hotel Search Agent
# This is used by other agents to discover and communicate with this agent
AGENT_CARD = AgentCard(
    name="Hotel Search Agent",
    description="An AI agent that searches for hotels using SerpAPI Google Hotels.",
    url="http://hotel-agent:9002",  # Docker service URL
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="search_hotels",
            name="Search Hotels",
            description="Search for hotels at a location using SerpAPI.",
            tags=["travel", "hotels", "search"],
        )
    ],
)
