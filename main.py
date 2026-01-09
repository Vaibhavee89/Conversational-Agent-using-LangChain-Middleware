import os
from langchain_core.messages import HumanMessage
from agent import MiddlewareAgent
from middleware.logging_middleware import LoggingMiddleware
from middleware.security_middleware import SecurityMiddleware
from middleware.cost_middleware import CostControlMiddleware
from middleware.adaptive_middleware import AdaptiveResponseMiddleware

def main():
    # Setup middleware
    user_profiles = {
        "user_1": {"tier": "premium", "style": "helpful and detailed"},
        "user_2": {"tier": "free", "style": "short and concise"}
    }
    
    middlewares = [
        LoggingMiddleware(),
        SecurityMiddleware(),
        CostControlMiddleware(token_limit=1000),
        AdaptiveResponseMiddleware(user_profiles=user_profiles)
    ]
    
    agent = MiddlewareAgent(middlewares=middlewares)
    
    print("Welcome to Middleware-Enhanced Customer Support Chatbot!")
    print("Type 'exit' to quit.")
    
    user_id = input("Enter your User ID (e.g., user_1, user_2): ") or "default"
    
    history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        history.append(HumanMessage(content=user_input))
        
        try:
            # We pass a copy of history to avoid state issues in simple loops
            # although middleware modifies it in-place in this implementation
            response = agent.chat(messages=history, user_id=user_id)
            print(f"\nAI: {response}")
        except Exception as e:
            print(f"\nError occurred: {e}")

if __name__ == "__main__":
    main()
