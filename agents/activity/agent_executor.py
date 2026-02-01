# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Activity Search Agent Executor

A2A AgentExecutor that handles incoming activity search requests.
"""

import logging
from uuid import uuid4

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    UnsupportedOperationError,
    JSONRPCResponse,
    ContentTypeNotSupportedError,
    InternalError,
    Message,
    Role,
    Part,
    TextPart,
    Task,
)
from a2a.utils import new_task
from a2a.utils.errors import ServerError

from agents.activity.agent import ActivitySearchAgent
from agents.activity.card import AGENT_CARD

logger = logging.getLogger("lungo.activity.agent_executor")


class ActivityAgentExecutor(AgentExecutor):
    """A2A executor for the Activity Search Agent."""
    
    def __init__(self):
        self.agent = ActivitySearchAgent()
        self.agent_card = AGENT_CARD.model_dump(mode="json", exclude_none=True)

    def _validate_request(self, context: RequestContext) -> JSONRPCResponse | None:
        """Validates the incoming request."""
        if not context or not context.message or not context.message.parts:
            logger.error("Invalid request parameters: %s", context)
            return JSONRPCResponse(error=ContentTypeNotSupportedError())
        return None
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """
        Execute the activity search for a given request context.
        """
        logger.debug("Received activity search request: %s", context.message)

        validation_error = self._validate_request(context)
        if validation_error:
            await event_queue.enqueue_event(validation_error)
            return
        
        prompt = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        try:
            # Invoke the activity search agent
            output = await self.agent.ainvoke(prompt)
        
            message = Message(
                message_id=str(uuid4()),
                role=Role.agent,
                metadata={"name": self.agent_card["name"]},
                parts=[Part(TextPart(text=output))],
            )

            logger.info("Activity agent output: %s", output[:100] if output else "empty")

            await event_queue.enqueue_event(message)              
        except Exception as e:
            logger.error(f'Error during activity search: {e}')
            raise ServerError(error=InternalError()) from e
        
    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        """Cancel this agent's execution."""
        raise ServerError(error=UnsupportedOperationError())
