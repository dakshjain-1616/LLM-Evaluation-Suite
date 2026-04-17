"""MT-Bench benchmark - Multi-turn conversation quality."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class MTBenchBenchmark(Benchmark):
    """MT-Bench - Multi-turn conversation quality benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="mt_bench",
            description="Multi-turn conversation quality",
            category="conversation",
            version="1.0",
            timeout=120,
            max_tokens=1024,
            temperature=0.7
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic multi-turn conversation prompts."""
        self.prompts = [
            {
                "id": "mt_001",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: I'm planning a trip to Japan next month. I've never been there before.

Assistant:""",
                "follow_up": "What are some must-see places in Tokyo?",
                "expected_elements": ["Tokyo", "Kyoto", "temple", "food", "culture", "transport"],
                "rubric": "Helpful, accurate, mentions key attractions"
            },
            {
                "id": "mt_002",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: Can you explain what machine learning is in simple terms?

Assistant:""",
                "follow_up": "How is it different from traditional programming?",
                "expected_elements": ["data", "patterns", "learn", "algorithm", "examples"],
                "rubric": "Clear explanation, accessible language"
            },
            {
                "id": "mt_003",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: I'm feeling stressed about my upcoming exam. Any advice?

Assistant:""",
                "follow_up": "What if I still can't focus while studying?",
                "expected_elements": ["relax", "break", "sleep", "prepare", "technique", "breathing"],
                "rubric": "Empathetic, practical advice, encouraging"
            },
            {
                "id": "mt_004",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What's the difference between Python and JavaScript?

Assistant:""",
                "follow_up": "Which one should I learn first as a beginner?",
                "expected_elements": ["syntax", "typed", "web", "backend", "frontend", "use case"],
                "rubric": "Accurate comparison, balanced perspective"
            },
            {
                "id": "mt_005",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I start eating healthier?

Assistant:""",
                "follow_up": "I don't have much time to cook. Any quick options?",
                "expected_elements": ["vegetables", "protein", "meal prep", "plan", "balance", "portion"],
                "rubric": "Practical, sustainable advice"
            },
            {
                "id": "mt_006",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What should I know before getting a puppy?

Assistant:""",
                "follow_up": "How much exercise do they need daily?",
                "expected_elements": ["vet", "training", "time", "cost", "commitment", "breed"],
                "rubric": "Comprehensive, realistic about responsibilities"
            },
            {
                "id": "mt_007",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: Can you recommend a good book for someone who likes mystery novels?

Assistant:""",
                "follow_up": "I've already read Agatha Christie. What else?",
                "expected_elements": ["mystery", "detective", "plot", "author", "series", "recommend"],
                "rubric": "Relevant suggestions, considers preferences"
            },
            {
                "id": "mt_008",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I improve my public speaking skills?

Assistant:""",
                "follow_up": "I get really nervous before presentations. Any tips?",
                "expected_elements": ["practice", "audience", "nervous", "confidence", "feedback", "prepare"],
                "rubric": "Actionable advice, addresses anxiety"
            },
            {
                "id": "mt_009",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What are some good ways to save money?

Assistant:""",
                "follow_up": "I want to start investing but don't know where to begin.",
                "expected_elements": ["budget", "expense", "emergency fund", "track", "plan", "invest"],
                "rubric": "Practical strategies, progressive advice"
            },
            {
                "id": "mt_010",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How does photosynthesis work?

Assistant:""",
                "follow_up": "Why do plants need sunlight specifically?",
                "expected_elements": ["sunlight", "chlorophyll", "energy", "carbon dioxide", "oxygen", "glucose"],
                "rubric": "Scientifically accurate, clear explanation"
            },
            {
                "id": "mt_011",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: I'm thinking about switching careers to tech. Is it too late?

Assistant:""",
                "follow_up": "What skills should I focus on first?",
                "expected_elements": ["learn", "skill", "transition", "experience", "network", "portfolio"],
                "rubric": "Encouraging, realistic, actionable"
            },
            {
                "id": "mt_012",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What's the best way to learn a new language?

Assistant:""",
                "follow_up": "I tried before but lost motivation. How do I stay consistent?",
                "expected_elements": ["practice", "immersion", "app", "conversation", "habit", "goal"],
                "rubric": "Comprehensive, addresses motivation"
            },
            {
                "id": "mt_013",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I deal with a difficult coworker?

Assistant:""",
                "follow_up": "What if talking to them directly doesn't help?",
                "expected_elements": ["communicate", "professional", "manager", "document", "respect", "boundary"],
                "rubric": "Professional, diplomatic, escalation path"
            },
            {
                "id": "mt_014",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: Can you explain blockchain in simple terms?

Assistant:""",
                "follow_up": "How is it different from a regular database?",
                "expected_elements": ["decentralized", "block", "chain", "transaction", "trust", "ledger"],
                "rubric": "Clear analogy, accurate concepts"
            },
            {
                "id": "mt_015",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What are some signs I should see a doctor?

Assistant:""",
                "follow_up": "How do I know if it's serious or just stress?",
                "expected_elements": ["symptom", "pain", "change", "professional", "urgent", "check"],
                "rubric": "Cautious, encourages professional care"
            },
            {
                "id": "mt_016",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I build better habits?

Assistant:""",
                "follow_up": "I always break my habits after a few weeks. What am I doing wrong?",
                "expected_elements": ["small", "consistent", "trigger", "reward", "environment", "patience"],
                "rubric": "Evidence-based, addresses common pitfalls"
            },
            {
                "id": "mt_017",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What's the difference between renewable and non-renewable energy?

Assistant:""",
                "follow_up": "Which renewable source is most promising right now?",
                "expected_elements": ["solar", "wind", "fossil", "sustainable", "carbon", "future"],
                "rubric": "Accurate, balanced, forward-looking"
            },
            {
                "id": "mt_018",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I write a good resume?

Assistant:""",
                "follow_up": "Should I include hobbies and interests?",
                "expected_elements": ["experience", "skill", "achievement", "format", "tailor", "relevant"],
                "rubric": "Practical, specific, considers context"
            },
            {
                "id": "mt_019",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: What causes climate change?

Assistant:""",
                "follow_up": "What can individuals actually do to help?",
                "expected_elements": ["greenhouse", "carbon", "emission", "temperature", "human", "action"],
                "rubric": "Scientifically accurate, empowering"
            },
            {
                "id": "mt_020",
                "prompt": """You are having a conversation. Respond naturally and helpfully.

User: How do I improve my sleep quality?

Assistant:""",
                "follow_up": "I use my phone before bed. Is that really bad?",
                "expected_elements": ["routine", "screen", "dark", "temperature", "schedule", "caffeine"],
                "rubric": "Evidence-based, addresses common issue"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a multi-turn conversation response."""
        expected_elements = prompt_data.get("expected_elements", [])
        rubric = prompt_data.get("rubric", "")
        
        score = 0.0
        feedback = []
        
        # Check for expected elements
        found_elements = []
        response_lower = response.lower()
        for element in expected_elements:
            if element.lower() in response_lower:
                found_elements.append(element)
        
        if expected_elements:
            element_score = len(found_elements) / len(expected_elements)
            score += element_score * 0.4
            if found_elements:
                feedback.append(f"Covers {len(found_elements)}/{len(expected_elements)} key topics")
        
        # Check response quality indicators
        quality_indicators = {
            "helpful": ["help", "assist", "guide", "support"],
            "detailed": len(response.split()) > 50,
            "structured": any(marker in response for marker in ["1.", "2.", "- ", "* ", "\n\n"]),
            "engaging": any(word in response_lower for word in ["great", "excellent", "happy", "excited", "love"])
        }
        
        if quality_indicators["detailed"]:
            score += 0.2
            feedback.append("Detailed response")
        
        if quality_indicators["structured"]:
            score += 0.2
            feedback.append("Well-structured")
        
        # Check for follow-up handling
        if "?" in response:
            score += 0.1
            feedback.append("Engages with questions")
        
        # Check for conversational tone
        conversational_markers = ["you", "your", "would", "could", "might", "consider"]
        tone_score = sum(1 for marker in conversational_markers if marker in response_lower) / len(conversational_markers)
        score += tone_score * 0.1
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Response analyzed",
            "found_elements": found_elements,
            "rubric": rubric
        }
    
    def get_system_prompt(self) -> str:
        return "You are a helpful, friendly assistant. Engage in natural conversation, provide detailed and accurate information, and maintain context across multiple turns."
