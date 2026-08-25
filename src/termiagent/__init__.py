"""
TermiAgent — Universal Terminal AI Coding Agent CLI.
"""

from .agent import TermiAgent
from .providers.universal import UniversalLLMProvider

__version__ = "0.1.0"

__all__ = ["TermiAgent", "UniversalLLMProvider"]
