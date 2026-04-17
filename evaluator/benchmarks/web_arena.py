"""WebArena benchmark - Web navigation and app interaction tasks with structured JSON actions."""

from typing import Dict, Any, List, Optional
import re
import json
from .base import Benchmark, BenchmarkConfig


class WebArenaBenchmark(Benchmark):
    """WebArena - Web navigation tasks requiring structured JSON action output."""

    def __init__(self):
        config = BenchmarkConfig(
            name="webarena",
            description="Web navigation and app interaction tasks with JSON action output",
            category="agent",
            version="1.0",
            timeout=60,
            max_tokens=2048,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load web navigation tasks with described UI states."""
        self.prompts = [
            {
                "id": "wa_001",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/login\n"
                    "Page Title: Sign In – Example Shop\n"
                    "Visible elements:\n"
                    "  - Input field: id='email', placeholder='Email address'\n"
                    "  - Input field: id='password', placeholder='Password'\n"
                    "  - Button: id='login-btn', text='Sign In'\n"
                    "  - Link: text='Forgot password?', href='/forgot-password'\n\n"
                    "Task: Log in with email 'user@example.com' and password 'SecurePass123'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "email",
                "expected_value": "user@example.com",
            },
            {
                "id": "wa_002",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/products\n"
                    "Page Title: Products – Example Shop\n"
                    "Visible elements:\n"
                    "  - Input field: id='search-bar', placeholder='Search products...'\n"
                    "  - Button: id='search-btn', text='Search'\n"
                    "  - Grid of product cards (20 items)\n"
                    "  - Dropdown: id='sort-by', options=['Relevance','Price Low–High','Price High–Low','Rating']\n\n"
                    "Task: Search for 'wireless headphones'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "search-bar",
                "expected_value": "wireless headphones",
            },
            {
                "id": "wa_003",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/products?q=wireless+headphones\n"
                    "Page Title: Search Results – Example Shop\n"
                    "Visible elements:\n"
                    "  - Input field: id='search-bar', value='wireless headphones'\n"
                    "  - Dropdown: id='sort-by', current='Relevance'\n"
                    "  - Product: id='prod-1041', name='SoundWave Pro X1', price='$89.99', rating='4.5'\n"
                    "  - Product: id='prod-2033', name='AudioMax BT700', price='$64.99', rating='4.3'\n"
                    "  - Product: id='prod-3019', name='ClearSound Elite', price='$112.00', rating='4.7'\n\n"
                    "Task: Sort results by highest rating first.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "sort-by",
                "expected_value": "Rating",
            },
            {
                "id": "wa_004",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/product/3019\n"
                    "Page Title: ClearSound Elite Headphones – Example Shop\n"
                    "Visible elements:\n"
                    "  - Heading: 'ClearSound Elite Headphones'\n"
                    "  - Text: 'Price: $112.00'\n"
                    "  - Dropdown: id='quantity', options=['1','2','3','4','5'], current='1'\n"
                    "  - Button: id='add-to-cart', text='Add to Cart'\n"
                    "  - Button: id='wishlist-btn', text='Save to Wishlist'\n"
                    "  - Text: 'In Stock: 7 remaining'\n\n"
                    "Task: Add 2 units of this product to the cart.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "quantity",
                "expected_value": "2",
            },
            {
                "id": "wa_005",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/cart\n"
                    "Page Title: Your Cart – Example Shop\n"
                    "Visible elements:\n"
                    "  - Cart item: 'ClearSound Elite Headphones', qty 2, $224.00\n"
                    "  - Input field: id='promo-code', placeholder='Enter promo code'\n"
                    "  - Button: id='apply-promo', text='Apply'\n"
                    "  - Text: 'Subtotal: $224.00'\n"
                    "  - Button: id='checkout-btn', text='Proceed to Checkout'\n\n"
                    "Task: Apply the promo code 'SAVE10'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "promo-code",
                "expected_value": "SAVE10",
            },
            {
                "id": "wa_006",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://mail.example.com/inbox\n"
                    "Page Title: Inbox – Example Mail\n"
                    "Visible elements:\n"
                    "  - Button: id='compose-btn', text='Compose'\n"
                    "  - Email list (10 messages)\n"
                    "  - Input field: id='search-mail', placeholder='Search mail'\n"
                    "  - Sidebar links: Inbox, Sent, Drafts, Trash\n\n"
                    "Task: Start composing a new email.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "compose-btn",
                "expected_value": "",
            },
            {
                "id": "wa_007",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://mail.example.com/compose\n"
                    "Page Title: New Message – Example Mail\n"
                    "Visible elements:\n"
                    "  - Input field: id='to-field', placeholder='To'\n"
                    "  - Input field: id='subject-field', placeholder='Subject'\n"
                    "  - Text area: id='body-field', placeholder='Compose email'\n"
                    "  - Button: id='send-btn', text='Send'\n"
                    "  - Button: id='attach-btn', text='Attach file'\n\n"
                    "Task: Address the email to 'manager@company.com'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "to-field",
                "expected_value": "manager@company.com",
            },
            {
                "id": "wa_008",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://docs.example.com/editor/doc-8821\n"
                    "Page Title: Q2 Report – Example Docs\n"
                    "Visible elements:\n"
                    "  - Document editor with text content\n"
                    "  - Toolbar: Bold (id='btn-bold'), Italic (id='btn-italic'), "
                    "Underline (id='btn-underline'), Insert Table (id='btn-table')\n"
                    "  - Button: id='share-btn', text='Share'\n"
                    "  - Button: id='download-btn', text='Download'\n"
                    "  - Dropdown: id='download-format', options=['PDF','DOCX','TXT']\n\n"
                    "Task: Download the document as a PDF.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "download-format",
                "expected_value": "PDF",
            },
            {
                "id": "wa_009",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://admin.example.com/users\n"
                    "Page Title: User Management – Admin Panel\n"
                    "Visible elements:\n"
                    "  - Table of users (id='users-table'), 15 rows\n"
                    "  - Input field: id='user-search', placeholder='Search by name or email'\n"
                    "  - Button: id='add-user-btn', text='Add New User'\n"
                    "  - Button: id='export-btn', text='Export CSV'\n"
                    "  - Pagination: showing 1–15 of 87 users\n\n"
                    "Task: Search for user 'diana.prince@example.com'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "user-search",
                "expected_value": "diana.prince@example.com",
            },
            {
                "id": "wa_010",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://app.example.com/settings/profile\n"
                    "Page Title: Profile Settings – Example App\n"
                    "Visible elements:\n"
                    "  - Input field: id='display-name', value='JohnD'\n"
                    "  - Input field: id='email-display', value='john@example.com' (read-only)\n"
                    "  - Input field: id='phone', value=''\n"
                    "  - Textarea: id='bio', placeholder='Write a short bio'\n"
                    "  - Button: id='save-profile', text='Save Changes'\n"
                    "  - Button: id='change-password', text='Change Password'\n\n"
                    "Task: Update the display name to 'John Doe'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "display-name",
                "expected_value": "John Doe",
            },
            {
                "id": "wa_011",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://bank.example.com/transfer\n"
                    "Page Title: Transfer Funds – Example Bank\n"
                    "Visible elements:\n"
                    "  - Dropdown: id='from-account', options=['Checking ****4421 ($3,200)','Savings ****8832 ($15,400)']\n"
                    "  - Input field: id='to-account', placeholder='Recipient account number'\n"
                    "  - Input field: id='amount', placeholder='Amount'\n"
                    "  - Input field: id='memo', placeholder='Memo (optional)'\n"
                    "  - Button: id='transfer-submit', text='Transfer Now'\n\n"
                    "Task: Enter the transfer amount of $500.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "amount",
                "expected_value": "500",
            },
            {
                "id": "wa_012",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://calendar.example.com/new-event\n"
                    "Page Title: New Event – Example Calendar\n"
                    "Visible elements:\n"
                    "  - Input field: id='event-title', placeholder='Event title'\n"
                    "  - Input field: id='event-date', placeholder='Date (YYYY-MM-DD)'\n"
                    "  - Input field: id='event-time', placeholder='Start time'\n"
                    "  - Input field: id='event-location', placeholder='Location'\n"
                    "  - Textarea: id='event-description', placeholder='Description'\n"
                    "  - Button: id='save-event', text='Save Event'\n\n"
                    "Task: Set the event title to 'Team Standup'.\n"
                    "What is the next action?"
                ),
                "expected_action": "type",
                "expected_target": "event-title",
                "expected_value": "Team Standup",
            },
            {
                "id": "wa_013",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/account/orders\n"
                    "Page Title: Order History – Example Shop\n"
                    "Visible elements:\n"
                    "  - Order #55821: Placed Jan 10, $224.00, Status: Delivered – "
                    "Button id='view-order-55821' text='View Details'\n"
                    "  - Order #55790: Placed Dec 28, $45.99, Status: Delivered – "
                    "Button id='view-order-55790' text='View Details'\n"
                    "  - Order #55652: Placed Dec 1, $189.00, Status: Delivered – "
                    "Button id='view-order-55652' text='View Details'\n"
                    "  - Button: id='start-return-btn', text='Start a Return'\n\n"
                    "Task: View the details of order #55821.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "view-order-55821",
                "expected_value": "",
            },
            {
                "id": "wa_014",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://project.example.com/board\n"
                    "Page Title: Sprint Board – Example Project\n"
                    "Visible elements:\n"
                    "  - Column: 'To Do' (5 cards)\n"
                    "  - Column: 'In Progress' (3 cards)\n"
                    "  - Column: 'Done' (8 cards)\n"
                    "  - Button: id='add-task-btn', text='+ Add Task'\n"
                    "  - Input field: id='board-search', placeholder='Search tasks'\n"
                    "  - Dropdown: id='assignee-filter', options=['All','Alice','Bob','Carol']\n\n"
                    "Task: Filter tasks to show only tasks assigned to Alice.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "assignee-filter",
                "expected_value": "Alice",
            },
            {
                "id": "wa_015",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://cms.example.com/posts/new\n"
                    "Page Title: New Post – Example CMS\n"
                    "Visible elements:\n"
                    "  - Input field: id='post-title', placeholder='Post title'\n"
                    "  - Rich text editor: id='post-body'\n"
                    "  - Input field: id='post-tags', placeholder='Tags (comma separated)'\n"
                    "  - Dropdown: id='post-status', options=['Draft','Published','Scheduled']\n"
                    "  - Button: id='publish-btn', text='Publish'\n"
                    "  - Button: id='save-draft-btn', text='Save Draft'\n\n"
                    "Task: Save the current post as a draft without publishing.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "save-draft-btn",
                "expected_value": "",
            },
            {
                "id": "wa_016",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://analytics.example.com/dashboard\n"
                    "Page Title: Analytics Dashboard – Example Analytics\n"
                    "Visible elements:\n"
                    "  - Date range picker: id='date-range', current='Last 7 days'\n"
                    "  - Metric cards: Users (1,240), Sessions (3,882), Bounce Rate (42.1%), Avg Duration (2:34)\n"
                    "  - Button: id='export-report', text='Export Report'\n"
                    "  - Dropdown: id='export-format', options=['CSV','PDF','XLSX']\n"
                    "  - Link: id='view-full-report', text='View Full Report'\n\n"
                    "Task: Navigate to the full analytics report.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "view-full-report",
                "expected_value": "",
            },
            {
                "id": "wa_017",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://app.example.com/notifications\n"
                    "Page Title: Notifications – Example App\n"
                    "Visible elements:\n"
                    "  - Toggle: id='email-notif', label='Email notifications', state='ON'\n"
                    "  - Toggle: id='sms-notif', label='SMS notifications', state='OFF'\n"
                    "  - Toggle: id='push-notif', label='Push notifications', state='ON'\n"
                    "  - Toggle: id='weekly-digest', label='Weekly digest email', state='OFF'\n"
                    "  - Button: id='save-notif', text='Save Notification Preferences'\n\n"
                    "Task: Enable SMS notifications.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "sms-notif",
                "expected_value": "",
            },
            {
                "id": "wa_018",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://forms.example.com/survey/q4-feedback\n"
                    "Page Title: Q4 Customer Feedback Survey\n"
                    "Visible elements:\n"
                    "  - Question 1: 'How satisfied are you with our service?'\n"
                    "    Radio buttons: id='rating-1' (1-star), id='rating-2' (2-star), id='rating-3' (3-star), "
                    "id='rating-4' (4-star), id='rating-5' (5-star)\n"
                    "  - Question 2: Textarea id='feedback-text', placeholder='Additional comments'\n"
                    "  - Button: id='submit-survey', text='Submit'\n"
                    "  - Button: id='next-page', text='Next' (grayed out until Q1 answered)\n\n"
                    "Task: Select a 5-star rating for Question 1.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "rating-5",
                "expected_value": "",
            },
            {
                "id": "wa_019",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://app.example.com/dashboard\n"
                    "Page Title: Dashboard – Example App\n"
                    "Visible elements:\n"
                    "  - Navigation: Home, Projects, Reports, Settings, Help\n"
                    "  - Summary cards: Active Projects (8), Pending Tasks (23), Team Members (5)\n"
                    "  - Recent activity feed (10 items)\n"
                    "  - Button: id='quick-add-task', text='+ Quick Add Task'\n\n"
                    "Task: Navigate to the Reports section.\n"
                    "What is the next action?"
                ),
                "expected_action": "navigate",
                "expected_target": "Reports",
                "expected_value": "",
            },
            {
                "id": "wa_020",
                "prompt": (
                    "Current browser state:\n"
                    "URL: https://shop.example.com/checkout/shipping\n"
                    "Page Title: Shipping Information – Checkout\n"
                    "Visible elements:\n"
                    "  - Input field: id='ship-name', placeholder='Full name'\n"
                    "  - Input field: id='ship-address', placeholder='Street address'\n"
                    "  - Input field: id='ship-city', placeholder='City'\n"
                    "  - Input field: id='ship-zip', placeholder='ZIP code'\n"
                    "  - Dropdown: id='ship-state', placeholder='State'\n"
                    "  - Dropdown: id='ship-method', options=['Standard (5–7 days, Free)','Express (2 days, $12.99)','Overnight (1 day, $24.99)']\n"
                    "  - Button: id='continue-payment', text='Continue to Payment'\n\n"
                    "Task: Select Express shipping.\n"
                    "What is the next action?"
                ),
                "expected_action": "click",
                "expected_target": "ship-method",
                "expected_value": "Express",
            },
        ]

    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Attempt to parse a JSON action dict from the model response.
        Tries the full response first, then looks for embedded JSON blocks.
        """
        # Direct parse
        try:
            return json.loads(response.strip())
        except (json.JSONDecodeError, ValueError):
            pass

        # JSON code block
        block_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", response, re.DOTALL)
        if block_match:
            try:
                return json.loads(block_match.group(1))
            except (json.JSONDecodeError, ValueError):
                pass

        # Any {...} in response
        brace_match = re.search(r"\{[^{}]*\"action\"[^{}]*\}", response, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except (json.JSONDecodeError, ValueError):
                pass

        return None

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Evaluate a WebArena response.

        Scoring:
          1.0 - action type AND target both match expected
          0.5 - action type matches but target does not
          0.0 - action type does not match or no valid JSON found
        """
        expected_action: str = prompt_data.get("expected_action", "").lower()
        expected_target: str = prompt_data.get("expected_target", "").lower()

        parsed = self._extract_json_from_response(response)

        if parsed is None:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {
                    "reason": "no_valid_json",
                    "expected_action": expected_action,
                    "expected_target": expected_target,
                },
            }

        got_action = str(parsed.get("action", "")).lower().strip()
        got_target = str(parsed.get("target", "")).lower().strip()

        action_correct = got_action == expected_action
        # Target match: exact or substring (handles partial IDs / display text)
        target_correct = (
            got_target == expected_target
            or expected_target in got_target
            or got_target in expected_target
        )

        if action_correct and target_correct:
            score = 1.0
            success = True
            match_type = "full_match"
        elif action_correct:
            score = 0.5
            success = False
            match_type = "action_only"
        else:
            score = 0.0
            success = False
            match_type = "no_match"

        return {
            "success": success,
            "score": score,
            "metadata": {
                "match_type": match_type,
                "expected_action": expected_action,
                "expected_target": expected_target,
                "got_action": got_action,
                "got_target": got_target,
                "parsed_json": parsed,
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are a web agent. Given the current browser state, output the next action as JSON "
            "with keys: action, target, value. "
            'Valid actions: "click", "type", "navigate", "submit". '
            '"target" is the element id or link text. '
            '"value" is the text to type (empty string if not applicable). '
            "Output only the JSON object, no explanation."
        )
