"""SWE-bench benchmark - Software engineering task completion."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class SWEBenchBenchmark(Benchmark):
    """SWE-bench style software engineering benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="swe_bench",
            description="Software engineering task completion",
            category="code",
            version="1.0",
            timeout=120,
            max_tokens=2048,
            temperature=0.2
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic software engineering task prompts."""
        self.prompts = [
            {
                "id": "swe_001",
                "prompt": """Fix the bug in this Python function:

```python
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
```

The function crashes when given an empty list. Fix it.""",
                "expected": "def calculate_average(numbers):\n    if not numbers:\n        return 0\n    total = 0\n    for num in numbers:\n        total += num\n    return total / len(numbers)",
                "test_cases": [{"input": [[]], "expected": 0}, {"input": [[1, 2, 3]], "expected": 2.0}]
            },
            {
                "id": "swe_002",
                "prompt": """Fix the bug in this Python function:

```python
def find_max(lst):
    max_val = 0
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val
```

The function returns incorrect results for lists with all negative numbers. Fix it.""",
                "expected": "def find_max(lst):\n    if not lst:\n        return None\n    max_val = lst[0]\n    for item in lst:\n        if item > max_val:\n            max_val = item\n    return max_val",
                "test_cases": [{"input": [[-5, -3, -10]], "expected": -3}, {"input": [[]], "expected": None}]
            },
            {
                "id": "swe_003",
                "prompt": """Fix the bug in this Python function:

```python
def parse_date(date_str):
    parts = date_str.split('-')
    year = parts[0]
    month = parts[1]
    day = parts[2]
    return {'year': year, 'month': month, 'day': day}
```

