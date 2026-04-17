"""Terminal-Bench benchmark - CLI task completion."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class TerminalBenchBenchmark(Benchmark):
    """Terminal-Bench style CLI task completion benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="terminal_bench",
            description="CLI task completion",
            category="agent",
            version="1.0",
            timeout=60,
            max_tokens=512,
            temperature=0.1
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic terminal/bash task prompts."""
        self.prompts = [
            {
                "id": "term_001",
                "prompt": """You are in a bash shell. Complete this task:

Task: Find all files larger than 100MB in the current directory and its subdirectories.

Provide the bash command:""",
                "expected": "find . -type f -size +100M",
                "explanation": "Uses find with -size to locate files over 100MB"
            },
            {
                "id": "term_002",
                "prompt": """You are in a bash shell. Complete this task:

Task: Count the number of lines in all .py files in the current directory.

Provide the bash command:""",
                "expected": "find . -name '*.py' -exec wc -l {} +",
                "explanation": "Finds all .py files and counts lines using wc"
            },
            {
                "id": "term_003",
                "prompt": """You are in a bash shell. Complete this task:

Task: List all running processes sorted by memory usage (highest first).

Provide the bash command:""",
                "expected": "ps aux --sort=-%mem | head -20",
                "explanation": "Uses ps with memory sort and limits output"
            },
            {
                "id": "term_004",
                "prompt": """You are in a bash shell. Complete this task:

Task: Extract all unique IP addresses from a log file named access.log.

Provide the bash command:""",
                "expected": "grep -oE '\\b[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\b' access.log | sort -u",
                "explanation": "Uses regex grep to find IPs, then sorts uniquely"
            },
            {
                "id": "term_005",
                "prompt": """You are in a bash shell. Complete this task:

Task: Create a backup of a directory called 'project' with timestamp in the name.

Provide the bash command:""",
                "expected": "tar -czf project_$(date +%Y%m%d_%H%M%S).tar.gz project",
                "explanation": "Creates timestamped tar.gz archive of project"
            },
            {
                "id": "term_006",
                "prompt": """You are in a bash shell. Complete this task:

Task: Find and replace 'foo' with 'bar' in all .txt files recursively.

Provide the bash command:""",
                "expected": "find . -name '*.txt' -exec sed -i 's/foo/bar/g' {} +",
                "explanation": "Finds .txt files and uses sed for in-place replacement"
            },
            {
                "id": "term_007",
                "prompt": """You are in a bash shell. Complete this task:

Task: Show disk usage of all subdirectories in current directory, sorted by size.

Provide the bash command:""",
                "expected": "du -sh */ 2>/dev/null | sort -h",
                "explanation": "Uses du for disk usage and sorts human-readable sizes"
            },
            {
                "id": "term_008",
                "prompt": """You are in a bash shell. Complete this task:

Task: Kill all processes named 'python' owned by the current user.

Provide the bash command:""",
                "expected": "pkill -u $(whoami) python",
                "explanation": "Uses pkill with user filter to terminate python processes"
            },
            {
                "id": "term_009",
                "prompt": """You are in a bash shell. Complete this task:

Task: Monitor a log file in real-time and filter for lines containing 'ERROR'.

Provide the bash command:""",
                "expected": "tail -f logfile.log | grep 'ERROR'",
                "explanation": "Uses tail -f for real-time monitoring with grep filter"
            },
            {
                "id": "term_010",
                "prompt": """You are in a bash shell. Complete this task:

Task: Find all empty directories in the current directory tree.

Provide the bash command:""",
                "expected": "find . -type d -empty",
                "explanation": "Uses find with -empty flag to locate empty directories"
            },
            {
                "id": "term_011",
                "prompt": """You are in a bash shell. Complete this task:

Task: Download a file from URL and save it with a specific filename.

Provide the bash command:""",
                "expected": "curl -o filename.zip https://example.com/file.zip",
                "explanation": "Uses curl with -o to specify output filename"
            },
            {
                "id": "term_012",
                "prompt": """You are in a bash shell. Complete this task:

Task: Check if port 8080 is listening on localhost.

Provide the bash command:""",
                "expected": "netstat -tlnp | grep ':8080' || ss -tlnp | grep ':8080'",
                "explanation": "Uses netstat or ss to check listening ports"
            },
            {
                "id": "term_013",
                "prompt": """You are in a bash shell. Complete this task:

Task: Create a directory structure with nested folders: project/src/main.

