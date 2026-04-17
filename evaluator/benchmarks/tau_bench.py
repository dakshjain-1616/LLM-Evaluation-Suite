"""TauBench benchmark - Tool-augmented reasoning tasks with simulated tool outputs."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class TauBenchBenchmark(Benchmark):
    """TauBench - Tool-augmented reasoning and action synthesis."""

    def __init__(self):
        config = BenchmarkConfig(
            name="tau_bench",
            description="Tool-augmented reasoning with simulated tool call results",
            category="agent",
            version="1.0",
            timeout=90,
            max_tokens=2048,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load tool-augmented reasoning prompts with inline simulated tool results."""
        self.prompts = [
            {
                "id": "tau_001",
                "prompt": (
                    "You called search('best hotels Paris budget under $200') and received these results:\n"
                    "1. Hotel Lumiere – 4.6 stars, $145/night, 0.8 km from Eiffel Tower, free breakfast\n"
                    "2. Grand Marais Inn – 4.2 stars, $189/night, 2.1 km from Louvre, parking available\n"
                    "3. Bastille Budget Lodge – 3.8 stars, $98/night, near Bastille metro, no amenities\n"
                    "4. Paris Stay Classic – 4.4 stars, $210/night, central location (over budget)\n"
                    "5. Le Petit Montmartre – 4.1 stars, $175/night, 1.5 km from Sacre-Coeur\n\n"
                    "Which hotel best fits the constraint of budget under $200 with rating above 4 stars? "
                    "State the hotel name and the booking action you would take next."
                ),
                "expected_interpretation": "Hotel Lumiere",
                "expected_action": "book Hotel Lumiere",
                "key_interpretation_terms": ["hotel lumiere", "lumiere"],
                "key_action_terms": ["book", "reserve", "select", "lumiere"],
            },
            {
                "id": "tau_002",
                "prompt": (
                    "You called get_weather('Seattle', days=5) and received:\n"
                    "Day 1 (Mon): 52°F, heavy rain, wind 18 mph\n"
                    "Day 2 (Tue): 49°F, overcast, light drizzle\n"
                    "Day 3 (Wed): 55°F, partly cloudy, no rain\n"
                    "Day 4 (Thu): 58°F, sunny intervals, mild breeze\n"
                    "Day 5 (Fri): 61°F, mostly sunny\n\n"
                    "You also called get_event('Seattle Marathon') and received: Date = Thursday, Start 7:00 AM.\n\n"
                    "Based on the weather forecast, is Thursday a good day for the outdoor marathon? "
                    "What would you advise the event organizer, and what action should you take next?"
                ),
                "expected_interpretation": "Thursday is good, sunny intervals",
                "expected_action": "confirm event or notify organizer Thursday is suitable",
                "key_interpretation_terms": ["thursday", "sunny", "good", "suitable", "favorable"],
                "key_action_terms": ["confirm", "notify", "proceed", "advise", "suitable"],
            },
            {
                "id": "tau_003",
                "prompt": (
                    "You called query_database('SELECT product_id, name, stock, reorder_level FROM inventory') "
                    "and received:\n"
                    "| product_id | name            | stock | reorder_level |\n"
                    "| P001       | Laptop Stand    | 12    | 20            |\n"
                    "| P002       | USB Hub         | 45    | 15            |\n"
                    "| P003       | Webcam Pro      | 8     | 25            |\n"
                    "| P004       | Keyboard Deluxe | 3     | 10            |\n"
                    "| P005       | Mouse Ergonomic | 31    | 20            |\n\n"
                    "Which products are below their reorder level? What reorder action should you take "
                    "for the most critically low item?"
                ),
                "expected_interpretation": "Laptop Stand, Webcam Pro, Keyboard Deluxe are below reorder level",
                "expected_action": "reorder Keyboard Deluxe first (most critical)",
                "key_interpretation_terms": ["keyboard deluxe", "webcam", "laptop stand", "below"],
                "key_action_terms": ["reorder", "order", "keyboard deluxe", "p004"],
            },
            {
                "id": "tau_004",
                "prompt": (
                    "You called flight_search(origin='BOS', dest='MIA', date='2024-05-10') and received:\n"
                    "Flight AA302: Depart 06:00, Arrive 09:45, 1 stop (PHL), $187, seats available\n"
                    "Flight DL890: Depart 08:30, Arrive 12:10, nonstop, $245, seats available\n"
                    "Flight UA441: Depart 14:00, Arrive 17:55, 1 stop (EWR), $162, last 2 seats\n"
                    "Flight B6334: Depart 17:30, Arrive 21:05, nonstop, $198, seats available\n\n"
                    "The traveler's requirements: arrive before 2 PM, prefers nonstop, budget max $250.\n\n"
                    "Which flight best meets all requirements? State the flight and the next action."
                ),
                "expected_interpretation": "DL890 (nonstop, arrives 12:10, within budget)",
                "expected_action": "book DL890",
                "key_interpretation_terms": ["dl890", "nonstop", "12:10", "8:30"],
                "key_action_terms": ["book", "select", "dl890", "reserve"],
            },
            {
                "id": "tau_005",
                "prompt": (
                    "You called code_executor(code='import pandas as pd; df = pd.read_csv(\"sales.csv\"); "
                    "print(df.describe())') and received:\n"
                    "         revenue    units_sold  customer_age\n"
                    "count   1200.000     1200.000    1200.000\n"
                    "mean    4325.670      142.330      34.820\n"
                    "std     1890.120       63.450      11.230\n"
                    "min      420.000       12.000      18.000\n"
                    "25%     2980.000       95.000      26.000\n"
                    "50%     4100.000      138.000      34.000\n"
                    "75%     5600.000      185.000      43.000\n"
                    "max    12400.000      398.000      67.000\n\n"
                    "Based on these statistics, what is the average revenue per unit sold? "
                    "What analysis step should you take next to understand the revenue distribution?"
                ),
                "expected_interpretation": "30.39 per unit (4325.67 / 142.33)",
                "expected_action": "plot histogram or analyze revenue distribution",
                "key_interpretation_terms": ["30", "revenue", "per unit", "average"],
                "key_action_terms": ["histogram", "distribution", "visualize", "plot", "analyze", "segment"],
            },
            {
                "id": "tau_006",
                "prompt": (
                    "You called calendar_check(user='alice@company.com', date='2024-05-15') and received:\n"
                    "09:00–10:00: Team standup (recurring)\n"
                    "11:00–12:30: Client presentation – TechCorp (high priority)\n"
                    "14:00–15:00: 1:1 with manager\n"
                    "16:00–16:30: Budget review call\n\n"
                    "You also called meeting_request(requester='bob@company.com', duration=60, "
                    "preferred_date='2024-05-15') and received: 'Please find a 60-minute slot.'\n\n"
                    "What is the best available 60-minute slot for Bob's meeting on May 15? "
                    "What scheduling action should you take?"
                ),
                "expected_interpretation": "12:30–13:30 or 15:00–16:00",
                "expected_action": "schedule meeting at 12:30 or 15:00",
                "key_interpretation_terms": ["12:30", "15:00", "available", "slot"],
                "key_action_terms": ["schedule", "book", "create", "invite", "12:30", "15:00"],
            },
            {
                "id": "tau_007",
                "prompt": (
                    "You called web_search('Python vs JavaScript for backend 2024') and received:\n"
                    "Result 1 (StackOverflow Survey 2024): Python used by 51% of backend devs; "
                    "JS/Node by 40%. Python top for data/ML.\n"
                    "Result 2 (Tiobe Index Apr 2024): Python #1 language globally; JavaScript #6.\n"
                    "Result 3 (Job listings analysis): Python backend roles up 23% YoY; "
                    "Node.js roles up 11% YoY.\n"
                    "Result 4 (Performance benchmark): Node.js 2.3x faster than Python (Django) for "
                    "high-concurrency HTTP requests.\n\n"
                    "The user is building a real-time chat application. Based on the tool results, "
                    "which language do you recommend and why? What should you do next to validate the recommendation?"
                ),
                "expected_interpretation": "JavaScript/Node.js for real-time chat due to performance",
                "expected_action": "recommend Node.js or research real-time frameworks",
                "key_interpretation_terms": ["node", "javascript", "real-time", "concurrent", "performance", "faster"],
                "key_action_terms": ["recommend", "node", "javascript", "websocket", "validate", "research"],
            },
            {
                "id": "tau_008",
                "prompt": (
                    "You called run_tests(suite='regression') and received:\n"
                    "Test Results Summary:\n"
                    "  PASSED: 142 tests\n"
                    "  FAILED: 3 tests\n"
                    "  SKIPPED: 5 tests\n"
                    "Failed tests:\n"
                    "  test_user_auth_token_expiry – AssertionError: expected 401, got 200\n"
                    "  test_payment_refund_partial – TypeError: 'NoneType' has no attribute 'amount'\n"
                    "  test_email_template_render – TemplateNotFound: 'welcome_v2.html'\n\n"
                    "Which failed test is the highest priority to fix and why? "
                    "What debugging action should you take for that test?"
                ),
                "expected_interpretation": "auth token test is highest priority (security issue)",
                "expected_action": "debug test_user_auth_token_expiry or check auth middleware",
                "key_interpretation_terms": ["auth", "401", "security", "token", "expiry", "priority"],
                "key_action_terms": ["debug", "fix", "auth", "token", "middleware", "check", "investigate"],
            },
            {
                "id": "tau_009",
                "prompt": (
                    "You called price_lookup(items=['ITEM-A', 'ITEM-B', 'ITEM-C']) and received:\n"
                    "ITEM-A: List price $150.00, member discount 10%, stock: YES\n"
                    "ITEM-B: List price $89.99, member discount 15%, stock: NO (backorder 2 weeks)\n"
                    "ITEM-C: List price $220.00, member discount 20%, stock: YES\n\n"
                    "You also called get_user_profile(user_id='U-8821') and received: "
                    "{'status': 'gold_member', 'cart_total_today': 280.00, 'free_shipping_threshold': 300.00}\n\n"
                    "The user wants all three items. What is the total cost after discounts? "
                    "Are they eligible for free shipping? What action should you take regarding the out-of-stock item?"
                ),
                "expected_interpretation": "total after discounts: $357.49, not eligible yet (need $42.51 more... but wait: 135+76.49+176=387.49 > 300 so eligible)",
                "expected_action": "notify about ITEM-B backorder and confirm order",
                "key_interpretation_terms": ["backorder", "item-b", "out of stock", "discount", "free shipping"],
                "key_action_terms": ["notify", "confirm", "backorder", "inform", "alert", "item-b"],
            },
            {
                "id": "tau_010",
                "prompt": (
                    "You called translate_text(text='Bonjour, comment puis-je vous aider?', "
                    "source='fr', target='en') and received: 'Hello, how can I help you?'\n\n"
                    "You then called sentiment_analysis(text='Hello, how can I help you?') and received: "
                    "{'sentiment': 'positive', 'confidence': 0.94, 'tone': 'professional_friendly'}\n\n"
                    "You also called language_detect(text='Guten Tag, ich brauche Hilfe.') and received: "
                    "{'language': 'de', 'confidence': 0.99}\n\n"
                    "A customer support bot received the German message. Based on these tool results, "
                    "what should the bot do next, and what is the correct action to take?"
                ),
                "expected_interpretation": "detect German, translate it, respond in German",
                "expected_action": "translate German message and respond in German",
                "key_interpretation_terms": ["german", "translate", "de", "guten tag"],
                "key_action_terms": ["translate", "german", "respond", "reply", "de"],
            },
            {
                "id": "tau_011",
                "prompt": (
                    "You called map_route(start='Chicago, IL', end='Nashville, TN', mode='driving') and received:\n"
                    "Route 1: I-65 S – 476 miles, 6 hr 55 min, tolls: $4.50\n"
                    "Route 2: I-57 S to I-24 W – 511 miles, 7 hr 30 min, tolls: $0\n"
                    "Route 3: US-41 S – 460 miles, 8 hr 15 min, tolls: $0, scenic route\n\n"
                    "You called gas_price(region='midwest') and received: $3.45/gallon average.\n"
                    "The vehicle gets 28 MPG. The driver values time over cost and has a meeting at 6 PM, "
                    "departing at 8 AM.\n\n"
                    "Which route should the driver take, and what time will they arrive?"
                ),
                "expected_interpretation": "Route 1 (I-65), arrives ~3:00 PM",
                "expected_action": "select Route 1, depart 8 AM, arrive ~2:55 PM",
                "key_interpretation_terms": ["route 1", "i-65", "fastest", "6 hr", "arrive"],
                "key_action_terms": ["route 1", "i-65", "select", "recommend", "2:55", "3:00"],
            },
            {
                "id": "tau_012",
                "prompt": (
                    "You called read_email(inbox='support@store.com', filter='unread') and received 3 emails:\n"
                    "Email 1 – From: angry_customer@gmail.com – Subject: 'WHERE IS MY ORDER #55821' – "
                    "Received: 3 days ago – Priority: HIGH\n"
                    "Email 2 – From: vendor@supplies.com – Subject: 'Invoice #INV-2024-991' – "
                    "Received: 1 day ago – Priority: MEDIUM\n"
                    "Email 3 – From: newsletter@partner.com – Subject: 'Weekly digest' – "
                    "Received: 2 hours ago – Priority: LOW\n\n"
                    "You called order_lookup(order_id='55821') and received: "
                    "Status: 'Shipped', Carrier: FedEx, Tracking: 7489234891, ETA: tomorrow.\n\n"
                    "Which email should you respond to first and what is the correct response action?"
                ),
                "expected_interpretation": "respond to Email 1 first (angry customer, 3 days old, order shipped)",
                "expected_action": "send tracking info to angry_customer@gmail.com",
                "key_interpretation_terms": ["email 1", "angry customer", "order 55821", "shipped", "tracking"],
                "key_action_terms": ["reply", "respond", "tracking", "fedex", "7489234891", "email 1"],
            },
            {
                "id": "tau_013",
                "prompt": (
                    "You called financial_data(ticker='AAPL', period='1y') and received:\n"
                    "Current Price: $189.30\n"
                    "52-week High: $199.62  |  52-week Low: $164.08\n"
                    "P/E Ratio: 31.2  |  EPS: $6.07  |  Dividend Yield: 0.52%\n"
                    "Revenue Growth YoY: +2.1%  |  Net Margin: 26.4%\n"
                    "Analyst Consensus: 28 Buy, 8 Hold, 2 Sell\n\n"
                    "You called compare_sector(ticker='AAPL', metric='PE') and received: "
                    "Sector avg P/E: 27.4, AAPL P/E: 31.2 (14% premium).\n\n"
                    "Based on these results, summarize the investment thesis and state the next analytical action."
                ),
                "expected_interpretation": "AAPL at slight premium to sector, strong margins, mostly buy ratings",
                "expected_action": "analyze DCF or compare to peers like MSFT",
                "key_interpretation_terms": ["premium", "p/e", "buy", "margin", "31.2", "analyst"],
                "key_action_terms": ["dcf", "peer", "compare", "msft", "valuation", "analyze", "further"],
            },
            {
                "id": "tau_014",
                "prompt": (
                    "You called ocr_scan(document='contract_signed.pdf') and received the following extracted text:\n"
                    "'This Agreement is entered into on March 1, 2024 between Nexus Corp ('Company') "
                    "and James Whitfield ('Contractor'). Term: 6 months. Rate: $125/hour. "
                    "Max hours per week: 40. Non-compete clause: 12 months post-termination. "
                    "IP ownership: all work product belongs to Company.'\n\n"
                    "You called calendar_add(event='Contract end date') and received: "
                    "'Event added: September 1, 2024.'\n\n"
                    "Based on the contract terms, what is the maximum total value of this contract? "
                    "What compliance action should you flag for the contractor?"
                ),
                "expected_interpretation": "max value $1,300,000 (125 * 40 * 26 weeks)",
                "expected_action": "flag 12-month non-compete restriction post September 2024",
                "key_interpretation_terms": ["1,300,000", "1300000", "non-compete", "maximum", "total"],
                "key_action_terms": ["non-compete", "flag", "alert", "compliance", "12 month", "september"],
            },
            {
                "id": "tau_015",
                "prompt": (
                    "You called support_ticket_list(status='open', assigned_to='unassigned') and received:\n"
                    "Ticket T-1021: 'Login page throws 500 error for all users' – Severity: CRITICAL – Age: 2h\n"
                    "Ticket T-1019: 'PDF export button missing in settings' – Severity: LOW – Age: 5 days\n"
                    "Ticket T-1022: 'Payment declined for Visa cards' – Severity: HIGH – Age: 4h\n"
                    "Ticket T-1018: 'Dark mode flicker on Safari' – Severity: MEDIUM – Age: 1 week\n\n"
                    "You called get_on_call_engineer() and received: {'name': 'Priya Mehta', 'email': 'priya@co.com'}\n\n"
                    "Which ticket should be escalated immediately and to whom? What is the escalation action?"
                ),
                "expected_interpretation": "T-1021 is critical (login broken for all users)",
                "expected_action": "assign T-1021 to Priya Mehta immediately",
                "key_interpretation_terms": ["t-1021", "critical", "login", "500", "all users"],
                "key_action_terms": ["assign", "escalate", "t-1021", "priya", "mehta", "immediately"],
            },
            {
                "id": "tau_016",
                "prompt": (
                    "You called recipe_search(query='vegan dinner', max_time=30, servings=4) and received:\n"
                    "Recipe 1: Chickpea Curry – 25 min, rating 4.7, ingredients: chickpeas, tomatoes, "
                    "coconut milk, spices\n"
                    "Recipe 2: Pasta Primavera – 20 min, rating 4.5, ingredients: pasta, bell peppers, "
                    "zucchini, olive oil\n"
                    "Recipe 3: Lentil Soup – 35 min (over limit), rating 4.9\n"
                    "Recipe 4: Buddha Bowl – 30 min, rating 4.6, ingredients: quinoa, roasted veggies, tahini\n\n"
                    "You called pantry_check(user_id='U-4421') and received: "
                    "Available: pasta, bell peppers, zucchini, olive oil, garlic, onions.\n\n"
                    "Which recipe can be made with pantry items already available? What action should you take?"
                ),
                "expected_interpretation": "Pasta Primavera uses available pantry items",
                "expected_action": "select Pasta Primavera and display the recipe",
                "key_interpretation_terms": ["pasta primavera", "pasta", "pantry", "available", "ingredients"],
                "key_action_terms": ["select", "pasta primavera", "display", "show recipe", "recommend"],
            },
            {
                "id": "tau_017",
                "prompt": (
                    "You called system_metrics(server='prod-web-01', window='1h') and received:\n"
                    "CPU Usage: 94% (threshold: 80%) – ALERT\n"
                    "Memory Usage: 71% (threshold: 85%) – OK\n"
                    "Disk I/O: 340 MB/s (threshold: 200 MB/s) – ALERT\n"
                    "Network Out: 890 Mbps (threshold: 1000 Mbps) – OK\n"
                    "Error Rate: 0.3% (threshold: 1%) – OK\n\n"
                    "You called process_list(server='prod-web-01', sort='cpu') and received: "
                    "Top process: 'image_processor.py' using 67% CPU, PID 44821.\n\n"
                    "What is causing the performance issue and what remediation action should you take?"
                ),
                "expected_interpretation": "image_processor.py causing high CPU and Disk I/O",
                "expected_action": "kill or throttle PID 44821, or scale horizontally",
                "key_interpretation_terms": ["image_processor", "cpu", "67%", "pid 44821", "disk"],
                "key_action_terms": ["kill", "restart", "throttle", "scale", "44821", "image_processor"],
            },
            {
                "id": "tau_018",
                "prompt": (
                    "You called social_media_metrics(account='@brandco', period='7d') and received:\n"
                    "Platform: Twitter/X – Followers: 12,400 (+2.1%), Engagement Rate: 1.8%\n"
                    "Platform: Instagram – Followers: 34,800 (+5.3%), Engagement Rate: 4.2%\n"
                    "Platform: LinkedIn – Followers: 8,200 (+0.8%), Engagement Rate: 2.9%\n"
                    "Top performing post this week: Instagram carousel on product launch – 1,240 likes, 87 shares\n\n"
                    "You called ad_budget_check(account='brandco') and received: "
                    "{'remaining_budget': '$2,400', 'top_ROI_platform': 'Instagram'}\n\n"
                    "Based on these results, where should the remaining ad budget be allocated? "
                    "What is the recommended next action?"
                ),
                "expected_interpretation": "Instagram has highest growth and ROI",
                "expected_action": "allocate budget to Instagram",
                "key_interpretation_terms": ["instagram", "5.3%", "4.2%", "roi", "highest"],
                "key_action_terms": ["allocate", "instagram", "budget", "invest", "spend"],
            },
            {
                "id": "tau_019",
                "prompt": (
                    "You called document_search(query='refund policy', corpus='company_handbook') and received:\n"
                    "Match 1 (Section 4.2, p. 18): 'Customers may request a full refund within 30 days of purchase. "
                    "After 30 days, store credit only. Digital downloads are non-refundable.'\n"
                    "Match 2 (Section 4.5, p. 20): 'Defective items may be returned for exchange or refund "
                    "regardless of purchase date, with proof of defect.'\n\n"
                    "A customer purchased a physical item 45 days ago and says it is defective. "
                    "Based on the policy results, what is the customer entitled to? What action should you take?"
                ),
                "expected_interpretation": "customer can get refund or exchange due to defect (Section 4.5)",
                "expected_action": "process refund or exchange for defective item",
                "key_interpretation_terms": ["defective", "4.5", "exchange", "refund", "regardless", "proof"],
                "key_action_terms": ["refund", "exchange", "process", "defective", "eligible"],
            },
            {
                "id": "tau_020",
                "prompt": (
                    "You called geo_lookup(address='1600 Pennsylvania Ave NW, Washington DC') and received:\n"
                    "{'lat': 38.8977, 'lng': -77.0365, 'place_type': 'landmark', 'name': 'White House'}\n\n"
                    "You called nearby_search(lat=38.8977, lng=-77.0365, radius_km=1, category='restaurant') "
                    "and received:\n"
                    "1. Old Ebbitt Grill – 0.4 km, rating 4.5, cuisine: American, open now\n"
                    "2. Founding Farmers DC – 0.7 km, rating 4.6, cuisine: Farm-to-table, open now\n"
                    "3. Joe's Seafood – 0.9 km, rating 4.4, cuisine: Seafood, closes in 30 min\n\n"
                    "A tourist at the White House wants to walk to dinner. They prefer high-rated food and "
                    "have ample time. Which restaurant do you recommend and what is the action?"
                ),
                "expected_interpretation": "Founding Farmers DC (highest rating 4.6, open, 0.7 km walkable)",
                "expected_action": "navigate to Founding Farmers DC",
                "key_interpretation_terms": ["founding farmers", "4.6", "highest", "walkable", "open"],
                "key_action_terms": ["navigate", "directions", "founding farmers", "recommend", "walk"],
            },
        ]

    def _check_terms(self, response: str, terms: List[str]) -> int:
        """Count how many terms appear in the response (case-insensitive)."""
        response_lower = response.lower()
        return sum(1 for term in terms if term.lower() in response_lower)

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Evaluate a TauBench response.

        Scoring:
          0.5 for correct interpretation of tool results (key_interpretation_terms matched)
          0.5 for correct action synthesis (key_action_terms matched)
          Total possible: 1.0
        """
        interp_terms: List[str] = prompt_data.get("key_interpretation_terms", [])
        action_terms: List[str] = prompt_data.get("key_action_terms", [])
        response_lower = response.lower().strip()

        if not response_lower:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"reason": "empty_response"},
            }

        # Interpretation score (0.5 max)
        interp_score = 0.0
        interp_found = 0
        if interp_terms:
            interp_found = self._check_terms(response, interp_terms)
            interp_ratio = interp_found / len(interp_terms)
            if interp_ratio >= 0.5:
                interp_score = 0.5
            elif interp_ratio >= 0.25:
                interp_score = 0.25

        # Action score (0.5 max)
        action_score = 0.0
        action_found = 0
        if action_terms:
            action_found = self._check_terms(response, action_terms)
            action_ratio = action_found / len(action_terms)
            if action_ratio >= 0.5:
                action_score = 0.5
            elif action_ratio >= 0.25:
                action_score = 0.25

        total_score = interp_score + action_score
        success = total_score >= 0.75

        return {
            "success": success,
            "score": round(total_score, 2),
            "metadata": {
                "interpretation_score": interp_score,
                "action_score": action_score,
                "interp_terms_found": interp_found,
                "interp_terms_total": len(interp_terms),
                "action_terms_found": action_found,
                "action_terms_total": len(action_terms),
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are a tool-augmented reasoning agent. You will be given the results of tool calls. "
            "Your task is to: (1) correctly interpret the tool results and identify the key findings, "
            "and (2) specify the correct next action or final answer based on those findings. "
            "Be explicit about both your interpretation and your recommended action."
        )
