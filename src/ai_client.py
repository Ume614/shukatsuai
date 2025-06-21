import os
from typing import Dict, Any, Optional
import anthropic
import openai
from abc import ABC, abstractmethod

class AIClient(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass

class ClaudeClient(AIClient):
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                system=system_prompt or "You are a helpful assistant for job hunting support.",
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"

class OpenAIClient(AIClient):
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt or "You are a helpful assistant for job hunting support."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

def get_ai_client(model: str = "claude") -> AIClient:
    if model == "claude":
        return ClaudeClient()
    elif model == "openai":
        return OpenAIClient()
    else:
        raise ValueError(f"Unsupported model: {model}")