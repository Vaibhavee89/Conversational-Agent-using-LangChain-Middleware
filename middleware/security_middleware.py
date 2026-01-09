import re
from typing import Any, Dict
from middleware.base import Middleware
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class SecurityMiddleware(Middleware):
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def before_model(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Redact PII from user messages before logging or sending to model
        if "messages" in state:
            for msg in state["messages"]:
                if hasattr(msg, "content"):
                    results = self.analyzer.analyze(text=msg.content, language='en')
                    anonymized_result = self.anonymizer.anonymize(
                        text=msg.content, 
                        analyzer_results=results
                    )
                    msg.content = anonymized_result.text
        return state

    def after_model(self, response: Any, state: Dict[str, Any]) -> Any:
        # Also redact model responses if they leak PII (e.g. if the model repeats it)
        if hasattr(response, "content"):
            results = self.analyzer.analyze(text=response.content, language='en')
            anonymized_result = self.anonymizer.anonymize(
                text=response.content, 
                analyzer_results=results
            )
            response.content = anonymized_result.text
        return response
