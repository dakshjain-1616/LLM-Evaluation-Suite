"""MMMU-Pro benchmark - Multimodal understanding."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class MMMUProBenchmark(Benchmark):
    """MMMU-Pro - Multimodal understanding benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="mmmu_pro",
            description="Multimodal understanding",
            category="multimodal",
            version="1.0",
            timeout=60,
            max_tokens=1024,
            temperature=0.2
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic multimodal understanding prompts."""
        self.prompts = [
            {
                "id": "mmmu_001",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A bar chart showing quarterly sales for three products (A, B, C) across Q1-Q4. Product A: 100, 150, 200, 250. Product B: 180, 180, 180, 180. Product C: 200, 180, 160, 140.

Question: Which product had the highest total sales?

A) Product A
B) Product B
C) Product C
D) All equal

Select the correct answer.""",
                "expected": "B",
                "explanation": "Product B: 180*4=720, Product A: 700, Product C: 680"
            },
            {
                "id": "mmmu_002",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A pie chart showing market share: Alpha (35%), Beta (25%), Gamma (20%), Delta (15%), Epsilon (5%).

Question: What is the combined market share of the top two companies?

A) 50%
B) 60%
C) 70%
D) 80%

Select the correct answer.""",
                "expected": "B",
                "explanation": "Alpha (35%) + Beta (25%) = 60%"
            },
            {
                "id": "mmmu_003",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A line graph showing temperature over 24 hours: 15°C at 00:00, rises to 25°C at 12:00, peaks at 28°C at 14:00, falls to 18°C at 23:00.

Question: What is the temperature range?

A) 10°C
B) 13°C
C) 15°C
D) 28°C

Select the correct answer.""",
                "expected": "B",
                "explanation": "Range = max - min = 28°C - 15°C = 13°C"
            },
            {
                "id": "mmmu_004",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A Venn diagram with two overlapping circles. Circle A: {1,2,3,4,5}. Circle B: {4,5,6,7,8}. Intersection: {4,5}.

Question: How many elements are in the union of A and B?

A) 5
B) 8
C) 10
D) 13

Select the correct answer.""",
                "expected": "B",
                "explanation": "Union = {1,2,3,4,5,6,7,8} = 8 elements"
            },
            {
                "id": "mmmu_005",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A flowchart: Start → Input → Decision (Yes/No) → If Yes: Process A → Output; If No: Process B → Output → End.

Question: How many distinct paths exist from Start to End?

A) 1
B) 2
C) 3
D) 4

Select the correct answer.""",
                "expected": "B",
                "explanation": "Two paths through the decision point"
            },
            {
                "id": "mmmu_006",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A table showing student grades: Alice (Math:85, Science:90, English:88), Bob (Math:92, Science:85, English:78), Carol (Math:78, Science:95, English:92).

Question: Who has the highest average grade?

A) Alice
B) Bob
C) Carol
D) Tie

Select the correct answer.""",
                "expected": "C",
                "explanation": "Carol: 88.3, Alice: 87.7, Bob: 85"
            },
            {
                "id": "mmmu_007",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A scatter plot with points clustering in bottom-left (0-30, 0-30) and top-right (70-100, 70-100) regions.

Question: What does this pattern suggest?

A) Strong positive correlation
B) Strong negative correlation
C) Bimodal distribution
D) Uniform distribution

Select the correct answer.""",
                "expected": "C",
                "explanation": "Two distinct clusters indicate bimodal distribution"
            },
            {
                "id": "mmmu_008",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A timeline 2010-2024: 2010-Smartphones(20%), 2014-Tablets(15%), 2018-Streaming(40%), 2022-AI(10%), 2024-AI(60%).

Question: Which technology showed fastest growth?

A) Smartphones
B) Tablets
C) Streaming
D) AI Tools

Select the correct answer.""",
                "expected": "D",
                "explanation": "AI grew from 10% to 60% in 2 years, fastest rate"
            },
            {
                "id": "mmmu_009",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A network diagram with 5 nodes (A,B,C,D,E). Connections: A-B, A-C, B-C, B-D, C-E, D-E. Node B is central.

Question: Which node has the highest degree?

A) A
B) B
C) C
D) E

Select the correct answer.""",
                "expected": "B",
                "explanation": "B connects to A, C, D (3 connections)"
            },
            {
                "id": "mmmu_010",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A Gantt chart: Task A (Week 1-2), Task B (Week 2-4), Task C (Week 3-5), Task D (Week 5-6). Tasks B and C overlap.

Question: What is the critical path length in weeks?

A) 4
B) 5
C) 6
D) 7

