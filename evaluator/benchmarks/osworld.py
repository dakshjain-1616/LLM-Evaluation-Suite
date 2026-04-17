"""OSWorld benchmark - GUI agent task completion."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class OSWorldBenchmark(Benchmark):
    """OSWorld style GUI agent task benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="osworld",
            description="GUI agent task completion",
            category="agent",
            version="1.0",
            timeout=120,
            max_tokens=1024,
            temperature=0.2
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic GUI agent task prompts."""
        self.prompts = [
            {
                "id": "osw_001",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the calculator application and calculate 15 * 23.

Provide step-by-step actions:""",
                "expected": ["Click Start menu", "Search for Calculator", "Open Calculator", "Click 1", "Click 5", "Click *", "Click 2", "Click 3", "Click ="],
                "explanation": "Opens calculator and performs multiplication"
            },
            {
                "id": "osw_002",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Create a new folder named 'Project' on the Desktop.

Provide step-by-step actions:""",
                "expected": ["Right-click on Desktop", "Select 'New'", "Select 'Folder'", "Type 'Project'", "Press Enter"],
                "explanation": "Creates new folder on desktop"
            },
            {
                "id": "osw_003",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open Chrome browser and navigate to google.com.

Provide step-by-step actions:""",
                "expected": ["Click Chrome icon", "Wait for browser to open", "Click address bar", "Type 'google.com'", "Press Enter"],
                "explanation": "Opens Chrome and navigates to Google"
            },
            {
                "id": "osw_004",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Change the desktop wallpaper to a solid blue color.

Provide step-by-step actions:""",
                "expected": ["Right-click Desktop", "Select 'Personalize'", "Click 'Background'", "Select 'Solid color'", "Choose blue color", "Click Apply"],
                "explanation": "Changes desktop background to blue"
            },
            {
                "id": "osw_005",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open Notepad, type 'Hello World', and save the file as test.txt on Desktop.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Search 'Notepad'", "Open Notepad", "Type 'Hello World'", "Press Ctrl+S", "Navigate to Desktop", "Type 'test.txt'", "Click Save"],
                "explanation": "Creates and saves text file"
            },
            {
                "id": "osw_006",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Take a screenshot and save it to the Pictures folder.

Provide step-by-step actions:""",
                "expected": ["Press Print Screen key", "Open Paint", "Press Ctrl+V", "Press Ctrl+S", "Navigate to Pictures folder", "Type filename", "Click Save"],
                "explanation": "Captures and saves screenshot"
            },
            {
                "id": "osw_007",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open File Explorer and navigate to Documents folder.

Provide step-by-step actions:""",
                "expected": ["Click File Explorer icon", "Click Documents in left sidebar"],
                "explanation": "Opens File Explorer to Documents"
            },
            {
                "id": "osw_008",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open Settings and check for Windows updates.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Click Settings gear icon", "Click 'Update & Security'", "Click 'Check for updates'"],
                "explanation": "Checks for Windows updates"
            },
            {
                "id": "osw_009",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Copy a file from Downloads to Desktop.

Provide step-by-step actions:""",
                "expected": ["Open File Explorer", "Navigate to Downloads", "Right-click file", "Select Copy", "Navigate to Desktop", "Right-click", "Select Paste"],
                "explanation": "Copies file between folders"
            },
            {
                "id": "osw_010",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open Task Manager and end a process named 'notepad.exe'.

Provide step-by-step actions:""",
                "expected": ["Press Ctrl+Shift+Esc", "Click 'More details' if needed", "Find notepad.exe", "Click on it", "Click 'End task'"],
                "explanation": "Opens Task Manager and ends process"
            },
            {
                "id": "osw_011",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Connect to a Wi-Fi network named 'HomeNetwork' with password 'password123'.

Provide step-by-step actions:""",
                "expected": ["Click Wi-Fi icon in system tray", "Select 'HomeNetwork'", "Click Connect", "Type 'password123'", "Click Next"],
                "explanation": "Connects to Wi-Fi network"
            },
            {
                "id": "osw_012",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open WordPad and format text as bold and italic.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Search 'WordPad'", "Open WordPad", "Type text", "Select text", "Click Bold button", "Click Italic button"],
                "explanation": "Formats text in WordPad"
            },
            {
                "id": "osw_013",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Create a new user account named 'GuestUser'.

Provide step-by-step actions:""",
                "expected": ["Open Settings", "Click Accounts", "Click Family & other users", "Click 'Add someone else to this PC'", "Enter 'GuestUser'", "Follow prompts"],
                "explanation": "Creates new user account"
            },
            {
                "id": "osw_014",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Recycle Bin and empty it.

Provide step-by-step actions:""",
                "expected": ["Double-click Recycle Bin icon", "Click 'Empty Recycle Bin'", "Click Yes to confirm"],
                "explanation": "Empties the Recycle Bin"
            },
            {
                "id": "osw_015",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Control Panel and uninstall a program.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Search 'Control Panel'", "Open Control Panel", "Click 'Programs'", "Click 'Uninstall a program'", "Select program", "Click Uninstall"],
                "explanation": "Uninstalls a program"
            },
            {
                "id": "osw_016",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Snipping Tool and capture a rectangular screenshot.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Search 'Snipping Tool'", "Open Snipping Tool", "Click 'New' dropdown", "Select 'Rectangular Snip'", "Drag to select area"],
                "explanation": "Captures rectangular screenshot"
            },
            {
                "id": "osw_017",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Command Prompt and run 'ipconfig' command.

Provide step-by-step actions:""",
                "expected": ["Click Start", "Search 'cmd'", "Open Command Prompt", "Type 'ipconfig'", "Press Enter"],
                "explanation": "Runs ipconfig in Command Prompt"
            },
            {
                "id": "osw_018",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Date and Time settings and change the time zone.

Provide step-by-step actions:""",
                "expected": ["Right-click time in taskbar", "Select 'Adjust date/time'", "Click 'Time zone' dropdown", "Select new time zone"],
                "explanation": "Changes system time zone"
            },
            {
                "id": "osw_019",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open File Explorer and show hidden files.

Provide step-by-step actions:""",
                "expected": ["Open File Explorer", "Click View tab", "Check 'Hidden items' checkbox"],
                "explanation": "Shows hidden files in File Explorer"
            },
            {
                "id": "osw_020",
                "prompt": """You are a GUI automation agent. Complete this task:

Task: Open the Sound settings and set the volume to 50%.

Provide step-by-step actions:""",
                "expected": ["Click speaker icon in taskbar", "Click 'Open Sound settings'", "Adjust volume slider to 50%"],
                "explanation": "Adjusts system volume"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a GUI agent task response."""
        expected = prompt_data.get("expected", [])
        
        # Extract steps from response
        steps = []
        for line in response.split('\n'):
            line = line.strip()
            match = re.match(r'^(?:\d+[.\)]\s*|[-*]\s*)(.+)$', line)
            if match:
                steps.append(match.group(1))
            elif line and len(line) > 5 and not line.startswith('#'):
                action_words = ['click', 'press', 'type', 'open', 'select', 'navigate', 'wait', 'find', 'drag']
                if any(word in line.lower() for word in action_words):
                    steps.append(line)
        
        if not steps:
            return {
                "success": False,
                "score": 0.0,
                "feedback": "No clear steps found in response",
                "extracted_steps": []
            }
        
        # Score based on step coverage
        score = 0.0
        feedback = []
        
        action_verbs = ['click', 'press', 'type', 'open', 'select', 'navigate', 'wait', 'find', 'drag', 'double-click', 'right-click']
        found_verbs = set()
        for step in steps:
            for verb in action_verbs:
                if verb in step.lower():
                    found_verbs.add(verb)
        
        if found_verbs:
            score += min(len(found_verbs) * 0.1, 0.4)
            feedback.append(f"Uses {len(found_verbs)} action types")
        
        if len(steps) >= 3:
            score += 0.2
            feedback.append("Has sufficient steps")
        
        if len(steps) >= 5:
            score += 0.2
            feedback.append("Detailed step-by-step plan")
        
        if expected:
            expected_text = ' '.join(expected).lower()
            steps_text = ' '.join(steps).lower()
            key_matches = 0
            for exp_step in expected:
                key_words = exp_step.lower().split()[:2]
                if any(word in steps_text for word in key_words):
                    key_matches += 1
            
            if key_matches > 0:
                score += min(key_matches / len(expected) * 0.2, 0.2)
                feedback.append(f"Covers {key_matches} key actions")
        
        return {
            "success": score >= 0.4,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Steps provided",
            "extracted_steps": steps[:10]
        }
    
    def get_system_prompt(self) -> str:
        return "You are a GUI automation agent. Break down the task into clear, step-by-step actions that could be executed by an automation system. List each step on a new line."
