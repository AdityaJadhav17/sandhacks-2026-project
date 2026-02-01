# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

"""
Shared State Module

Manages shared state and factory instances for the travel supervisor.
This module provides a singleton pattern for the AgntcyFactory to ensure
consistent tracing and client creation across the application.
"""

from typing import Optional
from agntcy_app_sdk.factory import AgntcyFactory

# Global factory instance - initialized once at startup
_factory: Optional[AgntcyFactory] = None


def set_factory(factory: AgntcyFactory) -> None:
    """
    Set the global factory instance.
    
    Called during application startup to initialize the shared factory
    with tracing enabled for observability.
    
    Args:
        factory: Configured AgntcyFactory instance
    """
    global _factory
    _factory = factory


def get_factory() -> Optional[AgntcyFactory]:
    """
    Get the global factory instance.
    
    Returns:
        The shared AgntcyFactory instance, or None if not initialized
    """
    return _factory
