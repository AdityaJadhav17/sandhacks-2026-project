# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

AGENT_SKILL = AgentSkill(
    id="search_flights",
    name="Search Flights",
    description="Searches for flight options to a given destination within budget constraints.",
    tags=["travel", "flights", "search"],
    examples=[
        "Plan a trip to Paris with budget $800 on 2026-03-10",
        "Find flights to Tokyo with a $1000 budget for March 15",
        "Search for flight options to London, budget $600, departing 2026-04-01",
        "I want to fly to Rome with $500 budget on March 20th",
        "Look up flights to Barcelona for $750 on 2026-03-25",
    ],
)

AGENT_CARD = AgentCard(
    name="Scout Agent",
    id="scout-agent",
    description="The Scout Agent searches for flight options by interfacing with flight search APIs. It returns a list of available flights for further analysis.",
    url="",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)
