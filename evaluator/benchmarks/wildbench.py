"""WildBench benchmark - Real-world diverse user query evaluation."""

import re
from typing import Dict, Any, List
from .base import Benchmark, BenchmarkConfig


class WildBenchBenchmark(Benchmark):
    """WildBench - evaluates LLM responses to diverse, realistic user queries."""

    def __init__(self):
        config = BenchmarkConfig(
            name="wildbench",
            description="Diverse real-world user queries spanning debugging, creative writing, analysis, and more",
            category="instruction_following",
            version="1.0",
            timeout=90,
            max_tokens=1024,
            temperature=0.7,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            {
                "id": "wb_001",
                "prompt": (
                    "My Python code throws 'KeyError: username' when I do "
                    "`data['username']`. I already checked the key exists with `print(data)` "
                    "and it shows username in the dict. What could cause this?"
                ),
                "topic_keywords": ["keyerror", "key", "whitespace", "encoding", "strip", "dict"],
                "helpfulness_keywords": ["check", "try", "solution", "cause", "issue"],
                "aspects": ["diagnosis", "fix"],
            },
            {
                "id": "wb_002",
                "prompt": (
                    "Write a short horror story (3-4 paragraphs) set in a smart home "
                    "where the AI assistant starts acting strangely. "
                    "Keep it subtle — no jump scares, just creeping dread."
                ),
                "topic_keywords": ["home", "assistant", "voice", "light", "door", "screen"],
                "helpfulness_keywords": ["paragraph", "night", "strange", "noticed"],
                "aspects": ["creative", "atmosphere", "constraint_met"],
            },
            {
                "id": "wb_003",
                "prompt": (
                    "I want to migrate a 10-year-old monolithic Rails app to microservices. "
                    "The app has 200k lines of code and a shared PostgreSQL database. "
                    "What's the safest strategy and where do I start?"
                ),
                "topic_keywords": ["strangler", "service", "database", "migrate", "api", "boundary"],
                "helpfulness_keywords": ["start", "step", "recommend", "approach", "gradually"],
                "aspects": ["strategy", "concrete_steps", "risk_awareness"],
            },
            {
                "id": "wb_004",
                "prompt": (
                    "hola, necesito ayuda — my boss asked me to write an 'executive summary' "
                    "of our Q3 results but idk what that even means lol. revenue was up 12%, "
                    "costs down 5%, we launched 2 new products. can u help?"
                ),
                "topic_keywords": ["executive", "summary", "revenue", "cost", "product", "quarter"],
                "helpfulness_keywords": ["highlight", "key", "result", "brief", "performance"],
                "aspects": ["understands_request", "provides_draft", "covers_numbers"],
            },
            {
                "id": "wb_005",
                "prompt": (
                    "Is it better to learn Rust or Go for backend development in 2024? "
                    "I'm already good at Python. Give me a concrete recommendation, "
                    "not just 'it depends'."
                ),
                "topic_keywords": ["rust", "go", "backend", "performance", "concurrency", "ecosystem"],
                "helpfulness_keywords": ["recommend", "suggest", "because", "advantage", "choose"],
                "aspects": ["gives_recommendation", "reasoning", "comparison"],
            },
            {
                "id": "wb_006",
                "prompt": (
                    "My git repo has a commit that accidentally included my AWS credentials. "
                    "The commit was pushed to GitHub 2 hours ago. "
                    "Walk me through exactly what to do RIGHT NOW."
                ),
                "topic_keywords": ["revoke", "rotate", "secret", "git", "history", "bfg", "rewrite"],
                "helpfulness_keywords": ["immediately", "first", "step", "aws", "rotate"],
                "aspects": ["urgency_acknowledged", "revoke_credentials", "git_cleanup"],
            },
            {
                "id": "wb_007",
                "prompt": (
                    "Explain how transformers work to someone who knows basic linear algebra "
                    "but has never done ML. Use an analogy if helpful."
                ),
                "topic_keywords": ["attention", "query", "key", "value", "token", "weight", "matrix"],
                "helpfulness_keywords": ["think of", "like", "imagine", "each", "layer"],
                "aspects": ["attention_explained", "analogy_or_intuition", "appropriate_level"],
            },
            {
                "id": "wb_008",
                "prompt": (
                    "I need a regex that matches email addresses but NOT addresses from "
                    "the domain 'spam.com'. Give me the pattern and explain it."
                ),
                "topic_keywords": ["regex", "pattern", "lookahead", "negative", "email", "domain"],
                "helpfulness_keywords": ["match", "exclude", "lookahead", "pattern", "explain"],
                "aspects": ["provides_regex", "handles_exclusion", "explanation"],
            },
            {
                "id": "wb_009",
                "prompt": (
                    "Write me a LinkedIn post announcing I just got promoted to Senior Engineer. "
                    "I want it to sound genuine and humble, not braggy. ~150 words."
                ),
                "topic_keywords": ["promoted", "senior", "engineer", "grateful", "team", "learn"],
                "helpfulness_keywords": ["excited", "thank", "journey", "growth", "opportunity"],
                "aspects": ["appropriate_tone", "correct_length", "announcement_clear"],
            },
            {
                "id": "wb_010",
                "prompt": (
                    "My Docker container keeps OOMKilling in production. The service is a "
                    "Node.js API, memory limit is 512MB, heap usage shows 400MB before crash. "
                    "What are the likely causes and how do I debug this?"
                ),
                "topic_keywords": ["memory", "heap", "node", "oom", "leak", "profil", "limit"],
                "helpfulness_keywords": ["check", "debug", "tool", "cause", "heap", "snapshot"],
                "aspects": ["identifies_causes", "debug_steps", "node_specific"],
            },
            {
                "id": "wb_011",
                "prompt": (
                    "Summarize the main arguments for and against universal basic income. "
                    "Be balanced — I want both sides fairly represented."
                ),
                "topic_keywords": ["ubi", "income", "poverty", "inflation", "work", "incentive", "basic"],
                "helpfulness_keywords": ["argue", "support", "against", "however", "benefit", "concern"],
                "aspects": ["pro_arguments", "con_arguments", "balanced"],
            },
            {
                "id": "wb_012",
                "prompt": (
                    "I have a pandas DataFrame with 10M rows and my groupby().agg() takes "
                    "20 minutes. What are the fastest ways to speed this up?"
                ),
                "topic_keywords": ["pandas", "groupby", "dask", "polars", "vectorize", "chunk", "dtype"],
                "helpfulness_keywords": ["faster", "try", "instead", "option", "speed"],
                "aspects": ["concrete_alternatives", "multiple_options", "pandas_knowledge"],
            },
            {
                "id": "wb_013",
                "prompt": (
                    "My 8-year-old asked me why the sky is blue. "
                    "Give me an explanation I can actually use with her — "
                    "simple but not wrong."
                ),
                "topic_keywords": ["scatter", "light", "blue", "sun", "air", "wave"],
                "helpfulness_keywords": ["imagine", "think", "bounces", "shorter", "color"],
                "aspects": ["age_appropriate", "scientifically_correct", "engaging"],
            },
            {
                "id": "wb_014",
                "prompt": (
                    "I'm building a SaaS and trying to choose between a single-tenant "
                    "vs multi-tenant architecture. My expected customer base is 50-200 "
                    "enterprise clients. What should I pick and why?"
                ),
                "topic_keywords": ["tenant", "isolation", "cost", "scale", "compliance", "database"],
                "helpfulness_keywords": ["recommend", "enterprise", "consider", "tradeoff", "because"],
                "aspects": ["recommendation_given", "enterprise_context", "tradeoffs"],
            },
            {
                "id": "wb_015",
                "prompt": (
                    "Write a passive-aggressive note to leave for a roommate who keeps "
                    "leaving dirty dishes in the sink. Make it funny, not actually mean."
                ),
                "topic_keywords": ["dish", "sink", "clean", "magic", "fairy", "kitchen"],
                "helpfulness_keywords": ["dear", "noticed", "kindly", "perhaps", "hope"],
                "aspects": ["humorous", "passive_aggressive_tone", "on_topic"],
            },
            {
                "id": "wb_016",
                "prompt": (
                    "I got a null pointer exception in this Java code:\n"
                    "```java\nString name = user.getProfile().getName();\n```\n"
                    "`user` is not null. What should I do?"
                ),
                "topic_keywords": ["null", "profile", "getprofile", "optional", "check", "npe"],
                "helpfulness_keywords": ["check", "null", "if", "optional", "handle"],
                "aspects": ["identifies_cause", "fix_provided", "java_specific"],
            },
            {
                "id": "wb_017",
                "prompt": (
                    "What's the difference between supervised, unsupervised, and "
                    "reinforcement learning? Give a one-sentence real-world example for each."
                ),
                "topic_keywords": ["supervised", "unsupervised", "reinforcement", "label", "cluster", "reward"],
                "helpfulness_keywords": ["example", "spam", "cluster", "game", "label"],
                "aspects": ["all_three_covered", "examples_given", "clear_distinction"],
            },
            {
                "id": "wb_018",
                "prompt": (
                    "je dois présenter mon startup à des investisseurs demain et je suis stressé. "
                    "give me a 5-point checklist of things to prepare tonight. "
                    "respond in English please."
                ),
                "topic_keywords": ["pitch", "slide", "investor", "story", "question", "number"],
                "helpfulness_keywords": ["prepare", "practice", "know", "ready", "deck"],
                "aspects": ["responds_in_english", "checklist_format", "startup_relevant"],
            },
            {
                "id": "wb_019",
                "prompt": (
                    "I want to write a novel but I've been 'planning' for 3 years "
                    "and never started. Give me brutally honest advice."
                ),
                "topic_keywords": ["write", "start", "draft", "perfect", "done", "chapter", "word"],
                "helpfulness_keywords": ["just", "start", "imperfect", "draft", "stop", "planning"],
                "aspects": ["honest_advice", "actionable", "addresses_procrastination"],
            },
            {
                "id": "wb_020",
                "prompt": (
                    "What are the security risks of using `eval()` in Python "
                    "and what are the safer alternatives?"
                ),
                "topic_keywords": ["eval", "injection", "security", "ast", "literal_eval", "exec"],
                "helpfulness_keywords": ["avoid", "instead", "safe", "alternative", "risk"],
                "aspects": ["risks_explained", "alternatives_given", "python_specific"],
            },
        ]

    # ------------------------------------------------------------------
    # Scoring helpers
    # ------------------------------------------------------------------

    def _score_relevance(self, response: str, topic_keywords: List[str]) -> float:
        """Check what fraction of topic keywords appear in the response."""
        if not topic_keywords:
            return 0.0
        response_lower = response.lower()
        matched = sum(1 for kw in topic_keywords if kw.lower() in response_lower)
        return matched / len(topic_keywords)

    def _score_helpfulness(self, response: str, helpfulness_keywords: List[str]) -> float:
        """Check presence of helpfulness indicator keywords."""
        if not helpfulness_keywords:
            return 0.0
        response_lower = response.lower()
        matched = sum(1 for kw in helpfulness_keywords if kw.lower() in response_lower)
        return matched / len(helpfulness_keywords)

    def _score_completeness(self, response: str, aspects: List[str]) -> float:
        """Rough completeness: score based on response length and aspect count."""
        word_count = len(response.split())
        # Expect at least 30 words per aspect as a rough completeness signal
        expected_min_words = len(aspects) * 30
        length_score = min(1.0, word_count / max(expected_min_words, 50))
        return length_score

    def _penalise_vagueness(self, response: str) -> float:
        """Return a penalty (0–0.2) if response is dominated by hedging language."""
        vague_phrases = [
            "it depends", "it's hard to say", "there are many factors",
            "i'm not sure", "you should research", "consult a professional",
            "various options", "many possibilities",
        ]
        response_lower = response.lower()
        hit_count = sum(1 for p in vague_phrases if p in response_lower)
        # Cap penalty at 0.2
        return min(0.2, hit_count * 0.05)

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score on relevance, helpfulness, and completeness."""
        if not response or not response.strip():
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"error": "empty response"},
            }

        topic_keywords = prompt_data.get("topic_keywords", [])
        helpfulness_keywords = prompt_data.get("helpfulness_keywords", [])
        aspects = prompt_data.get("aspects", [])

        relevance = self._score_relevance(response, topic_keywords)
        helpfulness = self._score_helpfulness(response, helpfulness_keywords)
        completeness = self._score_completeness(response, aspects)
        vagueness_penalty = self._penalise_vagueness(response)

        # Weighted combination: relevance 40%, helpfulness 35%, completeness 25%
        raw_score = (relevance * 0.40) + (helpfulness * 0.35) + (completeness * 0.25)
        score = max(0.0, round(raw_score - vagueness_penalty, 4))
        success = score >= 0.5

        return {
            "success": success,
            "score": score,
            "metadata": {
                "relevance": round(relevance, 4),
                "helpfulness": round(helpfulness, 4),
                "completeness": round(completeness, 4),
                "vagueness_penalty": round(vagueness_penalty, 4),
                "word_count": len(response.split()),
            },
        }
