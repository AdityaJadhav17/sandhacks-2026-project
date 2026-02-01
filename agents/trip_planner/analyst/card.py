# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

AGENT_SKILL = AgentSkill(
    id="analyze_flights",
    name="Analyze Flight Options",
    description="Analyzes flight options, filters by budget constraints, and selects the best value options.",
    tags=["travel", "analysis", "filtering"],
    examples=[
        "Filter these flights for a $800 budget",
        "Analyze flight options and pick the best two",
        "Which flights are within my budget?",
        "Sort these flights by price and recommend the cheapest",
        "Remove flights that exceed my budget limit",
    ],
)

AGENT_CARD = AgentCard(
    name="Analyst Agent",
    id="analyst-agent",
    description="The Analyst Agent applies budget constraints and logic to filter, sort, and select the best flight options from the Scout's search results.",
    url="",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    capabilities=AgentCapabilities(streaming=True),
    skills=[AGENT_SKILL],
    supportsAuthenticatedExtendedCard=False,
)
