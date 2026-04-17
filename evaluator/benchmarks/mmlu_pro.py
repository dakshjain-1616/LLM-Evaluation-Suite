"""MMLU-Pro benchmark - Professional knowledge multiple choice."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class MMLUProBenchmark(Benchmark):
    """MMLU-Pro - Professional knowledge multiple choice benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="mmlu_pro",
            description="Professional knowledge multiple choice",
            category="knowledge",
            version="1.0",
            timeout=60,
            max_tokens=512,
            temperature=0.1
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic professional knowledge prompts."""
        self.prompts = [
            {
                "id": "mmlu_001",
                "prompt": """Answer this professional knowledge question:

In contract law, what is required for a valid contract to be formed?

A) Only a written agreement
B) Offer, acceptance, consideration, and mutual assent
C) A notarized signature
D) Payment of money

Select the correct answer.""",
                "expected": "B",
                "explanation": "Valid contract requires offer, acceptance, consideration, and mutual assent"
            },
            {
                "id": "mmlu_002",
                "prompt": """Answer this professional knowledge question:

In accounting, which financial statement shows a company's financial position at a specific point in time?

A) Income Statement
B) Balance Sheet
C) Cash Flow Statement
D) Statement of Retained Earnings

Select the correct answer.""",
                "expected": "B",
                "explanation": "Balance sheet shows assets, liabilities, equity at a specific date"
            },
            {
                "id": "mmlu_003",
                "prompt": """Answer this professional knowledge question:

In medical practice, what does HIPAA primarily regulate?

A) Medical malpractice insurance
B) Patient privacy and health information security
C) Pharmaceutical pricing
D) Medical licensing requirements

Select the correct answer.""",
                "expected": "B",
                "explanation": "HIPAA regulates patient privacy and protected health information"
            },
            {
                "id": "mmlu_004",
                "prompt": """Answer this professional knowledge question:

In software engineering, what is the primary purpose of unit testing?

A) To test the entire system end-to-end
B) To test individual components in isolation
C) To test user interfaces
D) To test database performance

Select the correct answer.""",
                "expected": "B",
                "explanation": "Unit testing verifies individual units/components work correctly in isolation"
            },
            {
                "id": "mmlu_005",
                "prompt": """Answer this professional knowledge question:

In project management, what does the critical path represent?

A) The shortest path through a project network
B) The longest path that determines minimum project duration
C) The path with the most resources
D) The path with the highest risk

Select the correct answer.""",
                "expected": "B",
                "explanation": "Critical path is the longest path through project network, determines minimum duration"
            },
            {
                "id": "mmlu_006",
                "prompt": """Answer this professional knowledge question:

In finance, what is the Capital Asset Pricing Model (CAPM) used to calculate?

A) Company bankruptcy probability
B) Expected return on an asset given its systematic risk
C) Optimal debt-to-equity ratio
D) Currency exchange rates

Select the correct answer.""",
                "expected": "B",
                "explanation": "CAPM calculates expected return based on systematic risk (beta)"
            },
            {
                "id": "mmlu_007",
                "prompt": """Answer this professional knowledge question:

In cybersecurity, what is a man-in-the-middle attack?

A) A virus that spreads through email
B) An attacker intercepting communication between two parties
C) A denial of service attack
D) Physical theft of hardware

Select the correct answer.""",
                "expected": "B",
                "explanation": "MITM attack intercepts and potentially alters communication between parties"
            },
            {
                "id": "mmlu_008",
                "prompt": """Answer this professional knowledge question:

In human resources, what is the primary purpose of a 360-degree feedback review?

A) To evaluate only the manager's performance
B) To gather feedback from multiple sources including peers, subordinates, and supervisors
C) To conduct annual salary reviews
D) To assess technical skills only

Select the correct answer.""",
                "expected": "B",
                "explanation": "360-degree feedback collects input from multiple perspectives"
            },
            {
                "id": "mmlu_009",
                "prompt": """Answer this professional knowledge question:

In marketing, what does ROI stand for and measure?

A) Return on Investment - profitability relative to cost
B) Rate of Interest - financial charges
C) Revenue Operating Income - gross profit
D) Response Optimization Index - campaign effectiveness

Select the correct answer.""",
                "expected": "A",
                "explanation": "ROI = Return on Investment, measures profitability relative to investment cost"
            },
            {
                "id": "mmlu_010",
                "prompt": """Answer this professional knowledge question:

In architecture, what does LEED certification primarily evaluate?

A) Historical preservation
B) Environmental sustainability and energy efficiency
C) Structural earthquake resistance
D) Interior design aesthetics

Select the correct answer.""",
                "expected": "B",
                "explanation": "LEED certifies buildings for environmental sustainability and energy efficiency"
            },
            {
                "id": "mmlu_011",
                "prompt": """Answer this professional knowledge question:

