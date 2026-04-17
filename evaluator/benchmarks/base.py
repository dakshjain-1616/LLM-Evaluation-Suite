"""Base benchmark class and result dataclass for LLM evaluation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


@dataclass
class BenchmarkConfig:
    """Configuration for a benchmark task."""
    name: str
    description: str
    category: str
    version: str = "1.0"
    timeout: int = 60
    max_tokens: int = 1024
    temperature: float = 0.7


@dataclass
class BenchmarkResult:
    """Result container for a single benchmark evaluation."""
    # Core fields (required - matching runner.py expectations)
    model_id: str
    benchmark: str = ""
    score: float = 0.0
    samples_run: int = 0
    cost_usd: float = 0.0
    latency_avg_s: float = 0.0
    details: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    # Extended fields for detailed tracking
    model_name: str = ""
    benchmark_name: str = ""
    prompt_id: str = ""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    latency_ms: float = 0.0
    prompt: str = ""
    response: str = ""
    expected_answer: Optional[str] = None
    success: bool = False
    token_count_input: int = 0
    token_count_output: int = 0
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure benchmark and benchmark_name are synchronized."""
        if self.benchmark and not self.benchmark_name:
            self.benchmark_name = self.benchmark
        if self.benchmark_name and not self.benchmark:
            self.benchmark = self.benchmark_name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "benchmark": self.benchmark,
            "benchmark_name": self.benchmark_name,
            "model_name": self.model_name,
            "score": self.score,
            "samples_run": self.samples_run,
            "cost_usd": self.cost_usd,
            "latency_avg_s": self.latency_avg_s,
            "details": self.details,
            "errors": self.errors,
            "prompt_id": self.prompt_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "latency_ms": self.latency_ms,
            "prompt": self.prompt,
            "response": self.response,
            "expected_answer": self.expected_answer,
            "success": self.success,
            "token_count_input": self.token_count_input,
            "token_count_output": self.token_count_output,
            "error_message": self.error_message,
            "metadata": self.metadata
        }
    
    @property
    def total_tokens(self) -> int:
        return self.token_count_input + self.token_count_output

    def calculate_cost(self, input_price_per_1k: float, output_price_per_1k: float) -> float:
        input_cost = (self.token_count_input / 1000) * input_price_per_1k
        output_cost = (self.token_count_output / 1000) * output_price_per_1k
        return input_cost + output_cost


class Benchmark(ABC):
    """Abstract base class for all benchmarks."""
    
    def __init__(self, config: Optional[BenchmarkConfig] = None):
        self.config = config or BenchmarkConfig(
            name=self.__class__.__name__,
            description="",
            category="general"
        )
        self.prompts: List[Dict[str, Any]] = []
        self._load_prompts()
    
    @abstractmethod
    def _load_prompts(self) -> None:
        pass
    
    @abstractmethod
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        pass
    
    def get_prompts(self) -> List[Dict[str, Any]]:
        return self.prompts
    
    def get_prompt_count(self) -> int:
        return len(self.prompts)
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def category(self) -> str:
        return self.config.category
    
    def get_system_prompt(self) -> Optional[str]:
        return None
