"""AgentBench benchmark - Multi-step agent capability tasks."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class AgentBenchBenchmark(Benchmark):
    """AgentBench - Multi-step agent capability benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="agentbench",
            description="Multi-step agent capability tasks",
            category="agent",
            version="1.0",
            timeout=120,
            max_tokens=1024,
            temperature=0.2
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic agent capability task prompts."""
        self.prompts = [
            {
                "id": "agent_001",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Book a flight from New York to London for next Tuesday, returning Friday. Find the cheapest option with one stop or less.

Available tools: search_flights, compare_prices, book_flight

Think step by step:""",
                "expected": ["search_flights", "compare_prices", "book_flight"],
                "explanation": "Multi-step flight booking workflow"
            },
            {
                "id": "agent_002",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Research weather forecast for San Francisco for 5 days and create a packing list.

Available tools: get_weather_forecast, analyze_conditions, generate_packing_list

Think step by step:""",
                "expected": ["get_weather_forecast", "analyze_conditions", "generate_packing_list"],
                "explanation": "Weather research and packing workflow"
            },
            {
                "id": "agent_003",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Find a restaurant within 2 miles serving Italian food, rating 4+ stars, for 6 people tonight at 7pm.

Available tools: search_restaurants, filter_by_rating, check_availability, make_reservation

Think step by step:""",
                "expected": ["search_restaurants", "filter_by_rating", "check_availability", "make_reservation"],
                "explanation": "Restaurant search and reservation workflow"
            },
            {
                "id": "agent_004",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Summarize latest quarterly earnings report for Apple Inc. and identify key financial metrics.

Available tools: search_documents, extract_financial_data, calculate_metrics, generate_summary

Think step by step:""",
                "expected": ["search_documents", "extract_financial_data", "calculate_metrics", "generate_summary"],
                "explanation": "Financial document analysis workflow"
            },
            {
                "id": "agent_005",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Debug a Python script failing with MemoryError when processing large CSV files.

Available tools: read_file, analyze_error, search_documentation, suggest_fix, test_solution

Think step by step:""",
                "expected": ["read_file", "analyze_error", "search_documentation", "suggest_fix", "test_solution"],
                "explanation": "Debugging workflow with multiple steps"
            },
            {
                "id": "agent_006",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Plan a road trip from Los Angeles to San Francisco with 3 scenic stops, estimating driving time and fuel costs.

Available tools: calculate_route, find_attractions, estimate_travel_time, calculate_fuel_cost

Think step by step:""",
                "expected": ["calculate_route", "find_attractions", "estimate_travel_time", "calculate_fuel_cost"],
                "explanation": "Trip planning workflow"
            },
            {
                "id": "agent_007",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Create a weekly meal plan meeting nutritional requirements for a 2000-calorie diet.

Available tools: search_recipes, analyze_nutrition, check_macros, generate_meal_plan

Think step by step:""",
                "expected": ["search_recipes", "analyze_nutrition", "check_macros", "generate_meal_plan"],
                "explanation": "Meal planning workflow"
            },
            {
                "id": "agent_008",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Compare three laptop models based on specs, price, and reviews for software development.

Available tools: get_product_specs, get_pricing, aggregate_reviews, compare_products

Think step by step:""",
                "expected": ["get_product_specs", "get_pricing", "aggregate_reviews", "compare_products"],
                "explanation": "Product comparison workflow"
            },
            {
                "id": "agent_009",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Schedule a meeting between 5 team members across different time zones for next week.

Available tools: get_availability, find_common_slots, convert_timezones, send_invites

Think step by step:""",
                "expected": ["get_availability", "find_common_slots", "convert_timezones", "send_invites"],
                "explanation": "Meeting scheduling workflow"
            },
            {
                "id": "agent_010",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Analyze customer transactions to identify spending patterns and create customer segments.

Available tools: load_data, clean_data, analyze_patterns, create_segments, generate_report

Think step by step:""",
                "expected": ["load_data", "clean_data", "analyze_patterns", "create_segments", "generate_report"],
                "explanation": "Data analysis workflow"
            },
            {
                "id": "agent_011",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Write and send a professional email requesting a deadline extension.

Available tools: analyze_context, draft_email, review_draft, send_email

Think step by step:""",
                "expected": ["analyze_context", "draft_email", "review_draft", "send_email"],
                "explanation": "Email composition workflow"
            },
            {
                "id": "agent_012",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Set up a new Python development environment with virtualenv and required packages.

Available tools: create_virtualenv, activate_environment, install_packages, verify_installation

Think step by step:""",
                "expected": ["create_virtualenv", "activate_environment", "install_packages", "verify_installation"],
                "explanation": "Environment setup workflow"
            },
            {
                "id": "agent_013",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Monitor a website for price drops and send an alert when price falls below $50.

Available tools: scrape_price, compare_price, store_price_history, send_alert

Think step by step:""",
                "expected": ["scrape_price", "compare_price", "store_price_history", "send_alert"],
                "explanation": "Price monitoring workflow"
            },
            {
                "id": "agent_014",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Translate a document from English to Spanish, verify quality, and make corrections.

Available tools: translate_text, check_quality, identify_errors, correct_translation

Think step by step:""",
                "expected": ["translate_text", "check_quality", "identify_errors", "correct_translation"],
                "explanation": "Translation workflow"
            },
            {
                "id": "agent_015",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Create a social media content calendar for a week with post ideas and optimal timing.

Available tools: analyze_audience, generate_content_ideas, research_optimal_times, suggest_hashtags, create_calendar

Think step by step:""",
                "expected": ["analyze_audience", "generate_content_ideas", "research_optimal_times", "suggest_hashtags", "create_calendar"],
                "explanation": "Content planning workflow"
            },
            {
                "id": "agent_016",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Troubleshoot a home Wi-Fi network experiencing intermittent disconnections.

Available tools: diagnose_connection, check_router_settings, scan_interference, suggest_fixes, apply_configuration

Think step by step:""",
                "expected": ["diagnose_connection", "check_router_settings", "scan_interference", "suggest_fixes", "apply_configuration"],
                "explanation": "Network troubleshooting workflow"
            },
            {
                "id": "agent_017",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Generate a personalized workout plan based on fitness goals and available equipment.

Available tools: assess_fitness_level, define_goals, select_exercises, structure_routine, provide_instructions

Think step by step:""",
                "expected": ["assess_fitness_level", "define_goals", "select_exercises", "structure_routine", "provide_instructions"],
                "explanation": "Fitness planning workflow"
            },
            {
                "id": "agent_018",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Process images: resize, apply watermarks, and organize into folders by date.

Available tools: scan_directory, read_metadata, resize_image, apply_watermark, organize_by_date

Think step by step:""",
                "expected": ["scan_directory", "read_metadata", "resize_image", "apply_watermark", "organize_by_date"],
                "explanation": "Image processing workflow"
            },
            {
                "id": "agent_019",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Research competitors for a new SaaS product and create competitive positioning strategy.

Available tools: identify_competitors, gather_pricing, analyze_features, identify_gaps, create_strategy

Think step by step:""",
                "expected": ["identify_competitors", "gather_pricing", "analyze_features", "identify_gaps", "create_strategy"],
                "explanation": "Competitive analysis workflow"
            },
            {
                "id": "agent_020",
                "prompt": """You are an AI agent. Complete this multi-step task:

Task: Automate backup of important files to cloud storage with encryption and verification.

Available tools: identify_files, compress_files, encrypt_archive, upload_to_cloud, verify_backup

Think step by step:""",
                "expected": ["identify_files", "compress_files", "encrypt_archive", "upload_to_cloud", "verify_backup"],
                "explanation": "Backup automation workflow"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate an agent task response."""
        expected = prompt_data.get("expected", [])
        
        steps = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            for tool in expected:
                if tool in line.lower():
                    steps.append(tool)
                    break
            match = re.match(r'^\d+[.\)]\s*(?:Step\s*\d*:?\s*)?(.+)', line, re.IGNORECASE)
            if match:
                content = match.group(1)
                for tool in expected:
                    if tool in content.lower():
                        steps.append(tool)
        
        unique_steps = []
        for step in steps:
            if step not in unique_steps:
                unique_steps.append(step)
        
        if not expected:
            score = 0.0
        else:
            matched = len(set(unique_steps) & set(expected))
            score = matched / len(expected)
        
        has_reasoning = any(word in response.lower() for word in ['because', 'therefore', 'first', 'then', 'next', 'finally', 'step'])
        
        if has_reasoning:
            score = min(score + 0.1, 1.0)
        
        feedback = []
        if unique_steps:
            feedback.append(f"Identified {len(unique_steps)} steps")
        if has_reasoning:
            feedback.append("Shows clear reasoning")
        
        return {
            "success": score >= 0.5,
            "score": min(score, 1.0),
            "feedback": "; ".join(feedback) if feedback else "Response analyzed",
            "extracted_steps": unique_steps[:10],
            "expected_steps": expected
        }
    
    def get_system_prompt(self) -> str:
        return "You are an AI agent. Break down the task into clear steps, identify which tools to use, and explain your reasoning. List the steps in order."
