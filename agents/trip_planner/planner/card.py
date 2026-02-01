# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

AGENT_SKILL = AgentSkill(
    id="create_itinerary",
    name="Create Travel Itinerary",
    description="Creates a beautiful, formatted travel itinerary with flight details and savings summary.",
    tags=["travel", "planning", "itinerary"],
    examples=[
        "Create an itinerary for my Paris trip",
        "Show me my travel summary",
        "Format the flight options into a readable plan",
        "How much will I save on this trip?",
        "Generate the final trip recommendation",
    ],
)

AGENT_CARD = AgentCard(
    name="Planner Agent",
    id="planner-agent",
    description="The Planner Agent creates the final user experience by formatting approved flight options into a beautiful, readable itinerary with savings calculations.",
    url="",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)
