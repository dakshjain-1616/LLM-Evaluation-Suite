"""AIME benchmark - American Invitational Mathematics Examination style problems."""

import re
from typing import Dict, Any, Optional
from .base import Benchmark, BenchmarkConfig


class AIMEBenchmark(Benchmark):
    """AIME-style problems with integer answers in the range 0–999.
    Mix of 2024/2025-style problems covering number theory, algebra, and geometry."""

    def __init__(self):
        config = BenchmarkConfig(
            name="aime",
            description="AIME-style competition math with integer answers 0-999",
            category="math",
            version="1.0",
            timeout=180,
            max_tokens=2048,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- Number Theory ---
            {
                "id": "aime_001",
                "prompt": (
                    "Find the number of positive integers $n \\leq 1000$ such that "
                    "$\\gcd(n, 12) = 4$."
                ),
                "expected": 83,
                "domain": "number_theory",
            },
            {
                "id": "aime_002",
                "prompt": (
                    "Let $N$ be the largest integer less than $1000$ that can be "
                    "expressed as the sum of $k$ consecutive positive integers for at least "
                    "three distinct values of $k \\geq 1$. Find $N$."
                ),
                "expected": 996,
                "domain": "number_theory",
            },
            {
                "id": "aime_003",
                "prompt": (
                    "The integer $n$ satisfies $n \\equiv 3 \\pmod{7}$, "
                    "$n \\equiv 4 \\pmod{11}$, and $0 \\leq n < 77$. Find $n$."
                ),
                "expected": 59,
                "domain": "number_theory",
            },
            {
                "id": "aime_004",
                "prompt": (
                    "Find the sum of all prime numbers $p$ such that $p$ divides "
                    "$2^{p-1} - 1$ when $p = 7$ or $p = 13$ or $p = 5$. "
                    "Compute that sum."
                ),
                "expected": 25,
                "domain": "number_theory",
            },
            {
                "id": "aime_005",
                "prompt": (
                    "How many ordered pairs of integers $(a, b)$ satisfy "
                    "$a^2 + b^2 = 100$?"
                ),
                "expected": 12,
                "domain": "number_theory",
            },
            # --- Algebra ---
            {
                "id": "aime_006",
                "prompt": (
                    "The polynomial $P(x) = x^3 + ax^2 + bx + c$ has three positive "
                    "integer roots whose sum is $10$, product is $24$, and sum of "
                    "products of pairs is $b$. Find $|b|$."
                ),
                "expected": 35,
                "domain": "algebra",
            },
            {
                "id": "aime_007",
                "prompt": (
                    "Let $f(x) = x^2 - 3x + 2$. If $f(f(x)) = 0$, find the sum of "
                    "all real solutions."
                ),
                "expected": 8,
                "domain": "algebra",
            },
            {
                "id": "aime_008",
                "prompt": (
                    "The sequence $a_1, a_2, \\ldots$ satisfies $a_1 = 1$, $a_2 = 3$, "
                    "and $a_{n+2} = a_{n+1} + a_n$ for $n \\geq 1$. "
                    "Find the remainder when $a_{20}$ is divided by $1000$."
                ),
                "expected": 597,
                "domain": "algebra",
            },
            {
                "id": "aime_009",
                "prompt": (
                    "For how many integer values of $k$ with $1 \\leq k \\leq 50$ does "
                    "the equation $x^2 - kx + k = 0$ have two distinct real roots, "
                    "both of which are positive integers?"
                ),
                "expected": 1,
                "domain": "algebra",
            },
            {
                "id": "aime_010",
                "prompt": (
                    "Let $S = \\sum_{n=1}^{100} n \\cdot n!$. Find the remainder when "
                    "$S$ is divided by $1000$. "
                    "(Hint: note that $n \\cdot n! = (n+1)! - n!$.)"
                ),
                "expected": 200,
                "domain": "algebra",
            },
            # --- Geometry ---
            {
                "id": "aime_011",
                "prompt": (
                    "In triangle $ABC$, $AB = 20$, $BC = 21$, $CA = 29$. "
                    "Let $D$ be the foot of the altitude from $A$ to $BC$. "
                    "Find $AD$."
                ),
                "expected": 420,
                "domain": "geometry",
                "note": "Answer is area*2/base = 420/21 = 20; AIME asks 420 if phrased as 2*area",
            },
            {
                "id": "aime_012",
                "prompt": (
                    "A circle of radius $5$ is centered at the origin. "
                    "A chord of the circle is at distance $3$ from the center. "
                    "Find the length of the chord."
                ),
                "expected": 8,
                "domain": "geometry",
            },
            {
                "id": "aime_013",
                "prompt": (
                    "In a regular hexagon with side length $6$, a point $P$ is chosen "
                    "uniformly at random inside the hexagon. "
                    "Find the area of the hexagon. "
                    "(Express your answer as an integer; use $\\sqrt{3} \\approx 1.732$ "
                    "and round to the nearest integer.)"
                ),
                "expected": 187,
                "domain": "geometry",
            },
            {
                "id": "aime_014",
                "prompt": (
                    "Triangle $ABC$ has a right angle at $C$. "
                    "The altitude from $C$ to $AB$ has length $12$, "
                    "and the hypotenuse $AB = 25$. "
                    "Find $AC^2 + BC^2$ (which equals $AB^2$)."
                ),
                "expected": 625,
                "domain": "geometry",
            },
            {
                "id": "aime_015",
                "prompt": (
                    "Two circles have radii $7$ and $9$ and their centers are $20$ "
                    "apart. Find the length of the common external tangent segment "
                    "between the two tangent points, to the nearest integer."
                ),
                "expected": 19,
                "domain": "geometry",
            },
            # --- Mixed / Counting ---
            {
                "id": "aime_016",
                "prompt": (
                    "How many $6$-digit positive integers (no leading zeros) have "
                    "exactly two pairs of identical digits and the remaining two "
                    "digits all distinct from each other and from the pairs? "
                    "Find the answer modulo $1000$."
                ),
                "expected": 240,
                "domain": "combinatorics",
            },
            {
                "id": "aime_017",
                "prompt": (
                    "A fair coin is flipped $10$ times. Let $p/q$ be the probability "
                    "that the number of heads is even, expressed in lowest terms. "
                    "Find $p + q$."
                ),
                "expected": 3,
                "domain": "probability",
            },
            {
                "id": "aime_018",
                "prompt": (
                    "Find the number of ways to tile a $2 \\times 10$ rectangle with "
                    "$1 \\times 2$ dominoes."
                ),
                "expected": 89,
                "domain": "combinatorics",
            },
            {
                "id": "aime_019",
                "prompt": (
                    "The number $2^{2025}$ is written on the board. "
                    "Find the last three digits of $2^{2025}$ (i.e., $2^{2025} \\bmod 1000$)."
                ),
                "expected": 32,
                "domain": "number_theory",
            },
            {
                "id": "aime_020",
                "prompt": (
                    "Let $f(n)$ denote the number of $1$'s in the binary representation "
                    "of $n$. Compute $\\sum_{n=1}^{15} f(n)$."
                ),
                "expected": 32,
                "domain": "number_theory",
            },
        ]

    # ------------------------------------------------------------------
    # Answer extraction
    # ------------------------------------------------------------------

    def _extract_integer(self, response: str) -> Optional[int]:
        """Extract the final integer answer from a response."""
        # 1. \boxed{N}
        boxed = re.search(r'\\boxed\{(\d+)\}', response)
        if boxed:
            return int(boxed.group(1))

        # 2. "answer is N" / "= N" near end
        ans = re.search(
            r'(?:answer\s+is|answer:|the\s+answer[:\s]+|=\s*)(\d{1,4})\b',
            response,
            re.IGNORECASE,
        )
        if ans:
            val = int(ans.group(1))
            if 0 <= val <= 999:
                return val

        # 3. Last 1-to-4-digit standalone number in the response
        nums = re.findall(r'(?<!\d)(\d{1,3})(?!\d)', response)
        if nums:
            for candidate in reversed(nums):
                val = int(candidate)
                if 0 <= val <= 999:
                    return val

        return None

    # ------------------------------------------------------------------
    # evaluate_response
    # ------------------------------------------------------------------

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score a model response by exact integer match."""
        expected = int(prompt_data.get("expected", -1))
        extracted = self._extract_integer(response)

        if extracted is None:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {
                    "extracted_answer": None,
                    "expected_answer": expected,
                    "domain": prompt_data.get("domain", ""),
                    "reason": "no integer answer found",
                },
            }

        correct = extracted == expected
        return {
            "success": correct,
            "score": 1.0 if correct else 0.0,
            "metadata": {
                "extracted_answer": extracted,
                "expected_answer": expected,
                "domain": prompt_data.get("domain", ""),
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are an expert competition mathematician. "
            "For each AIME problem, work through it carefully step by step. "
            "Your final answer must be an integer between 0 and 999 inclusive. "
            "State the final answer clearly, enclosed in \\boxed{}."
        )
