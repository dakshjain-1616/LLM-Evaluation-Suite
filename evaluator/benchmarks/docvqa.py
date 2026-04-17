"""DocVQA benchmark - Document visual question answering via text-described documents."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class DocVQABenchmark(Benchmark):
    """DocVQA - Document understanding tasks described textually."""

    def __init__(self):
        config = BenchmarkConfig(
            name="docvqa",
            description="Document understanding and extraction tasks",
            category="multimodal",
            version="1.0",
            timeout=60,
            max_tokens=2048,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load document understanding prompts with inline document descriptions."""
        self.prompts = [
            {
                "id": "docvqa_001",
                "prompt": (
                    "A W-2 tax form shows the following fields:\n"
                    "  Employer: Acme Corp\n"
                    "  Employee: Sarah Johnson\n"
                    "  Box 1 (Wages): $92,400\n"
                    "  Box 2 (Federal income tax withheld): $18,480\n"
                    "  Box 4 (Social Security tax withheld): $5,729\n"
                    "  Box 6 (Medicare tax withheld): $1,340\n\n"
                    "What is the total amount of all taxes withheld from Sarah Johnson's wages?"
                ),
                "expected": "25549",
                "expected_display": "$25,549",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_002",
                "prompt": (
                    "An invoice from TechSupply LLC reads:\n"
                    "  Invoice #: INV-2024-0871\n"
                    "  Date: March 15, 2024\n"
                    "  Bill To: DataSoft Inc.\n"
                    "  Item 1: 10 x Wireless Keyboard @ $45.00 = $450.00\n"
                    "  Item 2: 10 x USB Mouse @ $22.50 = $225.00\n"
                    "  Item 3: 5 x Monitor Stand @ $38.00 = $190.00\n"
                    "  Subtotal: $865.00\n"
                    "  Tax (8.5%): [blank]\n"
                    "  Total Due: [blank]\n\n"
                    "Calculate the tax amount and total due on this invoice."
                ),
                "expected": "73.53",
                "expected_display": "Tax: $73.53, Total: $938.53",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_003",
                "prompt": (
                    "A bank statement for account holder Marcus Lee shows:\n"
                    "  Account: Checking ****4421\n"
                    "  Statement period: Feb 1 – Feb 28, 2024\n"
                    "  Opening balance: $3,210.00\n"
                    "  Deposits: $4,500.00 (payroll Feb 15), $200.00 (transfer Feb 20)\n"
                    "  Withdrawals: $1,450.00 (rent Feb 2), $380.00 (groceries), "
                    "$125.00 (electric bill), $89.50 (internet)\n"
                    "  Closing balance: [blank]\n\n"
                    "What is the closing balance on Marcus Lee's account?"
                ),
                "expected": "5865.50",
                "expected_display": "$5,865.50",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_004",
                "prompt": (
                    "A shipping label reads:\n"
                    "  Sender: GreenLeaf Organics, 420 Farm Road, Portland, OR 97201\n"
                    "  Recipient: Clara Nguyen, 88 Maple Ave, Apt 3B, Austin, TX 78701\n"
                    "  Tracking #: 1Z999AA10123456784\n"
                    "  Weight: 4.2 lbs\n"
                    "  Service: UPS Ground\n"
                    "  Estimated Delivery: 5–7 business days\n"
                    "  Declared Value: $75.00\n\n"
                    "What is the recipient's full name and apartment number?"
                ),
                "expected": "Clara Nguyen, Apt 3B",
                "question_type": "extraction",
            },
            {
                "id": "docvqa_005",
                "prompt": (
                    "A payroll stub for employee David Park shows:\n"
                    "  Pay period: April 1–15, 2024\n"
                    "  Gross Pay: $3,750.00\n"
                    "  Federal Tax (22%): $825.00\n"
                    "  State Tax (5%): $187.50\n"
                    "  Social Security (6.2%): $232.50\n"
                    "  Medicare (1.45%): $54.38\n"
                    "  Health Insurance Deduction: $142.00\n"
                    "  401(k) Contribution (4%): $150.00\n"
                    "  Net Pay: [blank]\n\n"
                    "What is David Park's net pay for this pay period?"
                ),
                "expected": "2158.62",
                "expected_display": "$2,158.62",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_006",
                "prompt": (
                    "A purchase order document states:\n"
                    "  PO Number: PO-2024-5532\n"
                    "  Issued By: Metro Hospital Supply Dept.\n"
                    "  Vendor: MedEquip Solutions\n"
                    "  Delivery Address: 100 Health Blvd, Chicago, IL 60601\n"
                    "  Items:\n"
                    "    - Surgical Gloves (Box/100): qty 50, unit price $12.40\n"
                    "    - N95 Masks (Box/20): qty 30, unit price $18.75\n"
                    "    - Disposable Gowns (Pack/10): qty 20, unit price $22.00\n"
                    "  Payment Terms: Net 30\n\n"
                    "What is the total cost of all items on this purchase order?"
                ),
                "expected": "1682.50",
                "expected_display": "$1,682.50",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_007",
                "prompt": (
                    "A lease agreement extract shows:\n"
                    "  Tenant: Priya Sharma\n"
                    "  Landlord: Sunset Properties LLC\n"
                    "  Property: 22 Oak Street, Unit 5, Denver, CO 80203\n"
                    "  Lease Start: June 1, 2024\n"
                    "  Lease Term: 12 months\n"
                    "  Monthly Rent: $1,850\n"
                    "  Security Deposit: 2 months' rent\n"
                    "  Late Fee: 5% of monthly rent after 5-day grace period\n\n"
                    "What is the security deposit amount, and what is the late fee if rent is paid late?"
                ),
                "expected": "3700",
                "expected_display": "Security deposit: $3,700; Late fee: $92.50",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_008",
                "prompt": (
                    "A nutrition label on a cereal box reads:\n"
                    "  Serving Size: 3/4 cup (30g)\n"
                    "  Servings Per Container: About 12\n"
                    "  Calories per serving: 120\n"
                    "  Total Fat: 1.5g (2% DV)\n"
                    "  Sodium: 190mg (8% DV)\n"
                    "  Total Carbohydrate: 25g (9% DV)\n"
                    "  Dietary Fiber: 3g (11% DV)\n"
                    "  Total Sugars: 6g\n"
                    "  Protein: 3g\n\n"
                    "If someone eats the entire box, how many total calories will they consume?"
                ),
                "expected": "1440",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_009",
                "prompt": (
                    "A meeting agenda document reads:\n"
                    "  Meeting: Q2 Product Review\n"
                    "  Date: Thursday, May 9, 2024, 2:00 PM – 4:30 PM\n"
                    "  Location: Conference Room B / Zoom link: zoom.us/j/98765\n"
                    "  Attendees: Emily Chen (Chair), Raj Patel, Sofia Torres, Ben Kim, Aisha Grant\n"
                    "  Agenda:\n"
                    "    2:00–2:15  Welcome and Q1 recap (Emily)\n"
                    "    2:15–3:00  Product roadmap presentation (Raj)\n"
                    "    3:00–3:30  User research findings (Sofia)\n"
                    "    3:30–4:00  Engineering status update (Ben)\n"
                    "    4:00–4:20  Open discussion\n"
                    "    4:20–4:30  Action items and wrap-up\n\n"
                    "Who is presenting the product roadmap, and how long is that presentation slot?"
                ),
                "expected": "Raj Patel, 45 minutes",
                "question_type": "extraction",
            },
            {
                "id": "docvqa_010",
                "prompt": (
                    "A medical prescription form shows:\n"
                    "  Patient: Thomas Okafor, DOB: 03/14/1978\n"
                    "  Prescriber: Dr. Linda Marsh, MD, License #: MD-44821\n"
                    "  Date: April 10, 2024\n"
                    "  Drug: Metformin HCl 500mg tablets\n"
                    "  Directions: Take 1 tablet twice daily with meals\n"
                    "  Quantity: 60 tablets\n"
                    "  Refills: 5\n"
                    "  Substitution permitted: Yes\n\n"
                    "How many total tablets can the patient receive if they use all refills?"
                ),
                "expected": "360",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_011",
                "prompt": (
                    "A flight itinerary reads:\n"
                    "  Passenger: Natalie Brooks\n"
                    "  Booking Ref: XKPQ72\n"
                    "  Flight 1: AA 2241  JFK → ORD  Depart 07:15, Arrive 09:05  (May 18)\n"
                    "  Layover: 2 hr 10 min at ORD\n"
                    "  Flight 2: AA 1837  ORD → LAX  Depart 11:15, Arrive 13:40  (May 18)\n"
                    "  Fare class: Economy, Seat 22D\n"
                    "  Checked bags: 1 (23kg)\n\n"
                    "What is the total travel time from JFK departure to LAX arrival, including the layover?"
                ),
                "expected": "6 hours 25 minutes",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_012",
                "prompt": (
                    "A real estate listing sheet states:\n"
                    "  Address: 47 Birchwood Drive, Burlington, VT 05401\n"
                    "  List Price: $489,000\n"
                    "  Bedrooms: 3  |  Bathrooms: 2.5\n"
                    "  Square Footage: 1,840 sq ft\n"
                    "  Lot Size: 0.28 acres\n"
                    "  Year Built: 1998\n"
                    "  Property Taxes (2023): $6,250/year\n"
                    "  HOA Fee: None\n"
                    "  Days on Market: 14\n\n"
                    "What is the price per square foot for this property?"
                ),
                "expected": "265.76",
                "expected_display": "$265.76 per sq ft",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_013",
                "prompt": (
                    "A business contract clause reads:\n"
                    "  Party A: Vertex Digital Inc. ('Client')\n"
                    "  Party B: PixelForge Studio ('Contractor')\n"
                    "  Project: Website redesign\n"
                    "  Total Contract Value: $24,000\n"
                    "  Payment Schedule:\n"
                    "    25% upon signing\n"
                    "    25% upon design approval\n"
                    "    25% upon development completion\n"
                    "    25% upon final delivery\n"
                    "  Penalty for late delivery: 2% of contract value per week, max 10%\n\n"
                    "What is the maximum penalty amount for late delivery?"
                ),
                "expected": "2400",
                "expected_display": "$2,400",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_014",
                "prompt": (
                    "A survey results table shows:\n"
                    "  Survey: Employee Satisfaction Q1 2024 (n=200 respondents)\n"
                    "  Question: How satisfied are you with your current role?\n"
                    "    Very Satisfied:    72 responses\n"
                    "    Satisfied:         88 responses\n"
                    "    Neutral:           24 responses\n"
                    "    Dissatisfied:      12 responses\n"
                    "    Very Dissatisfied:  4 responses\n\n"
                    "What percentage of employees responded either 'Satisfied' or 'Very Satisfied'?"
                ),
                "expected": "80",
                "expected_display": "80%",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_015",
                "prompt": (
                    "A grant proposal cover page reads:\n"
                    "  Title: Renewable Energy Integration in Rural Communities\n"
                    "  Applicant Organization: CleanFuture Foundation\n"
                    "  Principal Investigator: Dr. Amara Diallo\n"
                    "  Co-Investigator: Prof. James Thornton\n"
                    "  Funding Agency: Department of Energy\n"
                    "  Program: Small Business Innovation Research Phase II\n"
                    "  Requested Amount: $749,850\n"
                    "  Project Period: October 1, 2024 – September 30, 2027\n"
                    "  Project Duration: 36 months\n\n"
                    "Who is the principal investigator, and what is the monthly funding rate?"
                ),
                "expected": "Dr. Amara Diallo, 20829.17",
                "expected_display": "Dr. Amara Diallo; ~$20,829.17/month",
                "question_type": "extraction_calculation",
            },
            {
                "id": "docvqa_016",
                "prompt": (
                    "An academic transcript shows:\n"
                    "  Student: Kenji Yamamoto  |  ID: 20190847\n"
                    "  Major: Computer Science  |  Semester: Fall 2023\n"
                    "  Course Results:\n"
                    "    CS 401 Algorithms         4 credits  A  (4.0)\n"
                    "    CS 415 Machine Learning   3 credits  A- (3.7)\n"
                    "    MATH 310 Linear Algebra   3 credits  B+ (3.3)\n"
                    "    ENG 201 Technical Writing 2 credits  A  (4.0)\n"
                    "    CS 430 Networks           3 credits  B  (3.0)\n\n"
                    "Calculate Kenji's GPA for this semester (weighted by credit hours)."
                ),
                "expected": "3.63",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_017",
                "prompt": (
                    "A product warranty card reads:\n"
                    "  Product: ProSound X9 Wireless Headphones\n"
                    "  Serial Number: PSX9-2024-887643\n"
                    "  Purchase Date: January 22, 2024\n"
                    "  Retailer: SoundWorld Electronics\n"
                    "  Warranty Period: 2 years from purchase date\n"
                    "  Extended Warranty Option: Additional 1 year for $49.99 (must register within 60 days)\n"
                    "  Coverage: Manufacturing defects; excludes physical damage, water damage\n\n"
                    "What is the warranty expiration date, and by what date must the customer register for extended warranty?"
                ),
                "expected": "January 22, 2026",
                "expected_display": "Standard warranty expires January 22, 2026; extended warranty registration deadline March 22, 2024",
                "question_type": "date_calculation",
            },
            {
                "id": "docvqa_018",
                "prompt": (
                    "A city parking citation reads:\n"
                    "  Citation #: PCO-2024-093812\n"
                    "  Date Issued: April 3, 2024\n"
                    "  Vehicle: 2019 Honda Civic, License Plate: 7MNK402\n"
                    "  Location: 200 Block of West Elm Street\n"
                    "  Violation: Expired meter (VC 22500.1)\n"
                    "  Fine Amount: $65.00\n"
                    "  If paid within 30 days: $65.00\n"
                    "  If paid within 31–60 days: $97.50 (50% late surcharge)\n"
                    "  If paid after 60 days: $130.00 (100% late surcharge)\n\n"
                    "What is the license plate of the cited vehicle, and what is the late surcharge percentage if paid between days 31 and 60?"
                ),
                "expected": "7MNK402, 50%",
                "question_type": "extraction",
            },
            {
                "id": "docvqa_019",
                "prompt": (
                    "A conference registration form shows:\n"
                    "  Event: TechForward Summit 2024\n"
                    "  Registrant: Dr. Olivia Pham\n"
                    "  Affiliation: Stanford University\n"
                    "  Registration Type: Academic (Early Bird)\n"
                    "  Registration Fee: $350\n"
                    "  Workshop Selection: AI in Healthcare (+$75), Data Visualization (+$50)\n"
                    "  Dinner Banquet: Yes (+$95)\n"
                    "  Discount Code Applied: RESEARCH15 (15% off registration fee only)\n"
                    "  Total Due: [blank]\n\n"
                    "Calculate the total amount due for Dr. Pham's registration."
                ),
                "expected": "517.50",
                "expected_display": "$517.50",
                "question_type": "calculation",
            },
            {
                "id": "docvqa_020",
                "prompt": (
                    "A home energy bill shows:\n"
                    "  Customer: Robert Finley\n"
                    "  Service Address: 903 Cypress Lane, Nashville, TN 37201\n"
                    "  Billing Period: March 1–31, 2024\n"
                    "  Electricity Used: 980 kWh\n"
                    "  Rate Tiers:\n"
                    "    First 500 kWh: $0.09/kWh\n"
                    "    Next 500 kWh: $0.12/kWh\n"
                    "    Over 1000 kWh: $0.15/kWh\n"
                    "  Fixed Service Charge: $12.50/month\n"
                    "  State Tax (6%): applied to energy charges only\n"
                    "  Total Due: [blank]\n\n"
                    "Calculate Robert Finley's total electricity bill for March 2024."
                ),
                "expected": "107.26",
                "expected_display": "$107.26",
                "question_type": "calculation",
            },
        ]

    def _normalize_numeric(self, text: str) -> Optional[str]:
        """Extract and normalize a numeric value from text."""
        cleaned = text.replace(",", "").replace("$", "").replace("%", "").strip()
        match = re.search(r"\d+\.?\d*", cleaned)
        if match:
            return match.group(0)
        return None

    def _numeric_match(self, extracted: str, expected: str, tolerance: float = 0.02) -> bool:
        """Check if two numeric strings match within a relative tolerance."""
        try:
            e_val = float(extracted)
            x_val = float(expected)
            if x_val == 0:
                return e_val == 0
            return abs(e_val - x_val) / abs(x_val) <= tolerance
        except (ValueError, TypeError):
            return False

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Evaluate a DocVQA response.

        Scoring:
          1.0 - exact or within-tolerance numeric match / exact text match
          0.5 - partial match (key terms present, numeric within 10%)
          0.0 - incorrect
        """
        expected_raw = str(prompt_data.get("expected", ""))
        question_type = prompt_data.get("question_type", "extraction")
        response_lower = response.lower()

        # --- Numeric answer types ---
        if question_type in ("calculation", "date_calculation", "extraction_calculation"):
            expected_num = self._normalize_numeric(expected_raw)
            if expected_num is not None:
                # Search for any numeric value in the response
                candidates = re.findall(r"\d[\d,]*\.?\d*", response.replace(",", ""))
                for candidate in candidates:
                    cand_clean = candidate.replace(",", "")
                    if self._numeric_match(cand_clean, expected_num, tolerance=0.02):
                        return {
                            "success": True,
                            "score": 1.0,
                            "metadata": {
                                "extracted": cand_clean,
                                "expected": expected_num,
                                "match_type": "exact_numeric",
                            },
                        }
                # Partial: within 10% tolerance
                for candidate in candidates:
                    cand_clean = candidate.replace(",", "")
                    if self._numeric_match(cand_clean, expected_num, tolerance=0.10):
                        return {
                            "success": False,
                            "score": 0.5,
                            "metadata": {
                                "extracted": cand_clean,
                                "expected": expected_num,
                                "match_type": "partial_numeric",
                            },
                        }
                return {
                    "success": False,
                    "score": 0.0,
                    "metadata": {"expected": expected_num, "match_type": "no_match"},
                }

        # --- Text / extraction answer types ---
        # Exact match (case-insensitive)
        if expected_raw.lower() in response_lower:
            return {
                "success": True,
                "score": 1.0,
                "metadata": {"expected": expected_raw, "match_type": "exact_text"},
            }

        # Partial: all significant tokens (length > 2) present
        tokens = [t for t in re.split(r"[\s,;]+", expected_raw.lower()) if len(t) > 2]
        if tokens:
            matched_tokens = [t for t in tokens if t in response_lower]
            ratio = len(matched_tokens) / len(tokens)
            if ratio >= 0.8:
                return {
                    "success": True,
                    "score": 1.0,
                    "metadata": {
                        "expected": expected_raw,
                        "match_type": "full_token_match",
                        "ratio": ratio,
                    },
                }
            if ratio >= 0.5:
                return {
                    "success": False,
                    "score": 0.5,
                    "metadata": {
                        "expected": expected_raw,
                        "match_type": "partial_token_match",
                        "ratio": ratio,
                    },
                }

        return {
            "success": False,
            "score": 0.0,
            "metadata": {"expected": expected_raw, "match_type": "no_match"},
        }

    def get_system_prompt(self) -> str:
        return (
            "You are a document analysis assistant. Read the document description carefully "
            "and answer the question precisely. For calculations, show your working and state "
            "the final answer clearly. For extraction tasks, quote the exact value from the document."
        )
