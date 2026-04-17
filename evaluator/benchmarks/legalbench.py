"""LegalBench benchmark - Legal reasoning tasks across multiple task types."""

import re
from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


class LegalBenchBenchmark(Benchmark):
    """LegalBench - evaluates legal reasoning including contract interpretation,
    case outcome prediction, statute application, and IRAC-format analysis."""

    def __init__(self):
        config = BenchmarkConfig(
            name="legalbench",
            description=(
                "Legal reasoning tasks: contract clauses, case outcome prediction, "
                "statute application, legal definitions, and IRAC analysis"
            ),
            category="knowledge",
            version="1.0",
            timeout=90,
            max_tokens=1024,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # ----------------------------------------------------------------
            # CONTRACT CLAUSE INTERPRETATION (5 tasks)
            # ----------------------------------------------------------------
            {
                "id": "lb_001",
                "task_type": "contract_interpretation",
                "prompt": (
                    "Read the following contract clause and answer the question.\n\n"
                    "CLAUSE: 'In the event of Force Majeure, including but not limited to acts "
                    "of God, war, strikes, or government action, neither party shall be liable "
                    "for failure to perform its obligations under this Agreement.'\n\n"
                    "QUESTION: A supplier fails to deliver goods because a port authority strike "
                    "blocks shipment. Is the supplier liable for breach of contract?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "not liable",
                "reasoning_keywords": ["force majeure", "strike", "excused", "performance", "clause"],
            },
            {
                "id": "lb_002",
                "task_type": "contract_interpretation",
                "prompt": (
                    "Read the following contract clause and answer the question.\n\n"
                    "CLAUSE: 'This Agreement shall be governed by and construed in accordance "
                    "with the laws of the State of New York, without regard to its conflict of "
                    "law provisions. Any disputes shall be resolved exclusively in the state or "
                    "federal courts located in New York County.'\n\n"
                    "QUESTION: A dispute arises between a California company and a Texas company "
                    "who signed this contract. In which court must the dispute be resolved?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "new york",
                "reasoning_keywords": ["forum selection", "new york", "exclusive", "jurisdiction", "governed"],
            },
            {
                "id": "lb_003",
                "task_type": "contract_interpretation",
                "prompt": (
                    "Read the following contract clause and answer the question.\n\n"
                    "CLAUSE: 'Confidential Information means any non-public information disclosed "
                    "by either party that is designated as confidential or that reasonably should "
                    "be understood to be confidential given the nature of the information and the "
                    "circumstances of disclosure. Obligations under this Section survive termination "
                    "of this Agreement for a period of five (5) years.'\n\n"
                    "QUESTION: The contract was terminated 6 years ago. Is a party still bound "
                    "by the confidentiality obligation for information disclosed during the contract?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "not bound",
                "reasoning_keywords": ["survive", "five years", "expired", "termination", "obligation"],
            },
            {
                "id": "lb_004",
                "task_type": "contract_interpretation",
                "prompt": (
                    "Read the following contract clause and answer the question.\n\n"
                    "CLAUSE: 'Vendor shall indemnify, defend, and hold harmless Client from and "
                    "against any claims, damages, losses, and expenses arising out of or resulting "
                    "from Vendor's negligent acts or omissions in performing services under this "
                    "Agreement.'\n\n"
                    "QUESTION: A third party is injured by the Client's own employee during "
                    "a project. Must the Vendor indemnify the Client for this claim?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "no",
                "reasoning_keywords": ["vendor negligence", "arising out of", "client employee", "indemnity", "scope"],
            },
            {
                "id": "lb_005",
                "task_type": "contract_interpretation",
                "prompt": (
                    "Read the following contract clause and answer the question.\n\n"
                    "CLAUSE: 'Either party may terminate this Agreement for convenience upon "
                    "thirty (30) days written notice. Upon termination, Client shall pay for "
                    "all work completed to the date of termination.'\n\n"
                    "QUESTION: Client sends an email saying 'we're ending the contract' on "
                    "March 1st. Is this valid termination, and when does it take effect?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "march 31",
                "reasoning_keywords": ["written notice", "30 days", "email", "termination", "effective"],
            },
            # ----------------------------------------------------------------
            # CASE OUTCOME PREDICTION (4 tasks)
            # ----------------------------------------------------------------
            {
                "id": "lb_006",
                "task_type": "case_outcome",
                "prompt": (
                    "Based on the following facts, predict the likely legal outcome.\n\n"
                    "FACTS: A retailer posts a price of $50 for a television due to a website "
                    "error; the actual price is $500. A consumer places an order at $50 and "
                    "receives an order confirmation email. The retailer refuses to fulfil the "
                    "order at $50, claiming unilateral mistake.\n\n"
                    "QUESTION: Can the retailer void the contract on the basis of unilateral mistake?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["unilateral mistake", "void", "material", "website", "knew or should have known"],
            },
            {
                "id": "lb_007",
                "task_type": "case_outcome",
                "prompt": (
                    "Based on the following facts, predict the likely legal outcome.\n\n"
                    "FACTS: An employer has a written at-will employment policy. An employee is "
                    "terminated one day before his pension vests. The employee sues, alleging the "
                    "termination was specifically timed to prevent vesting and therefore violates "
                    "the implied covenant of good faith and fair dealing.\n\n"
                    "QUESTION: Does the employee have a viable wrongful termination claim?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["good faith", "bad faith", "at-will", "pension", "motive", "wrongful"],
            },
            {
                "id": "lb_008",
                "task_type": "case_outcome",
                "prompt": (
                    "Based on the following facts, predict the likely legal outcome.\n\n"
                    "FACTS: A landlord rents an apartment to a tenant. After six months, the "
                    "landlord enters the apartment without notice while the tenant is at work "
                    "to perform a non-emergency repair. The tenant sues for breach of quiet "
                    "enjoyment and invasion of privacy.\n\n"
                    "QUESTION: Is the landlord liable?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["quiet enjoyment", "notice", "breach", "landlord", "entry", "invasion"],
            },
            {
                "id": "lb_009",
                "task_type": "case_outcome",
                "prompt": (
                    "Based on the following facts, predict the likely legal outcome.\n\n"
                    "FACTS: A company's non-compete agreement prohibits a former software engineer "
                    "from working at any technology company anywhere in the world for 5 years. "
                    "The engineer takes a job at a competitor in California.\n\n"
                    "QUESTION: Is the non-compete enforceable in California?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "unenforceable",
                "reasoning_keywords": ["california", "non-compete", "void", "business code", "overbroad", "unenforceable"],
            },
            # ----------------------------------------------------------------
            # STATUTE APPLICATION (4 tasks)
            # ----------------------------------------------------------------
            {
                "id": "lb_010",
                "task_type": "statute_application",
                "prompt": (
                    "Apply the following statutory provision to the facts.\n\n"
                    "STATUTE (excerpt): 'Under Title VII of the Civil Rights Act, it is unlawful "
                    "for an employer to discriminate against any individual with respect to "
                    "compensation, terms, conditions, or privileges of employment because of "
                    "such individual\u2019s race, color, religion, sex, or national origin.'\n\n"
                    "FACTS: An employer pays female sales managers 15% less than male sales "
                    "managers with identical qualifications and performance ratings.\n\n"
                    "QUESTION: Does this constitute a violation of Title VII?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["title vii", "sex", "discrimination", "compensation", "disparate", "unlawful"],
            },
            {
                "id": "lb_011",
                "task_type": "statute_application",
                "prompt": (
                    "Apply the following statutory provision to the facts.\n\n"
                    "STATUTE (excerpt): 'The Americans with Disabilities Act requires employers "
                    "with 15 or more employees to provide reasonable accommodation to qualified "
                    "individuals with disabilities, unless doing so would cause undue hardship.'\n\n"
                    "FACTS: An employee with severe anxiety requests to work from home full-time. "
                    "The employer has 200 employees. The role is a customer-facing help desk "
                    "position that has always been performed in-office.\n\n"
                    "QUESTION: Must the employer grant the full-time remote work request?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "not necessarily",
                "reasoning_keywords": ["reasonable accommodation", "undue hardship", "ada", "interactive", "essential function"],
            },
            {
                "id": "lb_012",
                "task_type": "statute_application",
                "prompt": (
                    "Apply the following statutory provision to the facts.\n\n"
                    "STATUTE (excerpt): 'Under the GDPR, a data controller must obtain freely "
                    "given, specific, informed, and unambiguous consent before processing "
                    "personal data for direct marketing purposes.'\n\n"
                    "FACTS: A company pre-ticks a checkbox on a sign-up form that says "
                    "'I agree to receive marketing emails'. Users can un-tick the box.\n\n"
                    "QUESTION: Does this satisfy the GDPR consent requirement for marketing?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "no",
                "reasoning_keywords": ["gdpr", "pre-ticked", "freely given", "unambiguous", "opt-in", "invalid"],
            },
            {
                "id": "lb_013",
                "task_type": "statute_application",
                "prompt": (
                    "Apply the following statutory provision to the facts.\n\n"
                    "STATUTE (excerpt): 'Under 17 U.S.C. § 107, fair use of a copyrighted work "
                    "for purposes such as criticism, comment, news reporting, teaching, "
                    "scholarship, or research is not an infringement of copyright.'\n\n"
                    "FACTS: A professor photocopies 30 pages from a $90 textbook and distributes "
                    "copies to 50 students each semester as a course requirement.\n\n"
                    "QUESTION: Is this likely fair use?\n\n"
                    "Provide your legal conclusion and reasoning."
                ),
                "expected_conclusion": "no",
                "reasoning_keywords": ["fair use", "market harm", "commercial", "amount", "factor", "systematic"],
            },
            # ----------------------------------------------------------------
            # LEGAL DEFINITION QUESTIONS (4 tasks)
            # ----------------------------------------------------------------
            {
                "id": "lb_014",
                "task_type": "legal_definition",
                "prompt": (
                    "What is promissory estoppel and what are its required elements?\n\n"
                    "Apply your definition to this scenario: A company promises an independent "
                    "contractor they will hire him full-time next year. The contractor turns down "
                    "two other job offers in reliance. The company never hires him.\n\n"
                    "Does promissory estoppel apply here?"
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["promissory estoppel", "reliance", "detriment", "promise", "enforce", "reasonable"],
            },
            {
                "id": "lb_015",
                "task_type": "legal_definition",
                "prompt": (
                    "Define 'consideration' in contract law and explain why it is required.\n\n"
                    "SCENARIO: Alice promises to give her nephew $10,000 as a gift for graduating "
                    "from university. After graduation Alice refuses to pay. The nephew sues.\n\n"
                    "Is Alice's promise legally enforceable?"
                ),
                "expected_conclusion": "no",
                "reasoning_keywords": ["consideration", "gratuitous", "gift", "promise", "bargain", "not enforceable"],
            },
            {
                "id": "lb_016",
                "task_type": "legal_definition",
                "prompt": (
                    "Define 'negligence per se' and explain its significance.\n\n"
                    "SCENARIO: A driver runs a red light (violating a traffic statute) and "
                    "collides with a pedestrian who was crossing lawfully. The pedestrian sues "
                    "in negligence.\n\n"
                    "Can the pedestrian invoke negligence per se, and what effect does it have?"
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["negligence per se", "statute", "duty", "breach", "presumption", "traffic"],
            },
            {
                "id": "lb_017",
                "task_type": "legal_definition",
                "prompt": (
                    "What is the 'business judgment rule' in corporate law?\n\n"
                    "SCENARIO: A board of directors approves an acquisition that subsequently "
                    "loses $50 million. Shareholders sue the directors for breach of fiduciary duty. "
                    "The directors conducted due diligence and obtained a fairness opinion before voting.\n\n"
                    "Are the directors protected by the business judgment rule?"
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["business judgment", "due diligence", "informed", "good faith", "fiduciary", "protected"],
            },
            # ----------------------------------------------------------------
            # IRAC-FORMAT ANALYSIS (3 tasks)
            # ----------------------------------------------------------------
            {
                "id": "lb_018",
                "task_type": "irac_analysis",
                "prompt": (
                    "Using IRAC format (Issue, Rule, Application, Conclusion), analyse the "
                    "following scenario.\n\n"
                    "SCENARIO: Sarah, a 16-year-old, signs a contract to buy a used car for "
                    "$8,000 from a dealership. Two months later she regrets the purchase and "
                    "seeks to void the contract and get her money back.\n\n"
                    "Can Sarah void the contract? Apply the relevant legal doctrine."
                ),
                "expected_conclusion": "yes",
                "reasoning_keywords": ["minor", "infancy", "disaffirm", "voidable", "capacity", "restitution"],
            },
            {
                "id": "lb_019",
                "task_type": "irac_analysis",
                "prompt": (
                    "Using IRAC format, analyse the following scenario.\n\n"
                    "SCENARIO: Bob offers to sell his house to Carol for $500,000. Carol "
                    "responds: 'I'll buy it for $480,000.' Bob rejects that and says the "
                    "price is $500,000 firm. Carol then says, 'OK, I accept your original "
                    "offer of $500,000.' Bob refuses to sell.\n\n"
                    "Is there a binding contract between Bob and Carol?"
                ),
                "expected_conclusion": "no",
                "reasoning_keywords": ["counteroffer", "rejection", "mirror image", "acceptance", "offer terminated", "contract"],
            },
            {
                "id": "lb_020",
                "task_type": "irac_analysis",
                "prompt": (
                    "Using IRAC format, analyse the following scenario.\n\n"
                    "SCENARIO: TechCorp develops proprietary software using an employee (Dan) "
                    "who signs a standard employment agreement with a clause stating all work "
                    "product created during employment is a 'work made for hire' belonging to "
                    "TechCorp. Dan later claims copyright ownership of the software.\n\n"
                    "Who owns the copyright to the software?"
                ),
                "expected_conclusion": "techcorp",
                "reasoning_keywords": ["work made for hire", "copyright", "employer", "17 u.s.c", "employment", "ownership"],
            },
        ]

    # ------------------------------------------------------------------
    # Evaluation helpers
    # ------------------------------------------------------------------

    def _contains_conclusion(self, response: str, expected_conclusion: str) -> bool:
        """Check whether the response contains the expected legal conclusion."""
        response_lower = response.lower()
        # Handle multi-word conclusions
        parts = expected_conclusion.lower().split()
        if len(parts) == 1:
            pattern = r'\b' + re.escape(parts[0]) + r'\b'
            return bool(re.search(pattern, response_lower))
        # For phrases, check substring match
        return expected_conclusion.lower() in response_lower

    def _contains_reasoning_keywords(self, response: str, keywords: List[str]) -> float:
        """Return fraction of reasoning keywords present in the response."""
        if not keywords:
            return 0.0
        response_lower = response.lower()
        matched = sum(1 for kw in keywords if kw.lower() in response_lower)
        return matched / len(keywords)

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Scoring:
          0.5 if conclusion is correct
        + 0.5 if reasoning keywords are sufficiently present (threshold >= 0.4)
        Total score in {0.0, 0.5, 1.0}.
        """
        if not response or not response.strip():
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"error": "empty response"},
            }

        expected_conclusion: str = prompt_data.get("expected_conclusion", "")
        reasoning_keywords: List[str] = prompt_data.get("reasoning_keywords", [])

        conclusion_correct = self._contains_conclusion(response, expected_conclusion)
        keyword_fraction = self._contains_reasoning_keywords(response, reasoning_keywords)
        reasoning_present = keyword_fraction >= 0.4

        score = (0.5 if conclusion_correct else 0.0) + (0.5 if reasoning_present else 0.0)
        success = score >= 1.0

        return {
            "success": success,
            "score": round(score, 4),
            "metadata": {
                "task_type": prompt_data.get("task_type", ""),
                "expected_conclusion": expected_conclusion,
                "conclusion_found": conclusion_correct,
                "keyword_fraction": round(keyword_fraction, 4),
                "reasoning_present": reasoning_present,
                "keywords_matched": [
                    kw for kw in reasoning_keywords if kw.lower() in response.lower()
                ],
            },
        }