The function doesn't handle different date formats. Fix it to handle both 'YYYY-MM-DD' and 'MM/DD/YYYY'.""",
                "expected": "def parse_date(date_str):\n    if '/' in date_str:\n        parts = date_str.split('/')\n        return {'month': parts[0], 'day': parts[1], 'year': parts[2]}\n    parts = date_str.split('-')\n    return {'year': parts[0], 'month': parts[1], 'day': parts[2]}",
                "test_cases": [{"input": ["2024-03-15"], "expected": {'year': '2024', 'month': '03', 'day': '15'}}, {"input": ["03/15/2024"], "expected": {'month': '03', 'day': '15', 'year': '2024'}}]
            },
            {
                "id": "swe_004",
                "prompt": """Fix the bug in this Python function:

```python
def merge_dicts(dict1, dict2):
    result = dict1
    for key, value in dict2.items():
        result[key] = value
    return result
```

The function modifies the original dict1. Fix it to not mutate the input.""",
                "expected": "def merge_dicts(dict1, dict2):\n    result = dict1.copy()\n    for key, value in dict2.items():\n        result[key] = value\n    return result",
                "test_cases": [{"input": [{"a": 1}, {"b": 2}], "expected": {"a": 1, "b": 2}}]
            },
            {
                "id": "swe_005",
                "prompt": """Fix the bug in this Python function:

```python
def read_file_lines(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    return lines
```

The file is never closed. Fix the resource leak.""",
                "expected": "def read_file_lines(filename):\n    with open(filename, 'r') as f:\n        return f.readlines()",
                "test_cases": [{"input": ["test.txt"], "expected": ["line1\\n", "line2\\n"]}]
            },
            {
                "id": "swe_006",
                "prompt": """Fix the bug in this Python function:

```python
def remove_duplicates(items):
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen
```

The function has O(n²) complexity. Optimize it.""",
                "expected": "def remove_duplicates(items):\n    seen = set()\n    result = []\n    for item in items:\n        if item not in seen:\n            seen.add(item)\n            result.append(item)\n    return result",
                "test_cases": [{"input": [[1, 2, 2, 3, 3, 3]], "expected": [1, 2, 3]}]
            },
            {
                "id": "swe_007",
                "prompt": """Fix the bug in this Python function:

```python
def format_currency(amount):
    return '$' + str(amount)
```

The function doesn't format decimals correctly. Fix it to always show 2 decimal places.""",
                "expected": "def format_currency(amount):\n    return f'${amount:.2f}'",
                "test_cases": [{"input": [10], "expected": "$10.00"}, {"input": [10.5], "expected": "$10.50"}]
            },
            {
                "id": "swe_008",
                "prompt": """Fix the bug in this Python function:

```python
def is_valid_email(email):
    return '@' in email
```

The validation is too loose. Fix it to properly validate email format.""",
                "expected": "import re\ndef is_valid_email(email):\n    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'\n    return bool(re.match(pattern, email))",
                "test_cases": [{"input": ["test@example.com"], "expected": True}, {"input": ["invalid"], "expected": False}]
            },
            {
                "id": "swe_009",
                "prompt": """Fix the bug in this Python function:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

The function is very slow for large n. Optimize it.""",
                "expected": "def fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
                "test_cases": [{"input": [10], "expected": 55}, {"input": [20], "expected": 6765}]
            },
            {
                "id": "swe_010",
                "prompt": """Fix the bug in this Python function:

```python
def sort_by_key(items, key_func):
    return items.sort(key=key_func)
```

The function returns None. Fix it to return the sorted list.""",
                "expected": "def sort_by_key(items, key_func):\n    return sorted(items, key=key_func)",
                "test_cases": [{"input": [[3, 1, 2], lambda x: x], "expected": [1, 2, 3]}]
            },
            {
                "id": "swe_011",
                "prompt": """Fix the bug in this Python function:

```python
def get_user_data(user_id):
    users = {
        '1': {'name': 'Alice', 'age': 30},
        '2': {'name': 'Bob', 'age': 25}
    }
    return users[user_id]
```

The function raises KeyError for missing users. Fix it to return None instead.""",
                "expected": "def get_user_data(user_id):\n    users = {\n        '1': {'name': 'Alice', 'age': 30},\n        '2': {'name': 'Bob', 'age': 25}\n    }\n    return users.get(user_id)",
                "test_cases": [{"input": ["1"], "expected": {'name': 'Alice', 'age': 30}}, {"input": ["999"], "expected": None}]
            },
            {
                "id": "swe_012",
                "prompt": """Fix the bug in this Python function:

```python
def chunk_list(items, size):
    chunks = []
    for i in range(0, len(items), size):
        chunks.append(items[i:i+size])
    return chunks
```

The function works but could be more Pythonic. Improve it.""",
                "expected": "def chunk_list(items, size):\n    return [items[i:i+size] for i in range(0, len(items), size)]",
                "test_cases": [{"input": [[1, 2, 3, 4, 5], 2], "expected": [[1, 2], [3, 4], [5]]}]
            },
            {
                "id": "swe_013",
                "prompt": """Fix the bug in this Python function:

```python
def safe_divide(a, b):
    return a / b
```

The function crashes on division by zero. Fix it.""",
                "expected": "def safe_divide(a, b):\n    if b == 0:\n        return None\n    return a / b",
                "test_cases": [{"input": [10, 2], "expected": 5.0}, {"input": [10, 0], "expected": None}]
            },
            {
                "id": "swe_014",
                "prompt": """Fix the bug in this Python function:

```python
def flatten(nested):
    result = []
    for item in nested:
        if isinstance(item, list):
            result.append(item)
        else:
            result.append(item)
    return result
```

The function doesn't actually flatten nested lists. Fix it.""",
                "expected": "def flatten(nested):\n    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result",
                "test_cases": [{"input": [[1, [2, 3], 4]], "expected": [1, 2, 3, 4]}]
            },
            {
                "id": "swe_015",
                "prompt": """Fix the bug in this Python function:

```python
def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length]
    return s
```

The function should add '...' when truncating. Fix it.""",
                "expected": "def truncate_string(s, max_length):\n    if len(s) > max_length:\n        return s[:max_length-3] + '...'\n    return s",
                "test_cases": [{"input": ["hello world", 8], "expected": "hello..."}, {"input": ["hi", 8], "expected": "hi"}]
            },
            {
                "id": "swe_016",
                "prompt": """Fix the bug in this Python function:

```python
def parse_json(data):
    import json
    return json.loads(data)
```

The function raises exceptions on invalid JSON. Fix it to return None on error.""",
                "expected": "import json\ndef parse_json(data):\n    try:\n        return json.loads(data)\n    except json.JSONDecodeError:\n        return None",
                "test_cases": [{"input": ['{"key": "value"}'], "expected": {'key': 'value'}}, {"input": ["invalid"], "expected": None}]
            },
            {
                "id": "swe_017",
                "prompt": """Fix the bug in this Python function:

```python
def count_words(text):
    return len(text.split(' '))
```

The function counts empty strings and multiple spaces as words. Fix it.""",
                "expected": "def count_words(text):\n    return len(text.split())",
                "test_cases": [{"input": ["hello world"], "expected": 2}, {"input": ["  hello   world  "], "expected": 2}]
            },
            {
                "id": "swe_018",
                "prompt": """Fix the bug in this Python function:

```python
def retry(func, max_attempts):
    for i in range(max_attempts):
        try:
            return func()
        except:
            continue
    raise Exception("Max retries exceeded")
```

The function catches all exceptions including KeyboardInterrupt. Fix it.""",
                "expected": "def retry(func, max_attempts):\n    for i in range(max_attempts):\n        try:\n            return func()\n        except Exception:\n            if i == max_attempts - 1:\n                raise\n            continue",
                "test_cases": [{"input": [lambda: 42, 3], "expected": 42}]
            },
            {
                "id": "swe_019",
                "prompt": """Fix the bug in this Python function:

```python
def unique_elements(lst):
    return list(set(lst))
```

The function loses the original order. Fix it to preserve order.""",
                "expected": "def unique_elements(lst):\n    seen = set()\n    result = []\n    for item in lst:\n        if item not in seen:\n            seen.add(item)\n            result.append(item)\n    return result",
                "test_cases": [{"input": [[3, 1, 2, 1, 3]], "expected": [3, 1, 2]}]
            },
            {
                "id": "swe_020",
                "prompt": """Fix the bug in this Python function:

```python
def calculate_stats(numbers):
    return {
        'mean': sum(numbers) / len(numbers),
        'max': max(numbers),
        'min': min(numbers)
    }
```

The function crashes on empty list. Fix it.""",
                "expected": "def calculate_stats(numbers):\n    if not numbers:\n        return None\n    return {\n        'mean': sum(numbers) / len(numbers),\n        'max': max(numbers),\n        'min': min(numbers)\n    }",
                "test_cases": [{"input": [[1, 2, 3, 4, 5]], "expected": {'mean': 3.0, 'max': 5, 'min': 1}}, {"input": [[]], "expected": None}]
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a SWE-bench response."""
        expected = prompt_data.get("expected", "")
        
        # Extract code from response
        code_match = re.search(r'```(?:python)?\n(.*?)```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            lines = response.split('\n')
            code_lines = []
            for line in lines:
                if line.strip().startswith('def ') or line.strip().startswith('import '):
                    code_lines.append(line)
                elif code_lines:
                    code_lines.append(line)
            code = '\n'.join(code_lines) if code_lines else response
        
        if not code.strip():
            return {
                "success": False,
                "score": 0.0,
                "feedback": "No code found in response",
                "extracted_code": None
            }
        
        # Score based on code similarity
        score = 0.0
        feedback = []
        
        expected_clean = re.sub(r'\s+', ' ', expected.lower())
        code_clean = re.sub(r'\s+', ' ', code.lower())
        
        if 'def ' in code:
            score += 0.3
            feedback.append("Function definition found")
        
        if expected_clean and code_clean:
            expected_parts = expected_clean.split()
            code_parts = code_clean.split()
            matches = sum(1 for p in expected_parts if p in code_parts)
            if expected_parts:
                similarity = matches / len(expected_parts)
                score += similarity * 0.5
                if similarity > 0.5:
                    feedback.append("Code structure matches expected")
        
        if 'return' in code:
            score += 0.1
            feedback.append("Return statement present")
        
        if 'if' in code or 'try' in code:
            score += 0.1
            feedback.append("Control flow present")
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Code analyzed",
            "extracted_code": code[:300]
        }
    
    def get_system_prompt(self) -> str:
        return "You are a Python expert. Fix the bug in the provided code. Return only the fixed function."
