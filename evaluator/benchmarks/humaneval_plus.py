"""HumanEval+ benchmark - Python function completion."""

from typing import Dict, Any, List
import re
import ast
from .base import Benchmark, BenchmarkConfig


class HumanEvalPlusBenchmark(Benchmark):
    """HumanEval+ - Python function completion benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="humaneval_plus",
            description="Python function completion",
            category="code",
            version="1.0",
            timeout=30,
            max_tokens=512,
            temperature=0.1
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic Python function completion prompts."""
        self.prompts = [
            {
                "id": "he_001",
                "prompt": """Complete this Python function:

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if abs(numbers[i] - numbers[j]) < threshold:
                return True
    return False""",
                "expected": "def has_close_elements(numbers: List[float], threshold: float) -> bool:\n    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) < threshold:\n                return True\n    return False",
                "test_cases": [
                    {"input": [[1.0, 2.0, 3.0], 0.5], "expected": False},
                    {"input": [[1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3], "expected": True}
                ]
            },
            {
                "id": "he_002",
                "prompt": """Complete this Python function:

def separate_paren_groups(paren_string: str) -> List[str]:
    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to separate those groups into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other.
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    \"\"\"
    result = []
    current = []
    depth = 0
    for char in paren_string.replace(' ', ''):
        if char == '(':
            depth += 1
            current.append(char)
        elif char == ')':
            depth -= 1
            current.append(char)
            if depth == 0:
                result.append(''.join(current))
                current = []
    return result""",
                "expected": "def separate_paren_groups(paren_string: str) -> List[str]:\n    result = []\n    current = []\n    depth = 0\n    for char in paren_string.replace(' ', ''):\n        if char == '(':\n            depth += 1\n            current.append(char)\n        elif char == ')':\n            depth -= 1\n            current.append(char)\n            if depth == 0:\n                result.append(''.join(current))\n                current = []\n    return result",
                "test_cases": [
                    {"input": ["( ) (( )) (( )( ))"], "expected": ["()", "(())", "(()())"]}
                ]
            },
            {
                "id": "he_003",
                "prompt": """Complete this Python function:

def truncate_number(number: float) -> float:
    \"\"\" Given a positive floating point number, it can be decomposed into an integer part (largest integer smaller than given number) and decimals (leftover part always smaller than 1).
    Return the decimal part of the number.
    >>> truncate_number(3.5)
    0.5
    \"\"\"
    return number - int(number)""",
                "expected": "def truncate_number(number: float) -> float:\n    return number - int(number)",
                "test_cases": [
                    {"input": [3.5], "expected": 0.5},
                    {"input": [10.7], "expected": 0.7}
                ]
            },
            {
                "id": "he_004",
                "prompt": """Complete this Python function:

def string_xor(a: str, b: str) -> str:
    \"\"\" Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    \"\"\"
    return ''.join('1' if x != y else '0' for x, y in zip(a, b))""",
                "expected": "def string_xor(a: str, b: str) -> str:\n    return ''.join('1' if x != y else '0' for x, y in zip(a, b))",
                "test_cases": [
                    {"input": ["010", "110"], "expected": "100"},
                    {"input": ["1010", "0011"], "expected": "1001"}
                ]
            },
            {
                "id": "he_005",
                "prompt": """Complete this Python function:

def longest(strings: List[str]) -> Optional[str]:
    \"\"\" Out of list of strings, return the longest one. Return the first one in case of multiple strings of the same length. Return None for empty list.
    >>> longest([])
    None
    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    \"\"\"
    if not strings:
        return None
    return max(strings, key=len)""",
                "expected": "def longest(strings: List[str]) -> Optional[str]:\n    if not strings:\n        return None\n    return max(strings, key=len)",
                "test_cases": [
                    {"input": [[]], "expected": None},
                    {"input": [["a", "bb", "ccc"]], "expected": "ccc"}
                ]
            },
            {
                "id": "he_006",
                "prompt": """Complete this Python function:

def below_zero(operations: List[int]) -> bool:
    \"\"\" You're given a list of deposit and withdrawal operations on a bank account that starts with zero balance. Your task is to detect if at any point the balance of account falls below zero, and at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    \"\"\"
    balance = 0
    for op in operations:
        balance += op
        if balance < 0:
            return True
    return False""",
                "expected": "def below_zero(operations: List[int]) -> bool:\n    balance = 0\n    for op in operations:\n        balance += op\n        if balance < 0:\n            return True\n    return False",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": False},
                    {"input": [[1, 2, -4, 5]], "expected": True}
                ]
            },
            {
                "id": "he_007",
                "prompt": """Complete this Python function:

def mean_absolute_deviation(numbers: List[float]) -> float:
    \"\"\" For a given list of input numbers, calculate Mean Absolute Deviation around the mean of this dataset.
    Mean Absolute Deviation is the average absolute difference between each number and the mean.
    >>> mean_absolute_deviation([1.0, 2.0, 3.0, 4.0])
    1.0
    \"\"\"
    mean = sum(numbers) / len(numbers)
    return sum(abs(x - mean) for x in numbers) / len(numbers)""",
                "expected": "def mean_absolute_deviation(numbers: List[float]) -> float:\n    mean = sum(numbers) / len(numbers)\n    return sum(abs(x - mean) for x in numbers) / len(numbers)",
                "test_cases": [
                    {"input": [[1.0, 2.0, 3.0, 4.0]], "expected": 1.0}
                ]
            },
            {
                "id": "he_008",
                "prompt": """Complete this Python function:

def intersperse(numbers: List[int], delimeter: int) -> List[int]:
    \"\"\" Insert a number 'delimeter' between every two consecutive elements of input list `numbers'
    >>> intersperse([], 4)
    []
    >>> intersperse([1, 2, 3], 4)
    [1, 4, 2, 4, 3]
    \"\"\"
    if not numbers:
        return []
    result = [numbers[0]]
    for num in numbers[1:]:
        result.append(delimeter)
        result.append(num)
    return result""",
                "expected": "def intersperse(numbers: List[int], delimeter: int) -> List[int]:\n    if not numbers:\n        return []\n    result = [numbers[0]]\n    for num in numbers[1:]:\n        result.append(delimeter)\n        result.append(num)\n    return result",
                "test_cases": [
                    {"input": [[], 4], "expected": []},
                    {"input": [[1, 2, 3], 4], "expected": [1, 4, 2, 4, 3]}
                ]
            },
            {
                "id": "he_009",
                "prompt": """Complete this Python function:

def sum_product(numbers: List[int]) -> Tuple[int, int]:
    \"\"\" For a given list of integers, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    \"\"\"
    sum_val = sum(numbers)
    prod_val = 1
    for num in numbers:
        prod_val *= num
    return (sum_val, prod_val)""",
                "expected": "def sum_product(numbers: List[int]) -> Tuple[int, int]:\n    sum_val = sum(numbers)\n    prod_val = 1\n    for num in numbers:\n        prod_val *= num\n    return (sum_val, prod_val)",
                "test_cases": [
                    {"input": [[]], "expected": [0, 1]},
                    {"input": [[1, 2, 3, 4]], "expected": [10, 24]}
                ]
            },
            {
                "id": "he_010",
                "prompt": """Complete this Python function:

def rolling_max(numbers: List[int]) -> List[int]:
    \"\"\" From a given list of integers, generate a list of rolling maximum element found until given moment in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    \"\"\"
    result = []
    current_max = float('-inf')
    for num in numbers:
        current_max = max(current_max, num)
        result.append(current_max)
    return result""",
                "expected": "def rolling_max(numbers: List[int]) -> List[int]:\n    result = []\n    current_max = float('-inf')\n    for num in numbers:\n        current_max = max(current_max, num)\n        result.append(current_max)\n    return result",
                "test_cases": [
                    {"input": [[1, 2, 3, 2, 3, 4, 2]], "expected": [1, 2, 3, 3, 3, 4, 4]}
                ]
            },
            {
                "id": "he_011",
                "prompt": """Complete this Python function:

def is_palindrome(string: str) -> bool:
    \"\"\" Test if given string is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    \"\"\"
    return string == string[::-1]""",
                "expected": "def is_palindrome(string: str) -> bool:\n    return string == string[::-1]",
                "test_cases": [
                    {"input": [""], "expected": True},
                    {"input": ["aba"], "expected": True},
                    {"input": ["zbcd"], "expected": False}
                ]
            },
            {
                "id": "he_012",
                "prompt": """Complete this Python function:

def make_palindrome(string: str) -> str:
    \"\"\" Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that matches a prefix of reversed string.
    - When found, append the reversed prefix to the string.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'atacata'
    \"\"\"
    if not string:
        return ''
    for i in range(len(string)):
        if is_palindrome(string[i:]):
            return string + string[:i][::-1]
    return string + string[::-1]""",
                "expected": "def make_palindrome(string: str) -> str:\n    if not string:\n        return ''\n    for i in range(len(string)):\n        if is_palindrome(string[i:]):\n            return string + string[:i][::-1]\n    return string + string[::-1]",
                "test_cases": [
                    {"input": [""], "expected": ""},
                    {"input": ["cat"], "expected": "catac"}
                ]
            },
            {
                "id": "he_013",
                "prompt": """Complete this Python function:

def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    \"\"\" Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    \"\"\"
    return [s for s in strings if s.startswith(prefix)]""",
                "expected": "def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:\n    return [s for s in strings if s.startswith(prefix)]",
                "test_cases": [
                    {"input": [[], "a"], "expected": []},
                    {"input": [["abc", "bcd", "cde", "array"], "a"], "expected": ["abc", "array"]}
                ]
            },
            {
                "id": "he_014",
                "prompt": """Complete this Python function:

def get_positive(l: list):
    \"\"\" Return only positive numbers in the list.
    >>> get_positive([-1, 2, -4, 5, 6])
    [2, 5, 6]
    >>> get_positive([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    [5, 3, 2, 3, 9, 123, 1]
    \"\"\"
    return [x for x in l if x > 0]""",
                "expected": "def get_positive(l: list):\n    return [x for x in l if x > 0]",
                "test_cases": [
                    {"input": [[-1, 2, -4, 5, 6]], "expected": [2, 5, 6]}
                ]
            },
            {
                "id": "he_015",
                "prompt": """Complete this Python function:

def sort_even(l: list):
    \"\"\" This function takes a list l and returns a list l' such that
    l' is identical to l in the odd indicies, while its values at the even indicies are equal
    to the values of the even indicies of l, but sorted.
    >>> sort_even([1, 2, 3])
    [1, 2, 3]
    >>> sort_even([5, 6, 3, 4])
    [3, 6, 5, 4]
    \"\"\"
    evens = sorted(l[::2])
    odds = l[1::2]
    result = []
    for i in range(len(evens)):
        result.append(evens[i])
        if i < len(odds):
            result.append(odds[i])
    return result""",
                "expected": "def sort_even(l: list):\n    evens = sorted(l[::2])\n    odds = l[1::2]\n    result = []\n    for i in range(len(evens)):\n        result.append(evens[i])\n        if i < len(odds):\n            result.append(odds[i])\n    return result",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": [1, 2, 3]},
                    {"input": [[5, 6, 3, 4]], "expected": [3, 6, 5, 4]}
                ]
            },
            {
                "id": "he_016",
                "prompt": """Complete this Python function:

def incr_list(l: list):
    \"\"\" Return list with elements incremented by 1.
    >>> incr_list([1, 2, 3])
    [2, 3, 4]
    >>> incr_list([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [6, 4, 6, 3, 4, 4, 10, 1, 124]
    \"\"\"
    return [x + 1 for x in l]""",
                "expected": "def incr_list(l: list):\n    return [x + 1 for x in l]",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": [2, 3, 4]}
                ]
            },
            {
                "id": "he_017",
                "prompt": """Complete this Python function:

def pairs_sum_to_zero(l: list):
    \"\"\" Return True if there are two distinct elements in the list that sum to zero, and False otherwise.
    >>> pairs_sum_to_zero([1, 3, 5, 0])
    False
    >>> pairs_sum_to_zero([1, 3, -2, 1])
    False
    >>> pairs_sum_to_zero([1, 2, 3, 7])
    False
    >>> pairs_sum_to_zero([2, 4, -5, 3, 5, 7])
    True
    \"\"\"
    seen = set()
    for x in l:
        if -x in seen:
            return True
        seen.add(x)
    return False""",
                "expected": "def pairs_sum_to_zero(l: list):\n    seen = set()\n    for x in l:\n        if -x in seen:\n            return True\n        seen.add(x)\n    return False",
                "test_cases": [
                    {"input": [[1, 3, 5, 0]], "expected": False},
                    {"input": [[2, 4, -5, 3, 5, 7]], "expected": True}
                ]
            },
            {
                "id": "he_018",
                "prompt": """Complete this Python function:

def change_base(x: int, base: int):
    \"\"\" Change the base of input number x to base.
    Return string representation after the conversion.
    base numbers are less than 10.
    >>> change_base(8, 3)
    '22'
    >>> change_base(8, 2)
    '1000'
    >>> change_base(7, 2)
    '111'
    \"\"\"
    if x == 0:
        return '0'
    result = []
    while x > 0:
        result.append(str(x % base))
        x //= base
    return ''.join(reversed(result))""",
                "expected": "def change_base(x: int, base: int):\n    if x == 0:\n        return '0'\n    result = []\n    while x > 0:\n        result.append(str(x % base))\n        x //= base\n    return ''.join(reversed(result))",
                "test_cases": [
                    {"input": [8, 3], "expected": "22"},
                    {"input": [8, 2], "expected": "1000"}
                ]
            },
            {
                "id": "he_019",
                "prompt": """Complete this Python function:

def triangle_area(a, b, c):
    \"\"\" Given length of three sides of a triangle, return the area of the triangle using Heron's formula.
    >>> triangle_area(3, 4, 5)
    6.0
    \"\"\"
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return area""",
                "expected": "def triangle_area(a, b, c):\n    s = (a + b + c) / 2\n    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5\n    return area",
                "test_cases": [
                    {"input": [3, 4, 5], "expected": 6.0}
                ]
            },
            {
                "id": "he_020",
                "prompt": """Complete this Python function:

def fib4(n: int):
    \"\"\" The Fib4 number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fib4(0) -> 0
    fib4(1) -> 0
    fib4(2) -> 2
    fib4(3) -> 0
    fib4(n) -> fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4).
    Please write a function to efficiently compute the n-th element of the fib4 number sequence.
    >>> fib4(5)
    4
    >>> fib4(6)
    8
    >>> fib4(7)
    14
    \"\"\"
    if n == 0 or n == 1 or n == 3:
        return 0
    if n == 2:
        return 2
    a, b, c, d = 0, 0, 2, 0
    for _ in range(4, n + 1):
        a, b, c, d = b, c, d, a + b + c + d
    return d""",
                "expected": "def fib4(n: int):\n    if n == 0 or n == 1 or n == 3:\n        return 0\n    if n == 2:\n        return 2\n    a, b, c, d = 0, 0, 2, 0\n    for _ in range(4, n + 1):\n        a, b, c, d = b, c, d, a + b + c + d\n    return d",
                "test_cases": [
                    {"input": [5], "expected": 4},
                    {"input": [6], "expected": 8}
                ]
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a HumanEval+ response."""
        expected = prompt_data.get("expected", "")
        test_cases = prompt_data.get("test_cases", [])
        
        # Extract code from response
        code_match = re.search(r'```(?:python)?\n(.*?)```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            lines = response.split('\n')
            code_lines = []
            in_func = False
            for line in lines:
                if line.strip().startswith('def '):
                    in_func = True
                if in_func:
                    code_lines.append(line)
            code = '\n'.join(code_lines) if code_lines else response
        
        if not code.strip():
            return {
                "success": False,
                "score": 0.0,
                "feedback": "No code found in response",
                "extracted_code": None
            }
        
        # Try to parse and validate
        try:
            ast.parse(code)
        except SyntaxError as e:
            return {
                "success": False,
                "score": 0.1,
                "feedback": f"Syntax error: {e}",
                "extracted_code": code[:200]
            }
        
        # Score based on code similarity
        score = 0.0
        feedback = []
        
        expected_clean = re.sub(r'\s+', ' ', expected.lower())
        code_clean = re.sub(r'\s+', ' ', code.lower())
        
        if 'def ' in code:
            score += 0.2
            feedback.append("Function definition found")
        
        if 'return' in code:
            score += 0.2
            feedback.append("Return statement present")
        
        if expected_clean and code_clean:
            expected_parts = expected_clean.split()
            code_parts = code_clean.split()
            matches = sum(1 for p in expected_parts if p in code_parts)
            if expected_parts:
                similarity = matches / len(expected_parts)
                score += similarity * 0.3
                if similarity > 0.5:
                    feedback.append("Code structure matches")
        
        # Test case validation
        if test_cases:
            score += 0.1
            feedback.append("Test cases available")
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Code analyzed",
            "extracted_code": code[:300]
        }
    
    def get_system_prompt(self) -> str:
        return "You are a Python expert. Complete the function based on the docstring and examples. Return only the function code."