In data science, what is overfitting?

A) When a model performs well on training data but poorly on new data
B) When a model has too few parameters
C) When training takes too long
D) When the dataset is too large

Select the correct answer.""",
                "expected": "A",
                "explanation": "Overfitting: model memorizes training data, fails to generalize to new data"
            },
            {
                "id": "mmlu_012",
                "prompt": """Answer this professional knowledge question:

In supply chain management, what does JIT stand for?

A) Just In Transit
B) Just In Time
C) Joint Inventory Tracking
D) Job Integration Technology

Select the correct answer.""",
                "expected": "B",
                "explanation": "JIT = Just In Time inventory management"
            },
            {
                "id": "mmlu_013",
                "prompt": """Answer this professional knowledge question:

In electrical engineering, what does Ohm's Law state?

A) V = I / R
B) V = I × R
C) P = V × I
D) R = V × I

Select the correct answer.""",
                "expected": "B",
                "explanation": "Ohm's Law: Voltage = Current × Resistance (V = IR)"
            },
            {
                "id": "mmlu_014",
                "prompt": """Answer this professional knowledge question:

In business ethics, what is the stakeholder theory?

A) Only shareholders matter
B) All parties affected by business decisions should be considered
C) Only employees matter
D) Only customers matter

Select the correct answer.""",
                "expected": "B",
                "explanation": "Stakeholder theory considers all affected parties, not just shareholders"
            },
            {
                "id": "mmlu_015",
                "prompt": """Answer this professional knowledge question:

In database management, what is ACID?

A) A query language
B) Properties ensuring reliable transactions (Atomicity, Consistency, Isolation, Durability)
C) A data type
D) A security protocol

Select the correct answer.""",
                "expected": "B",
                "explanation": "ACID = Atomicity, Consistency, Isolation, Durability for reliable transactions"
            },
            {
                "id": "mmlu_016",
                "prompt": """Answer this professional knowledge question:

In civil engineering, what is the primary purpose of rebar in concrete?

A) To reduce weight
B) To provide tensile strength
C) To improve aesthetics
D) To increase thermal insulation

Select the correct answer.""",
                "expected": "B",
                "explanation": "Rebar provides tensile strength to complement concrete's compressive strength"
            },
            {
                "id": "mmlu_017",
                "prompt": """Answer this professional knowledge question:

In economics, what is inflation?

A) A decrease in the general price level
B) A sustained increase in the general price level
C) An increase in unemployment
D) A decrease in money supply

Select the correct answer.""",
                "expected": "B",
                "explanation": "Inflation is sustained increase in general price level, decreasing purchasing power"
            },
            {
                "id": "mmlu_018",
                "prompt": """Answer this professional knowledge question:

In machine learning, what is the difference between supervised and unsupervised learning?

A) Supervised uses labeled data, unsupervised does not
B) Supervised is faster
C) Supervised requires more memory
D) There is no difference

Select the correct answer.""",
                "expected": "A",
                "explanation": "Supervised learning uses labeled training data; unsupervised finds patterns without labels"
            },
            {
                "id": "mmlu_019",
                "prompt": """Answer this professional knowledge question:

In quality management, what does Six Sigma aim to achieve?

A) Reduce defects to 3.4 per million opportunities
B) Increase production speed by 6 times
C) Reduce costs by 60%
D) Achieve 99% accuracy

Select the correct answer.""",
                "expected": "A",
                "explanation": "Six Sigma targets 3.4 defects per million opportunities (99.99966% quality)"
            },
            {
                "id": "mmlu_020",
                "prompt": """Answer this professional knowledge question:

In network engineering, what is the purpose of a subnet mask?

A) To encrypt network traffic
B) To divide IP address into network and host portions
C) To filter spam emails
D) To increase bandwidth

Select the correct answer.""",
                "expected": "B",
                "explanation": "Subnet mask separates IP address into network and host portions"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate an MMLU-Pro response."""
        expected = prompt_data.get("expected", "")
        
        # Extract answer choice
        answer_match = re.search(r'\b([A-D])\b', response)
        if not answer_match:
            answer_match = re.search(r'^\s*([A-D])', response)
        
        if not answer_match:
            return {
                "success": False,
                "score": 0.0,
                "feedback": "No valid answer choice found",
                "extracted_answer": None
            }
        
        answer = answer_match.group(1)
        correct = answer == expected
        
        return {
            "success": correct,
            "score": 1.0 if correct else 0.0,
            "feedback": "Correct!" if correct else f"Incorrect. Expected {expected}.",
            "extracted_answer": answer,
            "expected_answer": expected
        }
    
    def get_system_prompt(self) -> str:
        return "You are a professional knowledge expert. Answer the question by selecting the correct letter (A, B, C, or D)."
