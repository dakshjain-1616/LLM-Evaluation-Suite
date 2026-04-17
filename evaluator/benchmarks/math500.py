"""Math-500 benchmark - Competition-level mathematics problems."""

import re
from typing import Dict, Any, Optional
from .base import Benchmark, BenchmarkConfig


class Math500Benchmark(Benchmark):
    """Math-500: competition-level math covering algebra, number theory,
    geometry, combinatorics, and calculus."""

    def __init__(self):
        config = BenchmarkConfig(
            name="math500",
            description="Competition-level math problems across five domains",
            category="math",
            version="1.0",
            timeout=120,
            max_tokens=2048,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- Algebra (4 problems) ---
            {
                "id": "math500_001",
                "prompt": (
                    "Let $P(x) = x^3 - 6x^2 + 11x - 6$. "
                    "Find all real roots of $P(x)$ and state the sum of the roots."
                ),
                "expected": "6",
                "domain": "algebra",
                "numeric": True,
            },
            {
                "id": "math500_002",
                "prompt": (
                    "The quadratic $x^2 + bx + c = 0$ has roots $r$ and $s$ with "
                    "$r + s = 7$ and $rs = 12$. What is $r^2 + s^2$?"
                ),
                "expected": "25",
                "domain": "algebra",
                "numeric": True,
            },
            {
                "id": "math500_003",
                "prompt": (
                    "Solve the system of equations:\n"
                    "$2x + 3y = 12$\n"
                    "$5x - y = 7$\n"
                    "Find the value of $x + y$."
                ),
                "expected": "4",
                "domain": "algebra",
                "numeric": True,
            },
            {
                "id": "math500_004",
                "prompt": (
                    "If $\\log_2(x) + \\log_2(x-2) = 3$, find the value of $x$."
                ),
                "expected": "4",
                "domain": "algebra",
                "numeric": True,
            },
            # --- Number Theory (4 problems) ---
            {
                "id": "math500_005",
                "prompt": (
                    "Find the number of positive divisors of $2^4 \\cdot 3^2 \\cdot 5^1$."
                ),
                "expected": "30",
                "domain": "number_theory",
                "numeric": True,
            },
            {
                "id": "math500_006",
                "prompt": (
                    "What is the remainder when $7^{100}$ is divided by $10$?"
                ),
                "expected": "1",
                "domain": "number_theory",
                "numeric": True,
            },
            {
                "id": "math500_007",
                "prompt": (
                    "Find the greatest common divisor of $1848$ and $3003$."
                ),
                "expected": "231",
                "domain": "number_theory",
                "numeric": True,
            },
            {
                "id": "math500_008",
                "prompt": (
                    "How many integers between $1$ and $300$ inclusive are divisible "
                    "by neither $3$ nor $5$?"
                ),
                "expected": "160",
                "domain": "number_theory",
                "numeric": True,
            },
            # --- Geometry (4 problems) ---
            {
                "id": "math500_009",
                "prompt": (
                    "A right triangle has legs of length $7$ and $24$. "
                    "What is the length of the hypotenuse?"
                ),
                "expected": "25",
                "domain": "geometry",
                "numeric": True,
            },
            {
                "id": "math500_010",
                "prompt": (
                    "In triangle $ABC$, $AB = 13$, $BC = 14$, $CA = 15$. "
                    "Find the area of the triangle."
                ),
                "expected": "84",
                "domain": "geometry",
                "numeric": True,
            },
            {
                "id": "math500_011",
                "prompt": (
                    "A circle is inscribed in a square with side length $10$. "
                    "What is the area of the region inside the square but outside the circle? "
                    "Express your answer in terms of $\\pi$."
                ),
                "expected": "100 - 25\\pi",
                "domain": "geometry",
                "numeric": False,
            },
            {
                "id": "math500_012",
                "prompt": (
                    "Two parallel lines are cut by a transversal. "
                    "One of the co-interior (same-side interior) angles measures $68^\\circ$. "
                    "What is the measure, in degrees, of the other co-interior angle?"
                ),
                "expected": "112",
                "domain": "geometry",
                "numeric": True,
            },
            # --- Combinatorics (4 problems) ---
            {
                "id": "math500_013",
                "prompt": (
                    "In how many ways can $8$ distinct books be arranged on a shelf?"
                ),
                "expected": "40320",
                "domain": "combinatorics",
                "numeric": True,
            },
            {
                "id": "math500_014",
                "prompt": (
                    "A committee of $3$ people is chosen from a group of $10$. "
                    "How many distinct committees are possible?"
                ),
                "expected": "120",
                "domain": "combinatorics",
                "numeric": True,
            },
            {
                "id": "math500_015",
                "prompt": (
                    "How many $4$-digit numbers (leading zeros not allowed) have "
                    "all four digits distinct?"
                ),
                "expected": "4536",
                "domain": "combinatorics",
                "numeric": True,
            },
            {
                "id": "math500_016",
                "prompt": (
                    "What is the coefficient of $x^3 y^2$ in the expansion of $(x + y)^5$?"
                ),
                "expected": "10",
                "domain": "combinatorics",
                "numeric": True,
            },
            # --- Calculus (4 problems) ---
            {
                "id": "math500_017",
                "prompt": (
                    "Find the derivative of $f(x) = x^4 - 3x^3 + 2x - 7$ and evaluate "
                    "it at $x = 2$."
                ),
                "expected": "14",
                "domain": "calculus",
                "numeric": True,
            },
            {
                "id": "math500_018",
                "prompt": (
                    "Evaluate the definite integral $\\int_0^2 (3x^2 + 2x)\\, dx$."
                ),
                "expected": "12",
                "domain": "calculus",
                "numeric": True,
            },
            {
                "id": "math500_019",
                "prompt": (
                    "Find all critical points of $f(x) = x^3 - 3x$ and classify each "
                    "as a local maximum, local minimum, or saddle point. "
                    "State the $x$-coordinates of the critical points as a set."
                ),
                "expected": "{-1, 1}",
                "domain": "calculus",
                "numeric": False,
            },
            {
                "id": "math500_020",
                "prompt": (
                    "Compute $\\lim_{x \\to 0} \\dfrac{\\sin(3x)}{x}$."
                ),
                "expected": "3",
                "domain": "calculus",
                "numeric": True,
            },
        ]

    # ------------------------------------------------------------------
    # Answer extraction helpers
    # ------------------------------------------------------------------

    def _extract_answer(self, response: str) -> Optional[str]:
        """Return the final answer from a response string, or None."""
        # 1. LaTeX boxed answer: \boxed{...}
        boxed = re.search(r'\\boxed\{([^}]+)\}', response)
        if boxed:
            return boxed.group(1).strip()

        # 2. "= X" near end of response
        eq_match = re.findall(r'=\s*([-+]?\d*\.?\d+(?:\s*/\s*\d+)?)', response)
        if eq_match:
            return eq_match[-1].strip()

        # 3. "answer is X" / "the answer: X"
        ans_match = re.search(
            r'(?:answer\s+is|answer:|final answer[:\s]+)\s*([-+]?\d*\.?\d+)',
            response,
            re.IGNORECASE,
        )
        if ans_match:
            return ans_match.group(1).strip()

        # 4. Last standalone number in text
        nums = re.findall(r'(?<!\w)([-+]?\d+(?:\.\d+)?)(?!\w)', response)
        if nums:
            return nums[-1].strip()

        return None

    def _to_float(self, value: str) -> Optional[float]:
        """Convert a string to float, handling simple fractions."""
        try:
            if '/' in value:
                num, den = value.split('/', 1)
                return float(num.strip()) / float(den.strip())
            return float(value.strip())
        except (ValueError, ZeroDivisionError):
            return None

    def _numeric_equal(self, extracted: str, expected: str, tol: float = 1e-6) -> bool:
        """Return True if both strings represent the same number within tolerance."""
        a = self._to_float(extracted)
        b = self._to_float(expected)
        if a is None or b is None:
            return False
        if b == 0:
            return abs(a) < tol
        return abs(a - b) / (abs(b) + 1e-12) < tol

    # ------------------------------------------------------------------
    # evaluate_response
    # ------------------------------------------------------------------

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score a model response against the expected answer."""
        expected = prompt_data.get("expected", "")
        is_numeric = prompt_data.get("numeric", True)

        extracted = self._extract_answer(response)

        if extracted is None:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {
                    "extracted_answer": None,
                    "expected_answer": expected,
                    "domain": prompt_data.get("domain", ""),
                    "reason": "no answer found in response",
                },
            }

        if is_numeric:
            correct = self._numeric_equal(extracted, expected)
        else:
            # Expression / set comparison: normalise whitespace
            correct = re.sub(r'\s+', '', extracted) == re.sub(r'\s+', '', expected)

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
            "You are an expert mathematician. Solve the problem step by step and "
            "state your final answer clearly. When possible, enclose the final "
            "answer in \\boxed{}."
        )
