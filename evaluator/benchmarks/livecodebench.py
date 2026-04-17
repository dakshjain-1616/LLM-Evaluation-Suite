"""LiveCodeBench benchmark - Competitive programming."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class LiveCodeBenchBenchmark(Benchmark):
    """LiveCodeBench style competitive programming benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="livecodebench",
            description="Competitive programming problems",
            category="code",
            version="1.0",
            timeout=60,
            max_tokens=1024,
            temperature=0.1
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic competitive programming prompts."""
        self.prompts = [
            {
                "id": "lcb_001",
                "prompt": """Solve this competitive programming problem:

Problem: Two Sum
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

Input: nums = [2,7,11,15], target = 9
Output: [0,1]

Input: nums = [3,2,4], target = 6
Output: [1,2]

Write a Python function to solve this.""",
                "expected": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []",
                "test_cases": [
                    {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                    {"input": [[3, 2, 4], 6], "expected": [1, 2]}
                ]
            },
            {
                "id": "lcb_002",
                "prompt": """Solve this competitive programming problem:

Problem: Reverse Integer
Given a signed 32-bit integer x, return x with its digits reversed.
If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.

Input: x = 123
Output: 321

Input: x = -123
Output: -321

Write a Python function to solve this.""",
                "expected": "def reverse(x):\n    sign = -1 if x < 0 else 1\n    x = abs(x)\n    result = 0\n    while x > 0:\n        result = result * 10 + x % 10\n        x //= 10\n    result *= sign\n    if result < -2**31 or result > 2**31 - 1:\n        return 0\n    return result",
                "test_cases": [
                    {"input": [123], "expected": 321},
                    {"input": [-123], "expected": -321}
                ]
            },
            {
                "id": "lcb_003",
                "prompt": """Solve this competitive programming problem:

Problem: Palindrome Number
Given an integer x, return true if x is a palindrome, and false otherwise.

Input: x = 121
Output: true

Input: x = -121
Output: false

Write a Python function to solve this.""",
                "expected": "def is_palindrome(x):\n    if x < 0:\n        return False\n    return str(x) == str(x)[::-1]",
                "test_cases": [
                    {"input": [121], "expected": True},
                    {"input": [-121], "expected": False}
                ]
            },
            {
                "id": "lcb_004",
                "prompt": """Solve this competitive programming problem:

Problem: Roman to Integer
Given a roman numeral, convert it to an integer.

Input: s = \"III\"
Output: 3

Input: s = \"LVIII\"
Output: 58

Write a Python function to solve this.""",
                "expected": "def roman_to_int(s):\n    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}\n    total = 0\n    for i in range(len(s)):\n        if i > 0 and values[s[i]] > values[s[i-1]]:\n            total += values[s[i]] - 2 * values[s[i-1]]\n        else:\n            total += values[s[i]]\n    return total",
                "test_cases": [
                    {"input": ["III"], "expected": 3},
                    {"input": ["LVIII"], "expected": 58}
                ]
            },
            {
                "id": "lcb_005",
                "prompt": """Solve this competitive programming problem:

Problem: Longest Common Prefix
Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string \"\".

Input: strs = [\"flower\",\"flow\",\"flight\"]
Output: \"fl\"

Write a Python function to solve this.""",
                "expected": "def longest_common_prefix(strs):\n    if not strs:\n        return ''\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix:\n                return ''\n    return prefix",
                "test_cases": [
                    {"input": [["flower", "flow", "flight"]], "expected": "fl"},
                    {"input": [["dog", "racecar", "car"]], "expected": ""}
                ]
            },
            {
                "id": "lcb_006",
                "prompt": """Solve this competitive programming problem:

Problem: Valid Parentheses
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

Input: s = \"()\"
Output: true

Input: s = \"()[]{}\"
Output: true

Input: s = \"(]\"
Output: false

Write a Python function to solve this.""",
                "expected": "def is_valid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            if not stack or stack.pop() != mapping[char]:\n                return False\n        else:\n            stack.append(char)\n    return not stack",
                "test_cases": [
                    {"input": ["()"], "expected": True},
                    {"input": ["()[]{}"], "expected": True},
                    {"input": ["(]"], "expected": False}
                ]
            },
            {
                "id": "lcb_007",
                "prompt": """Solve this competitive programming problem:

Problem: Merge Two Sorted Lists
Merge two sorted linked lists and return it as a sorted list.

Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]

