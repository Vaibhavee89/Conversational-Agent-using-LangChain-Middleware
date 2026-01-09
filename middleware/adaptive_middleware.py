from typing import Any, Dict
from middleware.base import Middleware
from langchain_core.messages import SystemMessage

class AdaptiveResponseMiddleware(Middleware):
    def __init__(self, user_profiles: Dict[str, Dict[str, Any]] = None):
        self.user_profiles = user_profiles or {}

    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_id = state.get("user_id", "default")
        profile = self.user_profiles.get(user_id, {"tier": "standard", "style": "brief"})
        
        # Inject behavior instructions into the system message or as a new message
        behavior_instr = f"User Preference: {profile['style']}. User Tier: {profile['tier']}."
        
        # Prepend to prompt or system message
        if "messages" in state:
            # Check if system message exists
            if not any(isinstance(m, SystemMessage) for m in state["messages"]):
                state["messages"].insert(0, SystemMessage(content=f"You are a helpful customer support assistant. {behavior_instr}"))
            else:
                for m in state["messages"]:
                    if isinstance(m, SystemMessage):
                        m.content += f"\nNote: {behavior_instr}"
                        
        return state

    def after_model(self, response: Any, state: Dict[str, Any]) -> Any:
        # Adjust behavior based on confidence thresholds if needed
        # (Simplified: if response is too short, warn or tag)
        if hasattr(response, 'content') and len(response.content) < 10:
            print("Warning: Model response is very short, low confidence?")
        return response
