# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Activity Search Agent Card

A2A Agent Card that describes the Activity Search Agent's capabilities
and connection information for the A2A protocol.
"""

from a2a.types import AgentCard, AgentCapabilities, AgentSkill

# Agent Card for the Activity Search Agent
# This is used by other agents to discover and communicate with this agent
AGENT_CARD = AgentCard(
    name="Activity Search Agent",
    description="An AI agent that searches for activities, attractions, and things to do using SerpAPI Google Local.",
    url="http://activity-agent:9003",  # Docker service URL
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="search_activities",
            name="Search Activities",
            description="Search for activities, attractions, and things to do at a location using SerpAPI.",
            tags=["travel", "activities", "attractions", "search"],
        )
    ],
)