Write a Python function to solve this.""",
                "expected": "def merge_two_lists(list1, list2):\n    result = []\n    i = j = 0\n    while i < len(list1) and j < len(list2):\n        if list1[i] <= list2[j]:\n            result.append(list1[i])\n            i += 1\n        else:\n            result.append(list2[j])\n            j += 1\n    result.extend(list1[i:])\n    result.extend(list2[j:])\n    return result",
                "test_cases": [
                    {"input": [[1, 2, 4], [1, 3, 4]], "expected": [1, 1, 2, 3, 4, 4]}
                ]
            },
            {
                "id": "lcb_008",
                "prompt": """Solve this competitive programming problem:

Problem: Remove Duplicates from Sorted Array
Given a sorted array nums, remove the duplicates in-place such that each element appears only once and returns the new length.

Input: nums = [1,1,2]
Output: 2, nums = [1,2,_]

Write a Python function to solve this.""",
                "expected": "def remove_duplicates(nums):\n    if not nums:\n        return 0\n    i = 0\n    for j in range(1, len(nums)):\n        if nums[j] != nums[i]:\n            i += 1\n            nums[i] = nums[j]\n    return i + 1",
                "test_cases": [
                    {"input": [[1, 1, 2]], "expected": 2}
                ]
            },
            {
                "id": "lcb_009",
                "prompt": """Solve this competitive programming problem:

Problem: Implement strStr()
Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

Input: haystack = \"hello\", needle = \"ll\"
Output: 2

Input: haystack = \"aaaaa\", needle = \"bba\"
Output: -1

Write a Python function to solve this.""",
                "expected": "def str_str(haystack, needle):\n    if not needle:\n        return 0\n    return haystack.find(needle)",
                "test_cases": [
                    {"input": ["hello", "ll"], "expected": 2},
                    {"input": ["aaaaa", "bba"], "expected": -1}
                ]
            },
            {
                "id": "lcb_010",
                "prompt": """Solve this competitive programming problem:

Problem: Search Insert Position
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

Input: nums = [1,3,5,6], target = 5
Output: 2

Input: nums = [1,3,5,6], target = 2
Output: 1

Write a Python function to solve this.""",
                "expected": "def search_insert(nums, target):\n    left, right = 0, len(nums)\n    while left < right:\n        mid = (left + right) // 2\n        if nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid\n    return left",
                "test_cases": [
                    {"input": [[1, 3, 5, 6], 5], "expected": 2},
                    {"input": [[1, 3, 5, 6], 2], "expected": 1}
                ]
            },
            {
                "id": "lcb_011",
                "prompt": """Solve this competitive programming problem:

Problem: Maximum Subarray
Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.

Write a Python function to solve this.""",
                "expected": "def max_sub_array(nums):\n    max_sum = current_sum = nums[0]\n    for num in nums[1:]:\n        current_sum = max(num, current_sum + num)\n        max_sum = max(max_sum, current_sum)\n    return max_sum",
                "test_cases": [
                    {"input": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6}
                ]
            },
            {
                "id": "lcb_012",
                "prompt": """Solve this competitive programming problem:

Problem: Length of Last Word
Given a string s consisting of words and spaces, return the length of the last word in the string.

Input: s = \"Hello World\"
Output: 5

Input: s = \"   fly me   to   the moon  \"
Output: 4

Write a Python function to solve this.""",
                "expected": "def length_of_last_word(s):\n    return len(s.strip().split()[-1])",
                "test_cases": [
                    {"input": ["Hello World"], "expected": 5},
                    {"input": ["   fly me   to   the moon  "], "expected": 4}
                ]
            },
            {
                "id": "lcb_013",
                "prompt": """Solve this competitive programming problem:

Problem: Plus One
Given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. Increment the large integer by one and return the resulting array of digits.

Input: digits = [1,2,3]
Output: [1,2,4]

Input: digits = [9,9,9]
Output: [1,0,0,0]

Write a Python function to solve this.""",
                "expected": "def plus_one(digits):\n    n = len(digits)\n    for i in range(n - 1, -1, -1):\n        if digits[i] < 9:\n            digits[i] += 1\n            return digits\n        digits[i] = 0\n    return [1] + digits",
                "test_cases": [
                    {"input": [[1, 2, 3]], "expected": [1, 2, 4]},
                    {"input": [[9, 9, 9]], "expected": [1, 0, 0, 0]}
                ]
            },
            {
                "id": "lcb_014",
                "prompt": """Solve this competitive programming problem:

Problem: Add Binary
Given two binary strings a and b, return their sum as a binary string.

Input: a = \"11\", b = \"1\"
Output: \"100\"

Input: a = \"1010\", b = \"1011\"
Output: \"10101\"

