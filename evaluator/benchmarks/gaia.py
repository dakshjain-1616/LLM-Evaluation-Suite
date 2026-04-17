"""GAIA benchmark - General AI assistant tasks with multi-step reasoning and simulated web access."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class GAIABenchmark(Benchmark):
    """GAIA - General AI assistant benchmark with verifiable answers."""

    def __init__(self):
        config = BenchmarkConfig(
            name="gaia",
            description="Multi-step reasoning tasks with simulated search results; specific verifiable answers",
            category="agent",
            version="1.0",
            timeout=90,
            max_tokens=2048,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load GAIA-style tasks with inline search/tool context and specific verifiable answers."""
        self.prompts = [
            {
                "id": "gaia_001",
                "prompt": (
                    "You searched for 'population of Tokyo 2023' and found:\n"
                    "Source: Tokyo Metropolitan Government (2023): 'As of January 1, 2023, the population "
                    "of Tokyo Metropolis is 13,988,129.'\n"
                    "Source: Worldometers (2023): 'Tokyo population 2023: 13.96 million (Tokyo Metropolis).'\n\n"
                    "Question: What is the population of Tokyo Metropolis as of January 1, 2023, "
                    "according to the Tokyo Metropolitan Government? Give the exact number."
                ),
                "expected": "13988129",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_002",
                "prompt": (
                    "You searched for 'tallest building in the world 2024' and found:\n"
                    "Source: CTBUH (Council on Tall Buildings): 'The Burj Khalifa in Dubai, UAE, remains "
                    "the world's tallest building at 828 meters (2,717 feet) as of 2024.'\n"
                    "Source: Wikipedia: 'Burj Khalifa, completed in 2010, stands 828 m tall.'\n\n"
                    "Question: How tall is the world's tallest building in meters?"
                ),
                "expected": "828",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_003",
                "prompt": (
                    "You searched for 'boiling point of water at sea level Celsius' and found:\n"
                    "Source: NIST Chemistry WebBook: 'Water boils at 100°C (212°F) at standard atmospheric "
                    "pressure (101.325 kPa) at sea level.'\n"
                    "Source: Khan Academy: 'The boiling point of water at sea level is 100 degrees Celsius.'\n\n"
                    "Question: At what temperature in degrees Celsius does water boil at sea level?"
                ),
                "expected": "100",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_004",
                "prompt": (
                    "You searched for 'speed of light in meters per second exact' and found:\n"
                    "Source: NIST: 'The speed of light in a vacuum is exactly 299,792,458 meters per second "
                    "(by definition since 1983).'\n"
                    "Source: NASA: 'Light travels at 299,792,458 m/s in a vacuum.'\n\n"
                    "Question: What is the exact speed of light in a vacuum in meters per second?"
                ),
                "expected": "299792458",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_005",
                "prompt": (
                    "You searched for 'how many bones in the adult human body' and found:\n"
                    "Source: Gray's Anatomy (online): 'The adult human skeleton consists of 206 bones.'\n"
                    "Source: MedlinePlus (NIH): 'Adults have 206 bones. Babies are born with around 270–300 "
                    "bones, which fuse together over time.'\n\n"
                    "Question: How many bones does a typical adult human body have?"
                ),
                "expected": "206",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_006",
                "prompt": (
                    "You searched for 'chemical symbol for gold' and found:\n"
                    "Source: IUPAC Periodic Table: 'Gold: Symbol Au, Atomic Number 79, from Latin Aurum.'\n"
                    "Source: Royal Society of Chemistry: 'Gold (Au) is a chemical element with the symbol Au.'\n\n"
                    "Question: What is the chemical symbol for gold?"
                ),
                "expected": "Au",
                "answer_type": "text",
            },
            {
                "id": "gaia_007",
                "prompt": (
                    "You searched for 'who wrote Pride and Prejudice' and found:\n"
                    "Source: Project Gutenberg: 'Pride and Prejudice, by Jane Austen. "
                    "First published January 28, 1813.'\n"
                    "Source: British Library: 'Jane Austen published Pride and Prejudice in 1813. "
                    "It was originally titled First Impressions.'\n\n"
                    "Question: Who wrote Pride and Prejudice?"
                ),
                "expected": "Jane Austen",
                "answer_type": "text",
            },
            {
                "id": "gaia_008",
                "prompt": (
                    "You searched for 'distance from Earth to Moon km' and found:\n"
                    "Source: NASA Moon Fact Sheet: 'Mean distance from Earth to Moon: 384,400 km. "
                    "Perigee: 362,600 km. Apogee: 405,500 km.'\n"
                    "Source: ESA: 'The average Earth-Moon distance is approximately 384,400 kilometers.'\n\n"
                    "Question: What is the mean distance from the Earth to the Moon in kilometers?"
                ),
                "expected": "384400",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_009",
                "prompt": (
                    "You performed a multi-step calculation task:\n"
                    "Search result 1 – 'GDP of Germany 2023 USD': "
                    "IMF World Economic Outlook 2023: 'Germany GDP: $4.430 trillion (2023).'\n"
                    "Search result 2 – 'GDP of France 2023 USD': "
                    "IMF World Economic Outlook 2023: 'France GDP: $3.049 trillion (2023).'\n"
                    "Search result 3 – 'GDP of Italy 2023 USD': "
                    "IMF World Economic Outlook 2023: 'Italy GDP: $2.187 trillion (2023).'\n\n"
                    "Question: What is the combined GDP (in trillions of USD, rounded to 3 decimal places) "
                    "of Germany, France, and Italy in 2023 according to the IMF?"
                ),
                "expected": "9.666",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_010",
                "prompt": (
                    "You searched for 'in what year was the Eiffel Tower completed' and found:\n"
                    "Source: Official Eiffel Tower website: 'Construction began in January 1887 and was "
                    "completed on March 31, 1889. It was inaugurated on May 6, 1889.'\n"
                    "Source: Encyclopedia Britannica: 'The Eiffel Tower was completed in 1889.'\n\n"
                    "Question: In what year was the Eiffel Tower completed?"
                ),
                "expected": "1889",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_011",
                "prompt": (
                    "You searched for 'atomic number of carbon' and found:\n"
                    "Source: IUPAC Periodic Table: 'Carbon: Symbol C, Atomic Number 6, Atomic Weight 12.011.'\n"
                    "Source: WebElements: 'Carbon is element 6 on the periodic table.'\n\n"
                    "Question: What is the atomic number of carbon?"
                ),
                "expected": "6",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_012",
                "prompt": (
                    "You performed the following research:\n"
                    "Search: 'how many planets in solar system' → "
                    "NASA: 'As of 2006, the solar system has 8 planets: Mercury, Venus, Earth, Mars, "
                    "Jupiter, Saturn, Uranus, and Neptune. Pluto was reclassified as a dwarf planet.'\n\n"
                    "Question: How many planets are in the solar system according to the current IAU definition?"
                ),
                "expected": "8",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_013",
                "prompt": (
                    "You searched for 'what country has the largest land area' and found:\n"
                    "Source: CIA World Factbook: 'Russia: 17,098,242 sq km – the world's largest country by area.'\n"
                    "Source: UN Statistics: 'Russian Federation has a total area of 17,098,242 km².'\n\n"
                    "Question: What country has the largest land area in the world?"
                ),
                "expected": "Russia",
                "answer_type": "text",
            },
            {
                "id": "gaia_014",
                "prompt": (
                    "You searched for 'melting point of iron Celsius' and found:\n"
                    "Source: Engineering Toolbox: 'Iron (Fe) melts at 1538°C (2800°F) at atmospheric pressure.'\n"
                    "Source: NIST WebBook: 'Iron melting point: 1538 °C.'\n\n"
                    "Question: What is the melting point of iron in degrees Celsius?"
                ),
                "expected": "1538",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_015",
                "prompt": (
                    "You searched for 'when did World War II end' and found:\n"
                    "Source: History.com: 'World War II ended on September 2, 1945, when Japan formally "
                    "surrendered aboard the USS Missouri in Tokyo Bay.'\n"
                    "Source: National WWII Museum: 'V-J Day (Victory over Japan) is September 2, 1945 – "
                    "the official end of World War II.'\n\n"
                    "Question: On what date did World War II officially end (V-J Day)?"
                ),
                "expected": "September 2, 1945",
                "answer_type": "text",
            },
            {
                "id": "gaia_016",
                "prompt": (
                    "You searched for 'what is the square root of 144' and calculated:\n"
                    "Mathematical computation: sqrt(144) = 12 (since 12 × 12 = 144).\n"
                    "Verified via WolframAlpha: 'sqrt(144) = 12'\n\n"
                    "Question: What is the square root of 144?"
                ),
                "expected": "12",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_017",
                "prompt": (
                    "You searched for 'capital of Australia' and found:\n"
                    "Source: Australian Government: 'Canberra is the capital city of Australia. "
                    "It has been the national capital since 1913.'\n"
                    "Source: Encyclopedia Britannica: 'Canberra, capital of the Commonwealth of Australia.'\n\n"
                    "Question: What is the capital city of Australia?"
                ),
                "expected": "Canberra",
                "answer_type": "text",
            },
            {
                "id": "gaia_018",
                "prompt": (
                    "You performed a multi-step research task:\n"
                    "Step 1 – Search 'average human heart rate BPM': "
                    "AHA (American Heart Association): 'Normal resting heart rate for adults: 60–100 BPM.'\n"
                    "Step 2 – Search 'how many beats per day at 70 BPM': "
                    "Calculation: 70 beats/min × 60 min/hr × 24 hr/day = 100,800 beats/day.\n\n"
                    "Question: How many times does the average adult heart beat per day, "
                    "assuming a resting rate of 70 BPM?"
                ),
                "expected": "100800",
                "answer_type": "numeric",
            },
            {
                "id": "gaia_019",
                "prompt": (
                    "You searched for 'who invented the telephone' and found:\n"
                    "Source: Smithsonian Institution: 'Alexander Graham Bell is credited with inventing "
                    "the first practical telephone and was awarded the first patent for it in 1876 (US Patent 174,465).'\n"
                    "Source: Library of Congress: 'Alexander Graham Bell patented the telephone on March 7, 1876.'\n\n"
                    "Question: Who is credited with inventing the telephone and in what year was the patent granted?"
                ),
                "expected": "Alexander Graham Bell, 1876",
                "answer_type": "text",
            },
            {
                "id": "gaia_020",
                "prompt": (
                    "You performed a compound research task:\n"
                    "Search 1 – 'how many minutes in a year': "
                    "Result: 365 days × 24 hours × 60 minutes = 525,600 minutes (non-leap year).\n"
                    "Search 2 – 'is 2024 a leap year': "
                    "Result: 'Yes, 2024 is a leap year (366 days).'\n"
                    "Calculation: 366 × 24 × 60 = 527,040 minutes.\n\n"
                    "Question: How many minutes are there in the year 2024?"
                ),
                "expected": "527040",
                "answer_type": "numeric",
            },
        ]

    def _normalize_answer(self, text: str) -> str:
        """Strip whitespace, commas from numbers, and lowercase for comparison."""
        text = text.strip()
        # Remove commas used as thousands separators in numeric strings
        text = re.sub(r"(\d),(\d)", r"\1\2", text)
        return text.lower()

    def _numeric_match(self, response: str, expected: str, tolerance: float = 0.001) -> bool:
        """Check whether the expected numeric value appears in the response."""
        # Normalize expected
        exp_clean = expected.replace(",", "").strip()
        try:
            exp_val = float(exp_clean)
        except ValueError:
            return False

        # Find all numeric candidates in response
        candidates = re.findall(r"\d[\d,]*\.?\d*", response.replace(",", ""))
        for cand in candidates:
            try:
                cand_val = float(cand)
                if exp_val == 0:
                    if cand_val == 0:
                        return True
                elif abs(cand_val - exp_val) / abs(exp_val) <= tolerance:
                    return True
            except ValueError:
                continue
        return False

    def _text_match(self, response: str, expected: str) -> bool:
        """Check whether all significant tokens of expected appear in the response."""
        response_lower = response.lower()
        expected_lower = expected.lower()

        # Direct substring match
        if expected_lower in response_lower:
            return True

        # Token-based match for multi-word answers
        tokens = [t for t in re.split(r"[\s,;]+", expected_lower) if len(t) > 1]
        if not tokens:
            return False
        matched = sum(1 for t in tokens if t in response_lower)
        return (matched / len(tokens)) >= 0.85

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Evaluate a GAIA response.

        Scoring:
          1.0 - correct final answer (exact numeric match within 0.1% or exact text match)
          0.0 - incorrect
        """
        expected: str = str(prompt_data.get("expected", ""))
        answer_type: str = prompt_data.get("answer_type", "text")
        response_stripped = response.strip()

        if not response_stripped:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"reason": "empty_response"},
            }

        if answer_type == "numeric":
            correct = self._numeric_match(response, expected)
        else:
            correct = self._text_match(response, expected)

        return {
            "success": correct,
            "score": 1.0 if correct else 0.0,
            "metadata": {
                "expected": expected,
                "answer_type": answer_type,
                "match": correct,
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are a general-purpose AI assistant. You have access to the provided search results "
            "and tool outputs. Reason step-by-step over the evidence and give a precise, verifiable "
            "final answer. State your final answer clearly and concisely — it should be a specific "
            "number, date, name, or short phrase."
        )
