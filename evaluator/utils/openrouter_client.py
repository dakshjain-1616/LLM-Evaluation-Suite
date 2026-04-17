"""OpenRouter API client for LLM evaluation."""

import os
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import logging

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


@dataclass
class OpenRouterResponse:
    """Structured response from OpenRouter API."""
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    model: str
    error: Optional[str] = None
    raw_response: Optional[Any] = None


class OpenRouterClient:
    """Client for OpenRouter API with rate limiting and error handling."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://openrouter.ai/api/v1",
                 timeout: int = 60, max_retries: int = 3, retry_delay: float = 2.0):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger(__name__)
        
        if OpenAI is None:
            raise ImportError("openai package is required. Install with: pip install openai")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout
        )
    
    def chat_completion(self, model: str, messages: List[Dict[str, str]], 
                       temperature: float = 0.7, max_tokens: int = 1024,
                       top_p: float = 0.9, **kwargs) -> OpenRouterResponse:
        """Send chat completion request with retry logic."""
        start_time = time.time()
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    **kwargs
                )
                
                latency_ms = (time.time() - start_time) * 1000
                
                content = response.choices[0].message.content if response.choices else ""
                usage = response.usage
                
                return OpenRouterResponse(
                    content=content,
                    prompt_tokens=usage.prompt_tokens if usage else 0,
                    completion_tokens=usage.completion_tokens if usage else 0,
                    total_tokens=usage.total_tokens if usage else 0,
                    latency_ms=latency_ms,
                    model=model,
                    raw_response=response
                )
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {last_error}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
        
        # All retries failed
        latency_ms = (time.time() - start_time) * 1000
        return OpenRouterResponse(
            content="",
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            latency_ms=latency_ms,
            model=model,
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def is_configured(self) -> bool:
        """Check if API key is configured."""
        return bool(self.api_key and self.api_key != "")
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get model information (placeholder for model metadata)."""
        return {
            "id": model_id,
            "name": model_id.split("/")[-1] if "/" in model_id else model_id,
            "provider": model_id.split("/")[0] if "/" in model_id else "unknown"
        }


# Singleton instance for reuse
_client_instance: Optional[OpenRouterClient] = None


def get_client(config: Optional[Dict[str, Any]] = None) -> OpenRouterClient:
    """Get or create OpenRouter client instance."""
    global _client_instance
    if _client_instance is None or config is not None:
        if config:
            _client_instance = OpenRouterClient(**config)
        else:
            _client_instance = OpenRouterClient()
    return _client_instance