Write a Python function to solve this.""",
                "expected": "def add_binary(a, b):\n    result = []\n    carry = 0\n    i, j = len(a) - 1, len(b) - 1\n    while i >= 0 or j >= 0 or carry:\n        total = carry\n        if i >= 0:\n            total += int(a[i])\n            i -= 1\n        if j >= 0:\n            total += int(b[j])\n            j -= 1\n        result.append(str(total % 2))\n        carry = total // 2\n    return ''.join(reversed(result))",
                "test_cases": [
                    {"input": ["11", "1"], "expected": "100"},
                    {"input": ["1010", "1011"], "expected": "10101"}
                ]
            },
            {
                "id": "lcb_015",
                "prompt": """Solve this competitive programming problem:

Problem: Climbing Stairs
You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Input: n = 2
Output: 2

Input: n = 3
Output: 3

Write a Python function to solve this.""",
                "expected": "def climb_stairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b",
                "test_cases": [
                    {"input": [2], "expected": 2},
                    {"input": [3], "expected": 3}
                ]
            },
            {
                "id": "lcb_016",
                "prompt": """Solve this competitive programming problem:

Problem: Sqrt(x)
Given a non-negative integer x, return the square root of x rounded down to the nearest integer.

Input: x = 4
Output: 2

Input: x = 8
Output: 2

Write a Python function to solve this.""",
                "expected": "def my_sqrt(x):\n    if x < 2:\n        return x\n    left, right = 1, x // 2\n    while left <= right:\n        mid = (left + right) // 2\n        if mid * mid == x:\n            return mid\n        elif mid * mid < x:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return right",
                "test_cases": [
                    {"input": [4], "expected": 2},
                    {"input": [8], "expected": 2}
                ]
            },
            {
                "id": "lcb_017",
                "prompt": """Solve this competitive programming problem:

Problem: Delete Node in a Linked List
Write a function to delete a node in a singly-linked list. You will not be given access to the head of the list, instead you will be given access to the node to be deleted directly.

Input: head = [4,5,1,9], node = 5
Output: [4,1,9]

Write a Python function to solve this.""",
                "expected": "def delete_node(node):\n    node.val = node.next.val\n    node.next = node.next.next",
                "test_cases": []
            },
            {
                "id": "lcb_018",
                "prompt": """Solve this competitive programming problem:

Problem: Reverse Linked List
Given the head of a singly linked list, reverse the list, and return the reversed list.

Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]

Write a Python function to solve this.""",
                "expected": "def reverse_list(head):\n    prev = None\n    current = head\n    while current:\n        next_temp = current.next\n        current.next = prev\n        prev = current\n        current = next_temp\n    return prev",
                "test_cases": [
                    {"input": [[1, 2, 3, 4, 5]], "expected": [5, 4, 3, 2, 1]}
                ]
            },
            {
                "id": "lcb_019",
                "prompt": """Solve this competitive programming problem:

Problem: Contains Duplicate
Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.

Input: nums = [1,2,3,1]
Output: true

Input: nums = [1,2,3,4]
Output: false

Write a Python function to solve this.""",
                "expected": "def contains_duplicate(nums):\n    return len(nums) != len(set(nums))",
                "test_cases": [
                    {"input": [[1, 2, 3, 1]], "expected": True},
                    {"input": [[1, 2, 3, 4]], "expected": False}
                ]
            },
            {
                "id": "lcb_020",
                "prompt": """Solve this competitive programming problem:

Problem: Missing Number
Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.

Input: nums = [3,0,1]
Output: 2

Input: nums = [0,1]
Output: 2

Write a Python function to solve this.""",
                "expected": "def missing_number(nums):\n    n = len(nums)\n    expected_sum = n * (n + 1) // 2\n    actual_sum = sum(nums)\n    return expected_sum - actual_sum",
                "test_cases": [
                    {"input": [[3, 0, 1]], "expected": 2},
                    {"input": [[0, 1]], "expected": 2}
                ]
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a LiveCodeBench response."""
        expected = prompt_data.get("expected", "")
        
        # Extract code from response
        code_match = re.search(r'```(?:python)?\n(.*?)```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            lines = response.split('\n')
            code_lines = []
            for line in lines:
                if line.strip().startswith('def '):
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
                    feedback.append("Algorithm matches expected")
        
        if 'return' in code:
            score += 0.1
            feedback.append("Return statement present")
        
        if 'for' in code or 'while' in code:
            score += 0.1
            feedback.append("Loop structure present")
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Code analyzed",
            "extracted_code": code[:300]
        }
    
    def get_system_prompt(self) -> str:
        return "You are a competitive programmer. Solve the given problem efficiently. Return only the solution function."
