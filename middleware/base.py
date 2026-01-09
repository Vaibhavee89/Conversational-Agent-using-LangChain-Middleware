from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage

class Middleware(ABC):
    @abstractmethod
    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Runs before the LLM is called."""
        return state

    @abstractmethod
    def after_model(self, response: Any, state: Dict[str, Any]) -> Any:
        """Runs after the LLM is called."""
        return response

class MiddlewarePipeline:
    def __init__(self, middlewares: List[Middleware]):
        self.middlewares = middlewares

    def run_before(self, state: Dict[str, Any]) -> Dict[str, Any]:
        for middleware in self.middlewares:
            state = middleware.before_model(state)
        return state

    def run_after(self, response: Any, state: Dict[str, Any]) -> Any:
        # Run in reverse order for 'after' hooks
        for middleware in reversed(self.middlewares):
            response = middleware.after_model(response, state)
        return response