Provide the bash command:""",
                "expected": "mkdir -p project/src/main",
                "explanation": "Uses mkdir -p to create nested directory structure"
            },
            {
                "id": "term_014",
                "prompt": """You are in a bash shell. Complete this task:

Task: Find files modified in the last 24 hours.

Provide the bash command:""",
                "expected": "find . -type f -mtime -1",
                "explanation": "Uses find with -mtime to find recently modified files"
            },
            {
                "id": "term_015",
                "prompt": """You are in a bash shell. Complete this task:

Task: Display the 10 most CPU-intensive processes.

Provide the bash command:""",
                "expected": "ps aux --sort=-%cpu | head -11",
                "explanation": "Sorts processes by CPU usage and shows top 10"
            },
            {
                "id": "term_016",
                "prompt": """You are in a bash shell. Complete this task:

Task: Create a symbolic link from /var/log/app.log to ~/logs/current.log.

Provide the bash command:""",
                "expected": "ln -s /var/log/app.log ~/logs/current.log",
                "explanation": "Uses ln -s to create a symbolic link"
            },
            {
                "id": "term_017",
                "prompt": """You are in a bash shell. Complete this task:

Task: Archive all .log files older than 7 days into old_logs.tar.gz.

Provide the bash command:""",
                "expected": "find . -name '*.log' -mtime +7 -exec tar -czf old_logs.tar.gz {} +",
                "explanation": "Finds old log files and archives them"
            },
            {
                "id": "term_018",
                "prompt": """You are in a bash shell. Complete this task:

Task: Show the difference between two files file1.txt and file2.txt.

Provide the bash command:""",
                "expected": "diff file1.txt file2.txt",
                "explanation": "Uses diff to compare two files"
            },
            {
                "id": "term_019",
                "prompt": """You are in a bash shell. Complete this task:

Task: Run a command every 5 seconds for 1 minute.

Provide the bash command:""",
                "expected": "for i in {1..12}; do command; sleep 5; done",
                "explanation": "Uses a loop with sleep to run command periodically"
            },
            {
                "id": "term_020",
                "prompt": """You are in a bash shell. Complete this task:

Task: Find all files with permissions 777 and change them to 755.

Provide the bash command:""",
                "expected": "find . -type f -perm 777 -exec chmod 755 {} +",
                "explanation": "Finds files with 777 permissions and changes to 755"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a shell command response."""
        expected = prompt_data.get("expected", "")
        
        # Extract command from response
        cmd_match = re.search(r'```(?:bash|sh)?\n(.*?)```', response, re.DOTALL)
        if not cmd_match:
            cmd_match = re.search(r'(?:command|bash|shell)[:\s]*\n?(.+?)(?:\n\n|\Z)', response, re.IGNORECASE | re.DOTALL)
        if not cmd_match:
            lines = [l.strip() for l in response.split('\n') if l.strip() and not l.strip().startswith('#')]
            if lines:
                cmd_match = type('obj', (object,), {'group': lambda self, x: lines[0]})()
        
        if not cmd_match:
            return {
                "success": False,
                "score": 0.0,
                "feedback": "No command found in response",
                "extracted_command": None
            }
        
        command = cmd_match.group(1).strip()
        
        # Score based on command similarity
        score = 0.0
        feedback = []
        
        expected_parts = expected.split()
        command_parts = command.split()
        
        if expected_parts and command_parts:
            if expected_parts[0] == command_parts[0]:
                score += 0.4
                feedback.append(f"Correct base command: {command_parts[0]}")
        
        expected_flags = set(p for p in expected_parts if p.startswith('-'))
        command_flags = set(p for p in command_parts if p.startswith('-'))
        if expected_flags:
            matching_flags = expected_flags & command_flags
            score += len(matching_flags) / len(expected_flags) * 0.3
            if matching_flags:
                feedback.append(f"Correct flags: {', '.join(matching_flags)}")
        
        if 'find' in command and 'find' in expected:
            score += 0.15
        if 'grep' in command and 'grep' in expected:
            score += 0.15
        if 'sed' in command and 'sed' in expected:
            score += 0.15
        if 'awk' in command and 'awk' in expected:
            score += 0.15
        
        if '|' in command and '|' in expected:
            score += 0.15
            feedback.append("Uses piping correctly")
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Command analyzed",
            "extracted_command": command[:200]
        }
    
    def get_system_prompt(self) -> str:
        return "You are a bash shell expert. Provide the exact command needed to complete the task. Return only the command without explanation."
