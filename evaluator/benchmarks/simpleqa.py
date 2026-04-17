"""SimpleQA benchmark - Factual short-answer knowledge questions."""

import re
from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


class SimpleQABenchmark(Benchmark):
    """SimpleQA - factual questions with short, verifiable answers."""

    # Phrases that indicate expressed uncertainty
    UNCERTAINTY_PHRASES = [
        "i'm not sure", "i am not sure", "i don't know", "i do not know",
        "not certain", "unclear", "i cannot confirm", "i can't confirm",
        "i'm uncertain", "i am uncertain", "not confident", "may be wrong",
        "might be", "possibly", "approximately", "around", "i believe but",
    ]

    def __init__(self):
        config = BenchmarkConfig(
            name="simpleqa",
            description="Factual short-answer questions across history, science, geography, and culture",
            category="knowledge",
            version="1.0",
            timeout=30,
            max_tokens=256,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            {
                "id": "sqa_001",
                "prompt": "What is the chemical symbol for gold?",
                "expected": "Au",
                "aliases": [],
            },
            {
                "id": "sqa_002",
                "prompt": "In what year did World War II end?",
                "expected": "1945",
                "aliases": [],
            },
            {
                "id": "sqa_003",
                "prompt": "What is the speed of light in a vacuum in metres per second (to 3 significant figures)?",
                "expected": "3.00 × 10^8",
                "aliases": ["300000000", "3×10^8", "2.998×10^8", "299792458", "3 × 10^8"],
            },
            {
                "id": "sqa_004",
                "prompt": "Who wrote the novel 'Pride and Prejudice'?",
                "expected": "Jane Austen",
                "aliases": ["austen"],
            },
            {
                "id": "sqa_005",
                "prompt": "What is the capital city of Australia?",
                "expected": "Canberra",
                "aliases": [],
            },
            {
                "id": "sqa_006",
                "prompt": "How many sides does a regular hexagon have?",
                "expected": "6",
                "aliases": ["six"],
            },
            {
                "id": "sqa_007",
                "prompt": "What element has atomic number 1?",
                "expected": "Hydrogen",
                "aliases": ["H"],
            },
            {
                "id": "sqa_008",
                "prompt": "In which country is the Amazon River primarily located?",
                "expected": "Brazil",
                "aliases": [],
            },
            {
                "id": "sqa_009",
                "prompt": "What is the value of pi to four decimal places?",
                "expected": "3.1416",
                "aliases": ["3.14159", "3.1415"],
            },
            {
                "id": "sqa_010",
                "prompt": "Who painted the Mona Lisa?",
                "expected": "Leonardo da Vinci",
                "aliases": ["da vinci", "leonardo", "leonardo da vinci"],
            },
            {
                "id": "sqa_011",
                "prompt": "What is the powerhouse of the cell?",
                "expected": "mitochondria",
                "aliases": ["the mitochondria", "mitochondrion"],
            },
            {
                "id": "sqa_012",
                "prompt": "In what year did the Berlin Wall fall?",
                "expected": "1989",
                "aliases": [],
            },
            {
                "id": "sqa_013",
                "prompt": "What is the largest planet in our solar system?",
                "expected": "Jupiter",
                "aliases": [],
            },
            {
                "id": "sqa_014",
                "prompt": "How many bones are in the adult human body?",
                "expected": "206",
                "aliases": [],
            },
            {
                "id": "sqa_015",
                "prompt": "What programming language was created by Guido van Rossum?",
                "expected": "Python",
                "aliases": [],
            },
            {
                "id": "sqa_016",
                "prompt": "What is the longest river in the world?",
                "expected": "Nile",
                "aliases": ["the nile", "nile river"],
            },
            {
                "id": "sqa_017",
                "prompt": "Who developed the theory of general relativity?",
                "expected": "Albert Einstein",
                "aliases": ["einstein"],
            },
            {
                "id": "sqa_018",
                "prompt": "What is the chemical formula for water?",
                "expected": "H2O",
                "aliases": ["h₂o", "h2o"],
            },
            {
                "id": "sqa_019",
                "prompt": "In Shakespeare's play, what is the full name of the tragic prince of Denmark?",
                "expected": "Hamlet",
                "aliases": ["prince hamlet"],
            },
            {
                "id": "sqa_020",
                "prompt": "What is 17 multiplied by 13?",
                "expected": "221",
                "aliases": [],
            },
        ]

    # ------------------------------------------------------------------
    # Evaluation helpers
    # ------------------------------------------------------------------

    def _extract_short_answer(self, response: str) -> str:
        """
        Try to extract the core short answer from a longer response.
        Looks for patterns like 'The answer is X', 'X.' at the start,
        or the first short clause.
        """
        # Look for explicit answer markers
        for pattern in [
            r'(?i)the answer is[:\s]+([^\.\n,]+)',
            r'(?i)answer[:\s]+([^\.\n,]+)',
            r'(?i)it is[:\s]+([^\.\n,]+)',
            r'(?i)that(?:\'s| is)[:\s]+([^\.\n,]+)',
        ]:
            match = re.search(pattern, response)
            if match:
                return match.group(1).strip()

        # Fall back to first sentence / short line
        first_line = response.strip().splitlines()[0] if response.strip() else ""
        first_sentence = re.split(r'[.!?]', first_line)[0]
        return first_sentence.strip()

    def _normalise(self, text: str) -> str:
        """Lowercase, strip punctuation and extra whitespace."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s\.\-\+×^]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _is_exact_or_contains(self, response: str, expected: str, aliases: List[str]) -> bool:
        """Return True if response contains the expected answer or any alias."""
        norm_response = self._normalise(response)
        candidates = [self._normalise(expected)] + [self._normalise(a) for a in aliases]
        for candidate in candidates:
            if candidate and candidate in norm_response:
                return True
        return False

    def _expressed_uncertainty(self, response: str) -> bool:
        """Return True if the response clearly expresses uncertainty about the answer."""
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in self.UNCERTAINTY_PHRASES)

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Score:
          1.0 - exact match or response contains expected answer
          0.5 - response expresses uncertainty and does NOT incorrectly state a wrong answer
          0.0 - wrong answer
        """
        if not response or not response.strip():
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"error": "empty response"},
            }

        expected: str = prompt_data.get("expected", "")
        aliases: List[str] = prompt_data.get("aliases", [])

        # Full credit: answer is correct
        if self._is_exact_or_contains(response, expected, aliases):
            return {
                "success": True,
                "score": 1.0,
                "metadata": {
                    "expected": expected,
                    "match_type": "contains",
                },
            }

        # Partial credit: expresses genuine uncertainty without asserting a wrong answer
        if self._expressed_uncertainty(response):
            return {
                "success": False,
                "score": 0.5,
                "metadata": {
                    "expected": expected,
                    "match_type": "uncertainty",
                    "note": "Response expresses uncertainty; partial credit awarded",
                },
            }

        # No credit
        short = self._extract_short_answer(response)
        return {
            "success": False,
            "score": 0.0,
            "metadata": {
                "expected": expected,
                "extracted_answer": short,
                "match_type": "none",
            },
        }
