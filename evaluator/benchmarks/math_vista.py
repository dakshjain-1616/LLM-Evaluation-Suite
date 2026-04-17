"""MathVista benchmark - Math questions grounded in described charts and figures."""

import re
from typing import Dict, Any, Optional
from .base import Benchmark, BenchmarkConfig


class MathVistaBenchmark(Benchmark):
    """MathVista: math questions about charts, graphs, and tables described in text.
    Evaluates numerical answer extraction with 1% tolerance and partial credit for
    correct approach."""

    def __init__(self):
        config = BenchmarkConfig(
            name="math_vista",
            description=(
                "Math questions grounded in text-described charts, graphs, and figures"
            ),
            category="math_multimodal",
            version="1.0",
            timeout=120,
            max_tokens=2048,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- Bar Charts ---
            {
                "id": "mvista_001",
                "prompt": (
                    "A bar chart shows monthly sales (in units): "
                    "Jan=120, Feb=95, Mar=150, Apr=80, May=200, Jun=175. "
                    "What is the percentage increase from the minimum to the maximum month? "
                    "Round to two decimal places."
                ),
                "expected": 150.0,
                "unit": "%",
                "approach_keywords": ["minimum", "maximum", "increase", "percent"],
            },
            {
                "id": "mvista_002",
                "prompt": (
                    "A bar chart shows the number of students enrolled in five subjects: "
                    "Math=340, Science=280, English=420, History=190, Art=150. "
                    "What fraction of the total enrollment is in Math and Science combined? "
                    "Express as a percentage rounded to one decimal place."
                ),
                "expected": 44.9,
                "unit": "%",
                "approach_keywords": ["total", "sum", "fraction", "percent"],
            },
            {
                "id": "mvista_003",
                "prompt": (
                    "A grouped bar chart compares revenue ($M) for two companies over three years:\n"
                    "Company A: 2022=45, 2023=52, 2024=61\n"
                    "Company B: 2022=38, 2023=47, 2024=55\n"
                    "What is the average annual growth rate (CAGR) for Company A from 2022 to 2024? "
                    "Round to one decimal place."
                ),
                "expected": 16.4,
                "unit": "%",
                "approach_keywords": ["growth", "CAGR", "compound", "rate", "square root"],
            },
            {
                "id": "mvista_004",
                "prompt": (
                    "A horizontal bar chart shows project durations in days: "
                    "Alpha=45, Beta=30, Gamma=60, Delta=25, Epsilon=50. "
                    "By how many days does the longest project exceed the mean project duration?"
                ),
                "expected": 18.0,
                "unit": "days",
                "approach_keywords": ["mean", "average", "longest", "exceed", "difference"],
            },
            # --- Line Graphs ---
            {
                "id": "mvista_005",
                "prompt": (
                    "A line graph shows temperature (°C) at hourly intervals from 6 AM to noon: "
                    "6AM=12, 7AM=14, 8AM=17, 9AM=20, 10AM=22, 11AM=24, 12PM=25. "
                    "What is the average rate of temperature increase per hour over this period?"
                ),
                "expected": 2.17,
                "unit": "°C/hr",
                "approach_keywords": ["rate", "average", "change", "per hour", "slope"],
            },
            {
                "id": "mvista_006",
                "prompt": (
                    "A line graph shows a company's stock price (USD) over 5 days: "
                    "Mon=142.50, Tue=138.20, Wed=145.80, Thu=149.60, Fri=155.30. "
                    "What is the percentage change from Monday's opening to Friday's close? "
                    "Round to two decimal places."
                ),
                "expected": 8.98,
                "unit": "%",
                "approach_keywords": ["change", "percent", "opening", "close", "increase"],
            },
            {
                "id": "mvista_007",
                "prompt": (
                    "A dual-axis line graph shows rainfall (mm) and humidity (%) for six months:\n"
                    "Rainfall: Jan=85, Feb=65, Mar=40, Apr=30, May=20, Jun=15\n"
                    "Humidity: Jan=90, Feb=85, Mar=75, Apr=65, May=55, Jun=50\n"
                    "What is the Pearson correlation between rainfall and humidity values across "
                    "the six months? Round to two decimal places."
                ),
                "expected": 0.99,
                "unit": "",
                "approach_keywords": ["correlation", "pearson", "covariance", "mean", "standard deviation"],
            },
            # --- Pie / Donut Charts ---
            {
                "id": "mvista_008",
                "prompt": (
                    "A pie chart shows a household budget allocation (total = $4800/month): "
                    "Rent=35%, Food=20%, Transport=12%, Entertainment=8%, Savings=15%, Other=10%. "
                    "How much money (in dollars) is allocated to Savings and Entertainment combined?"
                ),
                "expected": 1104.0,
                "unit": "$",
                "approach_keywords": ["savings", "entertainment", "percent", "total", "multiply"],
            },
            {
                "id": "mvista_009",
                "prompt": (
                    "A donut chart shows market-share percentages of five smartphone brands: "
                    "Alpha=32%, Beta=25%, Gamma=18%, Delta=15%, Others=10%. "
                    "If the total market has 240 million units sold, how many units did "
                    "Gamma and Delta sell in total?"
                ),
                "expected": 79.2,
                "unit": "million units",
                "approach_keywords": ["market share", "percent", "total", "units", "multiply"],
            },
            # --- Scatter Plots ---
            {
                "id": "mvista_010",
                "prompt": (
                    "A scatter plot shows study hours (x) and exam scores (y) for 6 students:\n"
                    "(2, 58), (3, 65), (4, 72), (5, 80), (6, 85), (7, 92).\n"
                    "Using the least-squares linear regression line, predict the exam score "
                    "for a student who studies 8 hours. Round to one decimal place."
                ),
                "expected": 98.3,
                "unit": "points",
                "approach_keywords": ["regression", "slope", "intercept", "predict", "linear"],
            },
            {
                "id": "mvista_011",
                "prompt": (
                    "A scatter plot shows the relationship between advertising spend ($k) and "
                    "revenue ($k) for 5 months:\n"
                    "(10, 85), (20, 140), (30, 195), (40, 250), (50, 310).\n"
                    "What is the approximate slope of the best-fit line (revenue per $1k of "
                    "advertising spend)?"
                ),
                "expected": 5.6,
                "unit": "$k revenue per $k spend",
                "approach_keywords": ["slope", "best-fit", "linear", "regression", "rise over run"],
            },
            # --- Histograms ---
            {
                "id": "mvista_012",
                "prompt": (
                    "A histogram shows the distribution of test scores in bins of width 10:\n"
                    "50-60: 5 students, 60-70: 12 students, 70-80: 20 students, "
                    "80-90: 15 students, 90-100: 8 students.\n"
                    "What is the median score? (Assume uniform distribution within each bin.) "
                    "Round to one decimal place."
                ),
                "expected": 75.5,
                "unit": "points",
                "approach_keywords": ["median", "cumulative", "midpoint", "bin", "frequency"],
            },
            {
                "id": "mvista_013",
                "prompt": (
                    "A histogram shows the ages of visitors at a museum over one day:\n"
                    "0-10: 8, 10-20: 14, 20-30: 22, 30-40: 35, 40-50: 28, 50-60: 18, 60+: 10.\n"
                    "Total visitors = 135. What percentage of visitors are aged 30-50?"
                ),
                "expected": 46.67,
                "unit": "%",
                "approach_keywords": ["percent", "total", "divide", "age range", "frequency"],
            },
            # --- Tables ---
            {
                "id": "mvista_014",
                "prompt": (
                    "A table shows quarterly profit margins (%) for three divisions:\n"
                    "         Q1    Q2    Q3    Q4\n"
                    "Div A:  12.5  14.0  11.0  15.5\n"
                    "Div B:   8.0   9.5  10.0   7.5\n"
                    "Div C:  20.0  18.5  22.0  19.5\n"
                    "What is the overall average profit margin across all three divisions "
                    "and all four quarters? Round to two decimal places."
                ),
                "expected": 13.96,
                "unit": "%",
                "approach_keywords": ["average", "mean", "sum", "divide", "margin"],
            },
            {
                "id": "mvista_015",
                "prompt": (
                    "A table shows the number of items produced and defective items per day "
                    "over five days:\n"
                    "Day 1: produced=500, defective=10\n"
                    "Day 2: produced=450, defective=9\n"
                    "Day 3: produced=520, defective=15\n"
                    "Day 4: produced=480, defective=8\n"
                    "Day 5: produced=510, defective=12\n"
                    "What is the overall defect rate as a percentage? Round to two decimal places."
                ),
                "expected": 2.24,
                "unit": "%",
                "approach_keywords": ["defect rate", "total", "divide", "percent", "ratio"],
            },
            # --- Mixed / Multi-step ---
            {
                "id": "mvista_016",
                "prompt": (
                    "A combo chart shows monthly website traffic (bar, in thousands of visits) "
                    "and conversion rate (line, in %) for six months:\n"
                    "Jan: traffic=80k, conversion=2.5%\n"
                    "Feb: traffic=95k, conversion=3.0%\n"
                    "Mar: traffic=110k, conversion=2.8%\n"
                    "Apr: traffic=130k, conversion=3.5%\n"
                    "May: traffic=125k, conversion=3.2%\n"
                    "Jun: traffic=150k, conversion=4.0%\n"
                    "In which month were the actual number of conversions the highest, "
                    "and what was that number (rounded to the nearest whole number)?"
                ),
                "expected": 6000,
                "unit": "conversions",
                "approach_keywords": ["multiply", "conversion", "traffic", "highest", "June"],
            },
            {
                "id": "mvista_017",
                "prompt": (
                    "A waterfall chart shows cumulative profit/loss ($k) across departments: "
                    "Starting balance=100, Sales=+250, Cost of Goods=-180, "
                    "Marketing=-40, Operations=-30, Tax=-25, Ending balance=?.\n"
                    "What is the ending balance in $k?"
                ),
                "expected": 75.0,
                "unit": "$k",
                "approach_keywords": ["cumulative", "starting", "ending", "balance", "sum"],
            },
            {
                "id": "mvista_018",
                "prompt": (
                    "A stacked bar chart shows the number of medals won by four countries "
                    "at a sports event:\n"
                    "Country A: Gold=8, Silver=6, Bronze=4\n"
                    "Country B: Gold=5, Silver=9, Bronze=7\n"
                    "Country C: Gold=3, Silver=4, Bronze=10\n"
                    "Country D: Gold=6, Silver=3, Bronze=5\n"
                    "If Gold=3 points, Silver=2 points, Bronze=1 point, "
                    "which country has the highest point total and how many points do they have?"
                ),
                "expected": 56,
                "unit": "points",
                "approach_keywords": ["gold", "silver", "bronze", "points", "total", "highest"],
            },
            {
                "id": "mvista_019",
                "prompt": (
                    "A heat map shows average daily temperatures (°C) for four cities "
                    "across four seasons:\n"
                    "         Spring  Summer  Autumn  Winter\n"
                    "City 1:    15      32      18       5\n"
                    "City 2:    20      38      22       8\n"
                    "City 3:    10      28      14       2\n"
                    "City 4:    18      35      20       6\n"
                    "What is the range (max minus min) of the annual mean temperatures "
                    "across the four cities? Round to two decimal places."
                ),
                "expected": 7.0,
                "unit": "°C",
                "approach_keywords": ["mean", "annual", "range", "maximum", "minimum"],
            },
            {
                "id": "mvista_020",
                "prompt": (
                    "A bubble chart represents three data dimensions for five products: "
                    "price (x-axis, $), satisfaction score (y-axis, 1-10), "
                    "and sales volume (bubble size, units):\n"
                    "Product A: price=50, satisfaction=7.5, volume=2000\n"
                    "Product B: price=80, satisfaction=8.2, volume=1500\n"
                    "Product C: price=30, satisfaction=6.0, volume=3500\n"
                    "Product D: price=120, satisfaction=9.1, volume=800\n"
                    "Product E: price=65, satisfaction=7.8, volume=1800\n"
                    "What is the revenue-weighted average satisfaction score "
                    "(weight = price * volume)? Round to two decimal places."
                ),
                "expected": 7.31,
                "unit": "score",
                "approach_keywords": ["weighted", "average", "revenue", "multiply", "sum"],
            },
        ]

    # ------------------------------------------------------------------
    # Answer extraction helpers
    # ------------------------------------------------------------------

    def _extract_number(self, response: str) -> Optional[float]:
        """Extract the last prominent numeric answer from a response."""
        # 1. \boxed{N}
        boxed = re.search(r'\\boxed\{([\d,.\-]+)\}', response)
        if boxed:
            return self._parse_number(boxed.group(1))

        # 2. "answer is N" / "= N" patterns
        ans = re.search(
            r'(?:answer\s+is|answer:|the\s+answer[:\s]+|≈\s*|=\s*)([\d,.\-]+)',
            response,
            re.IGNORECASE,
        )
        if ans:
            val = self._parse_number(ans.group(1))
            if val is not None:
                return val

        # 3. Last standalone decimal / integer
        nums = re.findall(r'(?<!\w)([\d]+(?:[,\d]*)?(?:\.\d+)?)(?!\w)', response)
        if nums:
            for candidate in reversed(nums):
                val = self._parse_number(candidate)
                if val is not None:
                    return val

        return None

    def _parse_number(self, s: str) -> Optional[float]:
        """Convert a string (possibly with commas) to float."""
        try:
            return float(s.replace(',', '').strip())
        except ValueError:
            return None

    def _approach_score(self, response: str, keywords) -> float:
        """Return partial credit (0-0.5) based on approach keyword presence."""
        if not keywords:
            return 0.0
        response_lower = response.lower()
        matches = sum(1 for kw in keywords if kw.lower() in response_lower)
        return 0.5 * (matches / len(keywords))

    # ------------------------------------------------------------------
    # evaluate_response
    # ------------------------------------------------------------------

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score numeric answer with 1% tolerance; partial credit for right approach."""
        expected = float(prompt_data.get("expected", 0.0))
        approach_keywords = prompt_data.get("approach_keywords", [])

        extracted = self._extract_number(response)

        # Approach partial credit (max 0.5 when answer is wrong)
        approach = self._approach_score(response, approach_keywords)

        if extracted is None:
            return {
                "success": False,
                "score": round(approach * 0.5, 4),
                "metadata": {
                    "extracted_answer": None,
                    "expected_answer": expected,
                    "unit": prompt_data.get("unit", ""),
                    "reason": "no numeric answer found",
                    "approach_score": approach,
                },
            }

        # Check within 1% relative tolerance (or 0.01 absolute for near-zero)
        if abs(expected) < 1e-9:
            within_tolerance = abs(extracted) < 0.01
        else:
            within_tolerance = abs(extracted - expected) / abs(expected) <= 0.01

        if within_tolerance:
            score = 1.0
            success = True
        else:
            # Partial credit: approach quality (up to 0.5)
            score = round(approach * 0.5, 4)
            success = False

        return {
            "success": success,
            "score": score,
            "metadata": {
                "extracted_answer": extracted,
                "expected_answer": expected,
                "unit": prompt_data.get("unit", ""),
                "within_tolerance": within_tolerance,
                "relative_error": (
                    abs(extracted - expected) / abs(expected)
                    if abs(expected) >= 1e-9
                    else None
                ),
                "approach_score": approach,
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are an expert data analyst and mathematician. "
            "You will be given a description of a chart, graph, or table along with "
            "a quantitative question. Read the data carefully, show your working "
            "step by step, and state the final numeric answer clearly."
        )
