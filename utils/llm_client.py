import os
import json
import time
from typing import Any, Dict, List, Optional
from anthropic import Anthropic, APIError
from dataclasses import dataclass


@dataclass
class APIMetrics:
    """Track API usage and performance"""
    requests: int = 0
    tokens_used: int = 0
    total_time: float = 0.0
    errors: int = 0
    retries: int = 0


class LLMClient:
    """Unified client for LLM interactions"""
    
    def __init__(self, model: str, api_key: Optional[str] = None, temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.metrics = APIMetrics()
        
    def call(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: Optional[float] = None,
        retry_count: int = 3,
        json_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Make an LLM call with retry logic
        
        Args:
            system_prompt: System instructions
            user_message: User query
            max_tokens: Maximum response tokens
            temperature: Override default temperature
            retry_count: Number of retries on failure
            json_mode: Expect JSON response
            
        Returns:
            Dictionary with response and metadata
        """
        temp = temperature if temperature is not None else self.temperature
        
        for attempt in range(retry_count):
            try:
                start_time = time.time()
                
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temp,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}]
                )
                
                elapsed = time.time() - start_time
                self.metrics.requests += 1
                self.metrics.tokens_used += response.usage.input_tokens + response.usage.output_tokens
                self.metrics.total_time += elapsed
                
                content = response.content[0].text
                
                # Try to parse JSON if json_mode is enabled
                result = content
                if json_mode:
                    try:
                        result = json.loads(content)
                    except json.JSONDecodeError:
                        # Try to extract JSON from the response
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            result = json.loads(json_match.group())
                
                return {
                    "success": True,
                    "content": result,
                    "model": self.model,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    },
                    "time_seconds": elapsed
                }
                
            except APIError as e:
                self.metrics.errors += 1
                if attempt < retry_count - 1:
                    self.metrics.retries += 1
                    wait_time = 2 ** attempt  # Exponential backoff
                    time.sleep(wait_time)
                else:
                    return {
                        "success": False,
                        "error": str(e),
                        "model": self.model,
                        "attempts": attempt + 1
                    }
        
        return {
            "success": False,
            "error": "Max retries exceeded",
            "model": self.model
        }
    
    def batch_call(
        self,
        system_prompt: str,
        messages: List[str],
        **kwargs
    ) -> List[Dict[str, Any]]:
        """Make multiple calls in sequence"""
        results = []
        for message in messages:
            result = self.call(system_prompt, message, **kwargs)
            results.append(result)
        return results
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        avg_time = self.metrics.total_time / max(self.metrics.requests, 1)
        return {
            "total_requests": self.metrics.requests,
            "total_tokens": self.metrics.tokens_used,
            "total_time": round(self.metrics.total_time, 2),
            "avg_time_per_request": round(avg_time, 2),
            "errors": self.metrics.errors,
            "retries": self.metrics.retries,
            "success_rate": (self.metrics.requests - self.metrics.errors) / max(self.metrics.requests, 1)
        }
    
    def reset_metrics(self):
        """Reset metrics"""
        self.metrics = APIMetrics()
