from typing import Any, Dict
from middleware.base import Middleware
from langchain_community.callbacks import get_openai_callback

class CostControlMiddleware(Middleware):
    def __init__(self, daily_limit: float = 1.0, token_limit: int = 5000):
        self.daily_limit = daily_limit
        self.token_limit = token_limit
        self.total_tokens = 0
        self.total_cost = 0.0

    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if self.total_tokens >= self.token_limit:
            raise Exception(f"Token limit exceeded for this session: {self.total_tokens}/{self.token_limit}")
        return state

    def after_model(self, response: Any, state: Dict[str, Any]) -> Any:
        # Note: In a real app, you'd extract token usage from the LLM response metadata
        # or use a callback. Here we'll simulate or use standard LangChain response metadata.
        if hasattr(response, 'response_metadata') and 'token_usage' in response.response_metadata:
            usage = response.response_metadata.get('token_usage', {})
            self.total_tokens += usage.get('total_tokens', 0)
        
        # Fallback if metadata is missing (e.g. for testing)
        elif hasattr(response, 'content'):
            # Rough estimate: 1 word ~ 1.33 tokens
            self.total_tokens += len(response.content.split()) * 2
            
        print(f"Total Session Tokens: {self.total_tokens}")
        return response
