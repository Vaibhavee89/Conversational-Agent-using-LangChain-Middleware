import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from middleware.base import MiddlewarePipeline, Middleware

load_dotenv()

class MiddlewareAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo", middlewares: List[Middleware] = []):
        self.llm = ChatOpenAI(model=model_name)
        self.pipeline = MiddlewarePipeline(middlewares)

    def chat(self, messages: List[BaseMessage], user_id: str = "default") -> str:
        state = {
            "messages": messages,
            "user_id": user_id
        }
        
        # 1. Before Model Hook
        state = self.pipeline.run_before(state)
        
        # 2. Call Model
        try:
            response = self.llm.invoke(state["messages"])
        except Exception as e:
            return f"Error: {str(e)}"
        
        # 3. After Model Hook
        response = self.pipeline.run_after(response, state)
        
        return response.content