Select the correct answer.""",
                "expected": "C",
                "explanation": "Longest path is 6 weeks"
            },
            {
                "id": "mmmu_011",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A chemical structure showing a benzene ring with alternating double bonds and a hydroxyl group (-OH) attached.

Question: What functional group is present?

A) Alcohol
B) Ketone
C) Aldehyde
D) Carboxylic acid

Select the correct answer.""",
                "expected": "A",
                "explanation": "The -OH group indicates an alcohol functional group"
            },
            {
                "id": "mmmu_012",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A geometric diagram showing a right triangle with sides 3, 4, 5. The right angle is between sides 3 and 4.

Question: What is the area of this triangle?

A) 6
B) 12
C) 15
D) 20

Select the correct answer.""",
                "expected": "A",
                "explanation": "Area = 1/2 * 3 * 4 = 6"
            },
            {
                "id": "mmmu_013",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A sequence: Circle, Square, Triangle, Circle, Square, ?

Question: What shape comes next?

A) Circle
B) Square
C) Triangle
D) Rectangle

Select the correct answer.""",
                "expected": "C",
                "explanation": "Pattern repeats: Circle, Square, Triangle"
            },
            {
                "id": "mmmu_014",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A map with cities A, B, C, D connected by roads: A-B (50km), B-C (30km), C-D (40km), A-D (120km), B-D (80km).

Question: What is the shortest path from A to D?

A) A-B-C-D (120km)
B) A-D direct (120km)
C) A-B-D (130km)
D) A-C-D (not connected)

Select the correct answer.""",
                "expected": "A",
                "explanation": "A-B-C-D = 50+30+40 = 120km"
            },
            {
                "id": "mmmu_015",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A weather map showing low-pressure (L) in west, high-pressure (H) in east. Wind arrows circulate counterclockwise around L.

Question: In which direction will wind blow north of the low-pressure center?

A) North
B) South
C) West
D) East

Select the correct answer.""",
                "expected": "C",
                "explanation": "North of low pressure, winds blow west"
            },
            {
                "id": "mmmu_016",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: An organizational chart: CEO at top, 3 VPs below, each VP has 2 managers.

Question: How many total management positions?

A) 6
B) 7
C) 10
D) 12

Select the correct answer.""",
                "expected": "C",
                "explanation": "1 CEO + 3 VPs + 6 Managers = 10 positions"
            },
            {
                "id": "mmmu_017",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A stock chart showing daily prices. Starts at $50, volatile between $45-$55, ends at $52.

Question: What is the approximate percentage return?

A) -4%
B) +4%
C) +10%
D) +20%

Select the correct answer.""",
                "expected": "B",
                "explanation": "($52 - $50) / $50 = 4% return"
            },
            {
                "id": "mmmu_018",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A food web: Plants → Rabbit → Fox; Plants → Deer → Wolf; Plants → Insects → Birds.

Question: Which organism is a primary consumer?

A) Fox
B) Wolf
C) Rabbit
D) Birds

Select the correct answer.""",
                "expected": "C",
                "explanation": "Rabbit eats plants directly, making it a primary consumer"
            },
            {
                "id": "mmmu_019",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A floor plan: Entry → Living Room (Kitchen, Bedroom 1), Kitchen → Bedroom 2, Bathroom.

Question: How many rooms directly connected to Kitchen?

A) 1
B) 2
C) 3
D) 4

Select the correct answer.""",
                "expected": "C",
                "explanation": "Kitchen connects to Living Room, Bedroom 2, Bathroom = 3 rooms"
            },
            {
                "id": "mmmu_020",
                "prompt": """You are analyzing a described image. Answer the question.

Image Description: A phase diagram showing solid, liquid, gas states with a triple point where all three meet.

Question: What happens at the triple point?

A) Only solid exists
B) Only liquid exists
C) Solid, liquid, and gas coexist
D) Plasma forms

Select the correct answer.""",
                "expected": "C",
                "explanation": "At triple point, all three phases coexist in equilibrium"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a multimodal understanding response."""
        expected = prompt_data.get("expected", "")
        
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
        return "You are analyzing a described visual element. Answer the question based on the description. Select the correct letter (A, B, C, or D)."
