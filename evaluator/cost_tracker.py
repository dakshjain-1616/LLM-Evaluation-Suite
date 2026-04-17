"""OpenRouter cost tracking — verified pricing Apr 2026."""

from dataclasses import dataclass, field
from typing import Dict, List

# (input_per_1M_usd, output_per_1M_usd)
OPENROUTER_PRICING: Dict[str, tuple] = {
    # Anthropic — verified via OpenRouter /api/v1/models Apr 2026
    "anthropic/claude-opus-4.7":            (5.00,   25.00),   # Claude Opus 4.7 ✓
    "anthropic/claude-opus-4-7":            (5.00,   25.00),   # alias (dash variant)
    "anthropic/claude-opus-4.6":            (5.00,   25.00),   # Claude Opus 4.6
    "anthropic/claude-opus-4.5":            (5.00,   25.00),   # Claude Opus 4.5
    "anthropic/claude-opus-4.1":            (15.00,  75.00),   # Claude Opus 4.1
    "anthropic/claude-opus-4":              (15.00,  75.00),   # Claude Opus 4 (May 2025)
    "anthropic/claude-opus-4.6-fast":       (30.00, 150.00),   # Opus 4.6 fast
    "anthropic/claude-sonnet-4.6":          (3.00,   15.00),   # Claude Sonnet 4.6
    "anthropic/claude-sonnet-4.5":          (3.00,   15.00),
    "anthropic/claude-sonnet-4":            (3.00,   15.00),
    "anthropic/claude-3-haiku":             (0.25,   1.25),
    # OpenAI
    "openai/gpt-5.4":                       (2.50,   15.00),   # GPT-5.4
    "openai/gpt-5.4-mini":                  (0.75,   4.50),
    "openai/gpt-4o":                        (5.00,   15.00),
    "openai/gpt-4o-mini":                   (0.15,   0.60),
    "openai/gpt-3.5-turbo":                 (0.50,   1.50),
    # Google
    "google/gemini-3.1-pro-preview":        (2.00,   12.00),   # Gemini 3.1 Pro
    "google/gemini-3-pro-preview":          (2.00,   12.00),
    "google/gemini-2.5-pro":                (3.50,   10.50),
    "google/gemma-2-9b-it":                 (0.0,    0.0),
    # xAI
    "x-ai/grok-4.20":                       (2.00,   6.00),    # Grok 4.20
    "x-ai/grok-4":                          (3.00,   15.00),
    "x-ai/grok-4-fast":                     (3.00,   15.00),
    # Meta / Mistral / DeepSeek
    "meta-llama/llama-3.1-8b-instruct":     (0.0,    0.0),
    "meta-llama/llama-3.1-70b-instruct":    (0.90,   0.90),
    "deepseek/deepseek-r1":                 (0.80,   2.40),
}

DEFAULT_PRICING = (1.00, 2.00)


def get_pricing(model_id: str) -> tuple:
    return OPENROUTER_PRICING.get(model_id, DEFAULT_PRICING)


@dataclass
class CostEntry:
    model_id: str
    benchmark_name: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float


@dataclass
class CostTracker:
    entries: List[CostEntry] = field(default_factory=list)

    def calculate_cost(self, model_id: str, prompt_tokens: int, completion_tokens: int) -> float:
        input_price, output_price = get_pricing(model_id)
        return (prompt_tokens / 1_000_000) * input_price + (completion_tokens / 1_000_000) * output_price

    def record(self, model_id: str, benchmark_name: str, prompt_tokens: int, completion_tokens: int) -> float:
        cost = self.calculate_cost(model_id, prompt_tokens, completion_tokens)
        self.entries.append(CostEntry(model_id, benchmark_name, prompt_tokens, completion_tokens, cost))
        return cost

    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    def cost_by_model(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for e in self.entries:
            totals[e.model_id] = totals.get(e.model_id, 0.0) + e.cost_usd
        return totals

    def summary(self) -> Dict:
        return {
            "total_cost_usd": self.total_cost(),
            "by_model": self.cost_by_model(),
            "total_entries": len(self.entries),
        }
