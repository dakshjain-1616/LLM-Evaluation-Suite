"""IFEval benchmark - Instruction Following Evaluation with verifiable constraints."""

import re
from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


class IFEvalBenchmark(Benchmark):
    """IFEval - evaluates instruction following via programmatically verifiable constraints."""

    def __init__(self):
        config = BenchmarkConfig(
            name="ifeval",
            description="Instruction following evaluation with verifiable constraints",
            category="instruction_following",
            version="1.0",
            timeout=60,
            max_tokens=1024,
            temperature=0.7,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            {
                "id": "ifeval_001",
                "prompt": (
                    "Write a haiku about autumn. "
                    "It must have exactly 3 lines with 5, 7, and 5 syllables respectively."
                ),
                "expected": "3-line haiku with 5/7/5 syllable structure",
                "constraints": [
                    {"type": "line_count", "value": 3},
                    {"type": "syllable_pattern", "pattern": [5, 7, 5]},
                ],
            },
            {
                "id": "ifeval_002",
                "prompt": (
                    "List 5 programming languages. "
                    "Your response must be a numbered list and each item must be under 10 words."
                ),
                "expected": "Numbered list of exactly 5 items, each under 10 words",
                "constraints": [
                    {"type": "numbered_list_count", "value": 5},
                    {"type": "each_item_max_words", "value": 10},
                ],
            },
            {
                "id": "ifeval_003",
                "prompt": (
                    "Explain gravity in exactly 3 sentences. "
                    "Do not use the word 'force'."
                ),
                "expected": "3-sentence explanation with no mention of 'force'",
                "constraints": [
                    {"type": "sentence_count", "value": 3},
                    {"type": "forbidden_word", "value": "force"},
                ],
            },
            {
                "id": "ifeval_004",
                "prompt": (
                    "Write a Python function that adds two numbers. "
                    "Include a docstring. Use snake_case for the function name. "
                    "Do not use global variables."
                ),
                "expected": "Python function with docstring, snake_case name, no globals",
                "constraints": [
                    {"type": "contains_pattern", "pattern": r'def [a-z][a-z0-9_]*\('},
                    {"type": "contains_pattern", "pattern": r'"""'},
                    {"type": "forbidden_word", "value": "global"},
                ],
            },
            {
                "id": "ifeval_005",
                "prompt": (
                    "Describe the water cycle in bullet points. "
                    "Use exactly 4 bullet points. "
                    "Each bullet must start with a capital letter."
                ),
                "expected": "4 bullet points, each starting with a capital letter",
                "constraints": [
                    {"type": "bullet_count", "value": 4},
                    {"type": "bullets_start_capital", "value": True},
                ],
            },
            {
                "id": "ifeval_006",
                "prompt": (
                    "Write a short story opening in exactly 2 sentences. "
                    "The first sentence must end with a question mark. "
                    "Do not use the word 'suddenly'."
                ),
                "expected": "2 sentences, first ends with '?', no 'suddenly'",
                "constraints": [
                    {"type": "sentence_count", "value": 2},
                    {"type": "first_sentence_ends_with", "value": "?"},
                    {"type": "forbidden_word", "value": "suddenly"},
                ],
            },
            {
                "id": "ifeval_007",
                "prompt": (
                    "Give me a recipe for pancakes. "
                    "Your response must contain the word 'batter' at least twice. "
                    "List ingredients as a bulleted list before the instructions."
                ),
                "expected": "Recipe with 'batter' >=2 times and bulleted ingredients section",
                "constraints": [
                    {"type": "word_min_count", "word": "batter", "count": 2},
                    {"type": "contains_pattern", "pattern": r'(?i)ingredient'},
                    {"type": "contains_bullet", "value": True},
                ],
            },
            {
                "id": "ifeval_008",
                "prompt": (
                    "Translate the following to French and provide the English original beside it: "
                    "'The cat sat on the mat.' "
                    "Format each as: English: ... / French: ..."
                ),
                "expected": "English and French versions with specified format labels",
                "constraints": [
                    {"type": "contains_pattern", "pattern": r'(?i)english\s*:'},
                    {"type": "contains_pattern", "pattern": r'(?i)french\s*:'},
                ],
            },
            {
                "id": "ifeval_009",
                "prompt": (
                    "Write a limerick about a programmer. "
                    "It must have exactly 5 lines. "
                    "Lines 1, 2, and 5 must rhyme with each other."
                ),
                "expected": "5-line limerick with AABBA rhyme structure",
                "constraints": [
                    {"type": "line_count", "value": 5},
                ],
            },
            {
                "id": "ifeval_010",
                "prompt": (
                    "Summarize the concept of machine learning in exactly 50 words. "
                    "Do not use the words 'artificial' or 'intelligence'."
                ),
                "expected": "50-word summary without 'artificial' or 'intelligence'",
                "constraints": [
                    {"type": "word_count_exact", "value": 50, "tolerance": 3},
                    {"type": "forbidden_word", "value": "artificial"},
                    {"type": "forbidden_word", "value": "intelligence"},
                ],
            },
            {
                "id": "ifeval_011",
                "prompt": (
                    "List the planets in our solar system. "
                    "Use an alphabetical ordering. "
                    "Each planet name must be on its own line."
                ),
                "expected": "Planets listed alphabetically, one per line",
                "constraints": [
                    {"type": "contains_pattern", "pattern": r'(?i)earth'},
                    {"type": "contains_pattern", "pattern": r'(?i)jupiter'},
                    {"type": "alphabetical_lines", "value": True},
                ],
            },
            {
                "id": "ifeval_012",
                "prompt": (
                    "Write a motivational quote. "
                    "It must be a single sentence. "
                    "It must contain the word 'journey'. "
                    "It must be fewer than 20 words."
                ),
                "expected": "Single sentence under 20 words containing 'journey'",
                "constraints": [
                    {"type": "sentence_count", "value": 1},
                    {"type": "required_word", "value": "journey"},
                    {"type": "max_word_count", "value": 20},
                ],
            },
            {
                "id": "ifeval_013",
                "prompt": (
                    "Explain the difference between a stack and a queue. "
                    "Use exactly two paragraphs, one for each data structure. "
                    "Do not use the word 'element'."
                ),
                "expected": "Two paragraphs, no use of 'element'",
                "constraints": [
                    {"type": "paragraph_count", "value": 2},
                    {"type": "forbidden_word", "value": "element"},
                ],
            },
            {
                "id": "ifeval_014",
                "prompt": (
                    "Write a tweet (max 280 characters) about climate change. "
                    "Include at least one hashtag. "
                    "Do not use the word 'global'."
                ),
                "expected": "<=280 chars, at least one hashtag, no 'global'",
                "constraints": [
                    {"type": "max_char_count", "value": 280},
                    {"type": "contains_pattern", "pattern": r'#\w+'},
                    {"type": "forbidden_word", "value": "global"},
                ],
            },
            {
                "id": "ifeval_015",
                "prompt": (
                    "Describe three benefits of exercise. "
                    "Use exactly 3 numbered items. "
                    "Each item must be a complete sentence ending with a period."
                ),
                "expected": "3 numbered items, each a complete sentence ending with '.'",
                "constraints": [
                    {"type": "numbered_list_count", "value": 3},
                    {"type": "each_item_ends_with_period", "value": True},
                ],
            },
            {
                "id": "ifeval_016",
                "prompt": (
                    "Write an email subject line for a job application. "
                    "It must be a single line. "
                    "It must be under 60 characters. "
                    "It must include the word 'Application'."
                ),
                "expected": "Single line, <60 chars, contains 'Application'",
                "constraints": [
                    {"type": "line_count", "value": 1},
                    {"type": "max_char_count", "value": 60},
                    {"type": "required_word", "value": "Application"},
                ],
            },
            {
                "id": "ifeval_017",
                "prompt": (
                    "Give five synonyms for the word 'happy'. "
                    "Format them as a comma-separated list on a single line. "
                    "All words must be lowercase."
                ),
                "expected": "5 lowercase synonyms as a comma-separated single line",
                "constraints": [
                    {"type": "comma_separated_count", "value": 5},
                    {"type": "all_lowercase_response", "value": True},
                    {"type": "line_count", "value": 1},
                ],
            },
            {
                "id": "ifeval_018",
                "prompt": (
                    "Explain what a REST API is. "
                    "Your response must have a title in ALL CAPS on the first line. "
                    "Then provide the explanation in no more than 4 sentences."
                ),
                "expected": "First line in ALL CAPS title, then <=4 sentence explanation",
                "constraints": [
                    {"type": "first_line_all_caps", "value": True},
                    {"type": "max_sentence_count", "value": 4, "skip_lines": 1},
                ],
            },
            {
                "id": "ifeval_019",
                "prompt": (
                    "Write a comparison of cats and dogs as pets. "
                    "Structure it with two sections labeled 'Cats:' and 'Dogs:'. "
                    "Each section must contain at least 2 sentences."
                ),
                "expected": "Two labeled sections 'Cats:' and 'Dogs:', each with >=2 sentences",
                "constraints": [
                    {"type": "contains_pattern", "pattern": r'(?m)^Cats:'},
                    {"type": "contains_pattern", "pattern": r'(?m)^Dogs:'},
                ],
            },
            {
                "id": "ifeval_020",
                "prompt": (
                    "Write a step-by-step guide to making tea. "
                    "Number each step starting from 1. "
                    "Include at least 5 steps. "
                    "Do not use the word 'simply'."
                ),
                "expected": "Numbered steps starting at 1, at least 5, no 'simply'",
                "constraints": [
                    {"type": "numbered_list_min", "value": 5},
                    {"type": "starts_with_step_1", "value": True},
                    {"type": "forbidden_word", "value": "simply"},
                ],
            },
        ]

    # ------------------------------------------------------------------
    # Constraint checkers (named functions, never bare lambdas)
    # ------------------------------------------------------------------

    def _check_line_count(self, response: str, value: int) -> bool:
        lines = [ln for ln in response.strip().splitlines() if ln.strip()]
        return len(lines) == value

    def _check_numbered_list_count(self, response: str, value: int) -> bool:
        items = re.findall(r'^\s*\d+[\.\)]\s+\S', response, re.MULTILINE)
        return len(items) == value

    def _check_numbered_list_min(self, response: str, value: int) -> bool:
        items = re.findall(r'^\s*\d+[\.\)]\s+\S', response, re.MULTILINE)
        return len(items) >= value

    def _check_each_item_max_words(self, response: str, value: int) -> bool:
        items = re.findall(r'^\s*\d+[\.\)]\s+(.+)', response, re.MULTILINE)
        if not items:
            return False
        return all(len(item.split()) <= value for item in items)

    def _check_sentence_count(self, response: str, value: int) -> bool:
        sentences = re.split(r'[.!?]+', response.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences) == value

    def _check_forbidden_word(self, response: str, value: str) -> bool:
        pattern = r'\b' + re.escape(value) + r'\b'
        return not bool(re.search(pattern, response, re.IGNORECASE))

    def _check_required_word(self, response: str, value: str) -> bool:
        pattern = r'\b' + re.escape(value) + r'\b'
        return bool(re.search(pattern, response, re.IGNORECASE))

    def _check_contains_pattern(self, response: str, pattern: str) -> bool:
        return bool(re.search(pattern, response))

    def _check_bullet_count(self, response: str, value: int) -> bool:
        bullets = re.findall(r'^\s*[-*•]\s+\S', response, re.MULTILINE)
        return len(bullets) == value

    def _check_contains_bullet(self, response: str, **_) -> bool:
        return bool(re.search(r'^\s*[-*•]\s+\S', response, re.MULTILINE))

    def _check_bullets_start_capital(self, response: str, **_) -> bool:
        bullets = re.findall(r'^\s*[-*•]\s+(.+)', response, re.MULTILINE)
        if not bullets:
            return False
        return all(item[0].isupper() for item in bullets)

    def _check_first_sentence_ends_with(self, response: str, value: str) -> bool:
        sentences = re.split(r'(?<=[.!?])\s+', response.strip())
        if not sentences:
            return False
        return sentences[0].rstrip().endswith(value)

    def _check_word_min_count(self, response: str, word: str, count: int) -> bool:
        found = re.findall(r'\b' + re.escape(word) + r'\b', response, re.IGNORECASE)
        return len(found) >= count

    def _check_word_count_exact(self, response: str, value: int, tolerance: int = 0) -> bool:
        words = response.split()
        return abs(len(words) - value) <= tolerance

    def _check_max_word_count(self, response: str, value: int) -> bool:
        return len(response.split()) <= value

    def _check_max_char_count(self, response: str, value: int) -> bool:
        return len(response.strip()) <= value

    def _check_alphabetical_lines(self, response: str, **_) -> bool:
        lines = [ln.strip().lower() for ln in response.strip().splitlines() if ln.strip()]
        return lines == sorted(lines)

    def _check_paragraph_count(self, response: str, value: int) -> bool:
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', response.strip()) if p.strip()]
        return len(paragraphs) == value

    def _check_comma_separated_count(self, response: str, value: int) -> bool:
        line = response.strip().splitlines()[0] if response.strip() else ""
        items = [i.strip() for i in line.split(',') if i.strip()]
        return len(items) == value

    def _check_all_lowercase_response(self, response: str, **_) -> bool:
        alpha_chars = [c for c in response if c.isalpha()]
        return all(c.islower() for c in alpha_chars) if alpha_chars else False

    def _check_first_line_all_caps(self, response: str, **_) -> bool:
        lines = [ln for ln in response.strip().splitlines() if ln.strip()]
        if not lines:
            return False
        first = lines[0].strip()
        alpha = [c for c in first if c.isalpha()]
        return bool(alpha) and all(c.isupper() for c in alpha)

    def _check_max_sentence_count(self, response: str, value: int, skip_lines: int = 0) -> bool:
        lines = response.strip().splitlines()
        body = '\n'.join(lines[skip_lines:])
        sentences = re.split(r'[.!?]+', body)
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences) <= value

    def _check_each_item_ends_with_period(self, response: str, **_) -> bool:
        items = re.findall(r'^\s*\d+[\.\)]\s+(.+)', response, re.MULTILINE)
        if not items:
            return False
        return all(item.rstrip().endswith('.') for item in items)

    def _check_starts_with_step_1(self, response: str, **_) -> bool:
        return bool(re.search(r'^\s*1[\.\)]\s+\S', response, re.MULTILINE))

    def _check_syllable_pattern(self, response: str, pattern: List[int]) -> bool:
        """Approximate syllable check using vowel-group counting."""
        lines = [ln for ln in response.strip().splitlines() if ln.strip()]
        if len(lines) != len(pattern):
            return False
        for line, expected_syllables in zip(lines, pattern):
            syllables = len(re.findall(r'[aeiouAEIOU]+', line))
            if abs(syllables - expected_syllables) > 1:
                return False
        return True

    # ------------------------------------------------------------------
    # Constraint evaluation dispatcher (named method, no bare lambdas)
    # ------------------------------------------------------------------

    def _evaluate_constraint(self, response: str, constraint: Dict[str, Any]) -> bool:
        ctype = constraint["type"]
        try:
            if ctype == "line_count":
                return self._check_line_count(response, constraint["value"])
            if ctype == "numbered_list_count":
                return self._check_numbered_list_count(response, constraint["value"])
            if ctype == "numbered_list_min":
                return self._check_numbered_list_min(response, constraint["value"])
            if ctype == "each_item_max_words":
                return self._check_each_item_max_words(response, constraint["value"])
            if ctype == "sentence_count":
                return self._check_sentence_count(response, constraint["value"])
            if ctype == "forbidden_word":
                return self._check_forbidden_word(response, constraint["value"])
            if ctype == "required_word":
                return self._check_required_word(response, constraint["value"])
            if ctype == "contains_pattern":
                return self._check_contains_pattern(response, constraint["pattern"])
            if ctype == "bullet_count":
                return self._check_bullet_count(response, constraint["value"])
            if ctype == "contains_bullet":
                return self._check_contains_bullet(response)
            if ctype == "bullets_start_capital":
                return self._check_bullets_start_capital(response)
            if ctype == "first_sentence_ends_with":
                return self._check_first_sentence_ends_with(response, constraint["value"])
            if ctype == "word_min_count":
                return self._check_word_min_count(response, constraint["word"], constraint["count"])
            if ctype == "word_count_exact":
                return self._check_word_count_exact(response, constraint["value"], constraint.get("tolerance", 0))
            if ctype == "max_word_count":
                return self._check_max_word_count(response, constraint["value"])
            if ctype == "max_char_count":
                return self._check_max_char_count(response, constraint["value"])
            if ctype == "alphabetical_lines":
                return self._check_alphabetical_lines(response)
            if ctype == "paragraph_count":
                return self._check_paragraph_count(response, constraint["value"])
            if ctype == "comma_separated_count":
                return self._check_comma_separated_count(response, constraint["value"])
            if ctype == "all_lowercase_response":
                return self._check_all_lowercase_response(response)
            if ctype == "first_line_all_caps":
                return self._check_first_line_all_caps(response)
            if ctype == "max_sentence_count":
                return self._check_max_sentence_count(response, constraint["value"], constraint.get("skip_lines", 0))
            if ctype == "each_item_ends_with_period":
                return self._check_each_item_ends_with_period(response)
            if ctype == "starts_with_step_1":
                return self._check_starts_with_step_1(response)
            if ctype == "syllable_pattern":
                return self._check_syllable_pattern(response, constraint["pattern"])
        except Exception:
            return False
        return False

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate response by checking each constraint programmatically."""
        constraints = prompt_data.get("constraints", [])
        if not constraints:
            return {"success": False, "score": 0.0, "metadata": {"error": "no constraints defined"}}

        results = []
        for constraint in constraints:
            passed = self._evaluate_constraint(response, constraint)
            results.append({"constraint": constraint, "passed": passed})

        passed_count = sum(1 for r in results if r["passed"])
        score = passed_count / len(results)
        success = score == 1.0

        return {
            "success": success,
            "score": round(score, 4),
            "metadata": {
                "constraints_total": len(results),
                "constraints_passed": passed_count,
                "constraint_results": results,
            },
        }
