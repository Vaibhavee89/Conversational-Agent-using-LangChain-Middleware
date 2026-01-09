import logging
from typing import Any, Dict
from middleware.base import Middleware

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ChatbotMiddleware")

class LoggingMiddleware(Middleware):
    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state.get("messages", [])[-1].content if state.get("messages") else "No input"
        logger.info(f"User Input: {user_input}")
        return state

    def after_model(self, response: Any, state: Dict[str, Any]) -> Any:
        model_output = response.content if hasattr(response, 'content') else str(response)
        logger.info(f"Model Response: {model_output}")
        return response
