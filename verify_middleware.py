import unittest
from langchain_core.messages import HumanMessage, AIMessage
from middleware.logging_middleware import LoggingMiddleware
from middleware.security_middleware import SecurityMiddleware
from middleware.cost_middleware import CostControlMiddleware
from middleware.adaptive_middleware import AdaptiveResponseMiddleware

class TestMiddleware(unittest.TestCase):
    def test_security_middleware(self):
        middleware = SecurityMiddleware()
        state = {"messages": [HumanMessage(content="My email is test@example.com and phone is 123-456-7890")]}
        processed_state = middleware.before_model(state)
        content = processed_state["messages"][0].content
        self.assertNotIn("test@example.com", content)
        self.assertNotIn("123-456-7890", content)
        print(f"PII Redacted Content: {content}")

    def test_cost_middleware(self):
        middleware = CostControlMiddleware(token_limit=10)
        state = {"messages": [HumanMessage(content="Hello")]}
        # Simulate a response that exceeds the small limit
        response = AIMessage(content="This is a very long response that should definitely exceed the ten token limit we set for this test case.")
        middleware.after_model(response, state)
        
        # Next call should fail
        with self.assertRaises(Exception):
            middleware.before_model(state)

    def test_adaptive_middleware(self):
        user_profiles = {"user_1": {"tier": "premium", "style": "formal"}}
        middleware = AdaptiveResponseMiddleware(user_profiles=user_profiles)
        state = {"messages": [HumanMessage(content="Hi")], "user_id": "user_1"}
        processed_state = middleware.before_model(state)
        system_msg = processed_state["messages"][0].content
        self.assertIn("premium", system_msg)
        self.assertIn("formal", system_msg)

if __name__ == "__main__":
    unittest.main()
