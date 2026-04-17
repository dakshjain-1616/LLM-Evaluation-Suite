"""BigCodeBench benchmark - real-library Python function writing tasks."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class BigCodeBenchBenchmark(Benchmark):
    """BigCodeBench - Python coding tasks requiring real library usage."""

    def __init__(self):
        config = BenchmarkConfig(
            name="bigcodebench",
            description="Python function writing using real standard and third-party libraries",
            category="code",
            version="1.0",
            timeout=90,
            max_tokens=1024,
            temperature=0.2,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            {
                "id": "bcb_001",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def fetch_json(url: str, timeout: int = 10) -> dict:\n"
                    "    ...\n\n"
                    "The function must use the `requests` library to perform a GET request to `url`, "
                    "raise an exception if the HTTP status is not 2xx, and return the parsed JSON response as a dict. "
                    "Include a docstring and a usage example in a `if __name__ == '__main__':` block."
                ),
                "expected": "def fetch_json",
                "expected_keywords": ["requests", "requests.get", "raise_for_status", "json", "def fetch_json"],
            },
            {
                "id": "bcb_002",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def csv_summary(filepath: str) -> dict:\n"
                    "    ...\n\n"
                    "Use `pandas` to read the CSV file at `filepath` and return a dict containing: "
                    "'shape' (tuple of rows and columns), 'columns' (list of column names), "
                    "'nulls' (dict mapping column name to null count), and 'dtypes' (dict mapping column name to dtype string). "
                    "Include a docstring."
                ),
                "expected": "def csv_summary",
                "expected_keywords": ["pandas", "pd.read_csv", "isnull", "shape", "def csv_summary"],
            },
            {
                "id": "bcb_003",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def normalize_matrix(matrix: list) -> list:\n"
                    "    ...\n\n"
                    "Use `numpy` to accept a 2-D list (or numpy array), apply min-max normalization "
                    "so all values fall in [0, 1], and return the result as a Python list of lists. "
                    "Handle the edge case where min == max by returning a zero matrix of the same shape. "
                    "Include a docstring."
                ),
                "expected": "def normalize_matrix",
                "expected_keywords": ["numpy", "np.array", "np.zeros", "def normalize_matrix"],
            },
            {
                "id": "bcb_004",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def days_between(date_str1: str, date_str2: str, fmt: str = '%Y-%m-%d') -> int:\n"
                    "    ...\n\n"
                    "Use the `datetime` module to parse both date strings with `fmt` and return the absolute "
                    "number of days between them as an integer. Include a docstring and at least one inline comment."
                ),
                "expected": "def days_between",
                "expected_keywords": ["datetime", "strptime", "timedelta", "abs", "def days_between"],
            },
            {
                "id": "bcb_005",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def list_python_files(directory: str) -> list:\n"
                    "    ...\n\n"
                    "Use `pathlib.Path` to recursively find all `.py` files under `directory` and return "
                    "a sorted list of their absolute path strings. Include a docstring."
                ),
                "expected": "def list_python_files",
                "expected_keywords": ["pathlib", "Path", "rglob", "*.py", "def list_python_files"],
            },
            {
                "id": "bcb_006",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def merge_json_files(paths: list) -> dict:\n"
                    "    ...\n\n"
                    "Use the `json` module to read each file path in `paths`, parse the JSON content "
                    "(assuming each file contains a JSON object/dict), and merge all dicts into a single dict "
                    "(later keys override earlier ones). Return the merged dict. Include a docstring."
                ),
                "expected": "def merge_json_files",
                "expected_keywords": ["json", "json.load", "open", "update", "def merge_json_files"],
            },
            {
                "id": "bcb_007",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def extract_emails(text: str) -> list:\n"
                    "    ...\n\n"
                    "Use the `re` module to find and return a deduplicated, sorted list of all email addresses "
                    "in `text`. A valid email for this task matches the pattern: word chars/dots/hyphens, "
                    "followed by @, followed by domain with at least one dot. Include a docstring."
                ),
                "expected": "def extract_emails",
                "expected_keywords": ["re", "re.findall", "sorted", "set", "def extract_emails"],
            },
            {
                "id": "bcb_008",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def word_frequency(text: str, top_n: int = 10) -> list:\n"
                    "    ...\n\n"
                    "Use `collections.Counter` to tokenize `text` into lowercase words (strip punctuation), "
                    "count word frequencies, and return the `top_n` most common as a list of (word, count) tuples. "
                    "Include a docstring."
                ),
                "expected": "def word_frequency",
                "expected_keywords": ["collections", "Counter", "most_common", "def word_frequency"],
            },
            {
                "id": "bcb_009",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def sliding_window_pairs(iterable, window_size: int = 2) -> list:\n"
                    "    ...\n\n"
                    "Use `itertools` to generate all consecutive sub-sequences of length `window_size` "
                    "from `iterable` and return them as a list of tuples. "
                    "Use `itertools.islice` in your implementation. Include a docstring."
                ),
                "expected": "def sliding_window_pairs",
                "expected_keywords": ["itertools", "islice", "zip", "def sliding_window_pairs"],
            },
            {
                "id": "bcb_010",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def memoized_fibonacci(n: int) -> int:\n"
                    "    ...\n\n"
                    "Use `functools.lru_cache` (or `functools.cache`) to compute the n-th Fibonacci number "
                    "recursively with memoization. Raise a `ValueError` for negative inputs. "
                    "Include a docstring."
                ),
                "expected": "def memoized_fibonacci",
                "expected_keywords": ["functools", "lru_cache", "def memoized_fibonacci", "ValueError"],
            },
            {
                "id": "bcb_011",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def post_json(url: str, payload: dict, headers: dict = None) -> dict:\n"
                    "    ...\n\n"
                    "Use `requests` to POST `payload` as JSON to `url` with optional `headers`, "
                    "call `raise_for_status()`, and return the response JSON as a dict. Include a docstring."
                ),
                "expected": "def post_json",
                "expected_keywords": ["requests", "requests.post", "raise_for_status", "json", "def post_json"],
            },
            {
                "id": "bcb_012",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def dataframe_from_records(records: list, dtypes: dict = None) -> object:\n"
                    "    ...\n\n"
                    "Use `pandas` to create a DataFrame from a list of dicts (`records`). "
                    "If `dtypes` is provided, cast each column to the specified dtype using `astype`. "
                    "Return the DataFrame. Include a docstring."
                ),
                "expected": "def dataframe_from_records",
                "expected_keywords": ["pandas", "pd.DataFrame", "astype", "def dataframe_from_records"],
            },
            {
                "id": "bcb_013",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def running_statistics(numbers: list) -> dict:\n"
                    "    ...\n\n"
                    "Use `numpy` to compute and return a dict with keys 'mean', 'std', 'min', 'max', "
                    "and 'median' for the provided list of numbers. Round each value to 4 decimal places. "
                    "Include a docstring."
                ),
                "expected": "def running_statistics",
                "expected_keywords": ["numpy", "np.mean", "np.std", "np.median", "def running_statistics"],
            },
            {
                "id": "bcb_014",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def business_days_between(start: str, end: str) -> int:\n"
                    "    ...\n\n"
                    "Use the `datetime` module (and only the standard library) to return the number of "
                    "weekdays (Monday-Friday) between `start` and `end` date strings in 'YYYY-MM-DD' format, "
                    "inclusive of start, exclusive of end. Include a docstring."
                ),
                "expected": "def business_days_between",
                "expected_keywords": ["datetime", "strptime", "weekday", "timedelta", "def business_days_between"],
            },
            {
                "id": "bcb_015",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def safe_read_text(path: str, encoding: str = 'utf-8') -> str:\n"
                    "    ...\n\n"
                    "Use `pathlib.Path` to read and return the text content of the file at `path`. "
                    "If the file does not exist, return an empty string. Include a docstring."
                ),
                "expected": "def safe_read_text",
                "expected_keywords": ["pathlib", "Path", "read_text", "exists", "def safe_read_text"],
            },
            {
                "id": "bcb_016",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def pretty_print_json(data: dict, indent: int = 2) -> str:\n"
                    "    ...\n\n"
                    "Use the `json` module to serialize `data` to a pretty-printed JSON string with "
                    "the given `indent`. Ensure non-ASCII characters are preserved (ensure_ascii=False). "
                    "Include a docstring."
                ),
                "expected": "def pretty_print_json",
                "expected_keywords": ["json", "json.dumps", "indent", "ensure_ascii", "def pretty_print_json"],
            },
            {
                "id": "bcb_017",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def parse_log_levels(log_text: str) -> dict:\n"
                    "    ...\n\n"
                    "Use the `re` module to scan `log_text` for lines containing log levels "
                    "(DEBUG, INFO, WARNING, ERROR, CRITICAL) and use `collections.Counter` to return "
                    "a dict mapping each level to its occurrence count. Include a docstring."
                ),
                "expected": "def parse_log_levels",
                "expected_keywords": ["re", "collections", "Counter", "findall", "def parse_log_levels"],
            },
            {
                "id": "bcb_018",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def chunked(iterable, size: int) -> list:\n"
                    "    ...\n\n"
                    "Use `itertools.islice` to split `iterable` into consecutive chunks of length `size` "
                    "(the last chunk may be shorter). Return a list of lists. Include a docstring."
                ),
                "expected": "def chunked",
                "expected_keywords": ["itertools", "islice", "iter(", "def chunked"],
            },
            {
                "id": "bcb_019",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def compose(*functions):\n"
                    "    ...\n\n"
                    "Use `functools.reduce` to compose an arbitrary number of single-argument functions "
                    "so that `compose(f, g, h)(x)` is equivalent to `f(g(h(x)))`. "
                    "Return the composed function. Include a docstring."
                ),
                "expected": "def compose",
                "expected_keywords": ["functools", "reduce", "lambda", "def compose"],
            },
            {
                "id": "bcb_020",
                "prompt": (
                    "Write a complete Python function with the following signature:\n\n"
                    "def http_retry(url: str, retries: int = 3, backoff: float = 1.0) -> dict:\n"
                    "    ...\n\n"
                    "Use `requests` and `time` (standard library) to GET `url` with up to `retries` attempts. "
                    "On a non-2xx response or connection error, wait `backoff * attempt` seconds before retrying. "
                    "Return the parsed JSON on success, or raise the last exception on failure. Include a docstring."
                ),
                "expected": "def http_retry",
                "expected_keywords": ["requests", "time", "sleep", "raise_for_status", "def http_retry"],
            },
        ]

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a BigCodeBench response.

        Score = (fraction of expected_keywords present) + 0.2 bonus if a docstring or
        test block is present, capped at 1.0.
        """
        expected_keywords: List[str] = prompt_data.get("expected_keywords", [])
        response_lower = response.lower()

        def keyword_present(kw: str) -> bool:
            return kw.lower() in response_lower

        if not expected_keywords:
            keyword_score = 0.0
        else:
            hits = sum(1 for kw in expected_keywords if keyword_present(kw))
            keyword_score = hits / len(expected_keywords)

        has_docstring = '"""' in response or "'''" in response
        has_tests = "__main__" in response or "def test_" in response or "assert " in response
        bonus = 0.2 if (has_docstring or has_tests) else 0.0

        raw_score = keyword_score + bonus
        score = min(1.0, raw_score)
        success = score >= 0.6

        matched = [kw for kw in expected_keywords if keyword_present(kw)]
        missing = [kw for kw in expected_keywords if not keyword_present(kw)]

        return {
            "success": success,
            "score": round(score, 4),
            "metadata": {
                "keyword_score": round(keyword_score, 4),
                "has_docstring": has_docstring,
                "has_tests": has_tests,
                "bonus_applied": bonus > 0,
                "matched_keywords": matched,
                "missing_keywords": missing,
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are an expert Python engineer. Write complete, correct, and well-documented "
            "Python functions using the specified libraries. Always include imports at the top "
            "of your code and a docstring for the function."
        )
