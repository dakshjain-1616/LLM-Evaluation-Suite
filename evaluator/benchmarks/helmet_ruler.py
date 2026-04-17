"""HELMET Ruler benchmark - long-context retrieval and needle-in-haystack tasks."""

from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


_FILLER_A = (
    "The history of the public library stretches back to ancient civilizations. "
    "In Mesopotamia, clay tablets inscribed with cuneiform script were stored in "
    "temple archives accessible to scribes and scholars. The Library of Alexandria, "
    "founded in the third century BCE, represented perhaps the most ambitious attempt "
    "in the ancient world to collect all human knowledge in one place. Scholars from "
    "across the Mediterranean traveled to Alexandria to consult its hundreds of thousands "
    "of scrolls. The institution employed dedicated librarians whose job was to catalogue, "
    "copy, and preserve texts. Medieval European monasteries continued this tradition, "
    "maintaining scriptoria where monks hand-copied manuscripts to prevent their loss. "
    "The invention of the printing press by Gutenberg in the fifteenth century transformed "
    "the economics of book production, enabling broader distribution of texts. Public "
    "lending libraries began to emerge in eighteenth-century Britain and America, driven "
    "by a belief that an educated populace was essential to democratic self-governance. "
    "Andrew Carnegie funded the construction of more than 2,500 library buildings between "
    "1883 and 1929, cementing the public library as a civic institution across the "
    "English-speaking world. Today, public libraries lend not only books but also digital "
    "media, host community events, and provide internet access to those who might otherwise "
    "lack it. The role of the library continues to evolve in the digital age."
)

_FILLER_B = (
    "Ocean currents are large-scale movements of seawater driven by a combination of "
    "wind, the Earth's rotation, differences in water density caused by temperature and "
    "salinity, and the shape of ocean basins. The global system of ocean circulation is "
    "sometimes called the ocean conveyor belt or thermohaline circulation. Cold, salty, "
    "dense water sinks in the North Atlantic and flows southward along the ocean floor, "
    "while warmer surface water flows northward to replace it. This circulation pattern "
    "has a profound effect on global climate, transporting heat from the tropics toward "
    "the poles. The Gulf Stream, a powerful surface current, carries warm water from the "
    "Gulf of Mexico northeastward across the Atlantic, moderating the climates of Western "
    "Europe. Surface currents are primarily driven by prevailing winds and are influenced "
    "by the Coriolis effect, which deflects moving water to the right in the Northern "
    "Hemisphere and to the left in the Southern Hemisphere. Upwelling zones, where cold "
    "nutrient-rich water rises to the surface, are among the most productive marine "
    "ecosystems in the world. The Humboldt Current off the west coast of South America "
    "supports enormous fisheries. Climate scientists are monitoring whether global warming "
    "could weaken thermohaline circulation, with potentially dramatic consequences for "
    "regional climates around the Atlantic basin."
)

_FILLER_C = (
    "The development of modern cryptography has roots in ancient substitution ciphers, "
    "but the field was transformed in the twentieth century by mathematics and computing. "
    "During World War II the Enigma machine, used by the German military to encrypt "
    "communications, was eventually broken by British codebreakers at Bletchley Park, "
    "a feat that is widely believed to have shortened the war by several years. The "
    "introduction of public-key cryptography in the 1970s by Diffie, Hellman, Rivest, "
    "Shamir, and Adleman was revolutionary: for the first time it became possible to "
    "communicate securely over an untrusted channel without first exchanging a secret key "
    "in person. The RSA algorithm, based on the difficulty of factoring large integers, "
    "became the foundation of secure internet commerce. Modern cryptographic systems must "
    "defend against increasingly powerful adversaries, including nation-state actors with "
    "access to supercomputers. Post-quantum cryptography is an active research area aimed "
    "at developing algorithms that would remain secure even against a large-scale quantum "
    "computer. The National Institute of Standards and Technology finalized its first set "
    "of post-quantum cryptographic standards in 2024."
)

_FILLER_D = (
    "Urban planning as a formal discipline emerged in the late nineteenth and early "
    "twentieth centuries as industrial cities faced problems of overcrowding, sanitation, "
    "and traffic congestion. Pioneering figures like Ebenezer Howard proposed the garden "
    "city concept, advocating for planned communities that combined the advantages of "
    "city and countryside. The modernist movement, championed by architects such as "
    "Le Corbusier, favored high-rise towers set in open green space and strict separation "
    "of land uses into residential, commercial, and industrial zones. These ideas heavily "
    "influenced postwar housing projects across Europe and North America, many of which "
    "later became associated with social problems. Reaction against modernist orthodoxy "
    "gave rise to the New Urbanism movement, which advocated for walkable, mixed-use "
    "neighborhoods designed at a human scale. Contemporary urban planning grapples with "
    "challenges including climate adaptation, equitable access to housing and transit, "
    "and the effects of remote work on city centers. Transit-oriented development, which "
    "concentrates housing and commerce around public transport nodes, has become an "
    "influential model for sustainable urban growth."
)


def _build_needle_prompt(filler_before: str, needle_sentence: str, filler_after: str, question: str) -> str:
    passage = filler_before.strip() + " " + needle_sentence.strip() + " " + filler_after.strip()
    return f"Read the following passage carefully, then answer the question.\n\n---\n{passage}\n---\n\nQuestion: {question}"


class HELMETBenchmark(Benchmark):
    """HELMET Ruler - long-context needle-in-haystack and multi-document retrieval benchmark."""

    def __init__(self):
        config = BenchmarkConfig(
            name="helmet_ruler",
            description="Long-context retrieval: needle-in-haystack and multi-document tasks",
            category="long_context",
            version="1.0",
            timeout=120,
            max_tokens=256,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- Needle-in-haystack prompts (1-12) ---
            {
                "id": "helmet_001",
                "prompt": _build_needle_prompt(
                    _FILLER_A,
                    "The secret project codename assigned to the mission was AZURE FALCON.",
                    _FILLER_B,
                    "What was the secret project codename mentioned in the passage?",
                ),
                "needle_facts": ["azure falcon"],
            },
            {
                "id": "helmet_002",
                "prompt": _build_needle_prompt(
                    _FILLER_B,
                    "The exact population of the island colony in 1847 was recorded as 14,392 inhabitants.",
                    _FILLER_C,
                    "What was the population of the island colony in 1847 according to the passage?",
                ),
                "needle_facts": ["14,392", "14392"],
            },
            {
                "id": "helmet_003",
                "prompt": _build_needle_prompt(
                    _FILLER_C,
                    "Dr. Elena Vasquez discovered that the melting point of compound X-77 is 312 degrees Celsius.",
                    _FILLER_D,
                    "What is the melting point of compound X-77 according to the passage?",
                ),
                "needle_facts": ["312"],
            },
            {
                "id": "helmet_004",
                "prompt": _build_needle_prompt(
                    _FILLER_D,
                    "The treaty was signed on March 4, 1923, in the city of Lausanne.",
                    _FILLER_A,
                    "On what date and in which city was the treaty signed according to the passage?",
                ),
                "needle_facts": ["march 4", "1923", "lausanne"],
            },
            {
                "id": "helmet_005",
                "prompt": _build_needle_prompt(
                    _FILLER_A + " " + _FILLER_B,
                    "The password to the encrypted vault is: SILVER-MOON-7749.",
                    _FILLER_C,
                    "What is the password to the encrypted vault mentioned in the passage?",
                ),
                "needle_facts": ["silver-moon-7749", "silver moon 7749"],
            },
            {
                "id": "helmet_006",
                "prompt": _build_needle_prompt(
                    _FILLER_B + " " + _FILLER_C,
                    "The winning bid for the rare manuscript was $2,340,000.",
                    _FILLER_D,
                    "What was the winning bid for the rare manuscript?",
                ),
                "needle_facts": ["2,340,000", "2340000", "2.34 million"],
            },
            {
                "id": "helmet_007",
                "prompt": _build_needle_prompt(
                    _FILLER_C,
                    "Agent Thompson's cover identity was that of a Swiss watchmaker named Henri Bouchard.",
                    _FILLER_A + " " + _FILLER_B,
                    "What was Agent Thompson's cover identity according to the passage?",
                ),
                "needle_facts": ["henri bouchard", "swiss watchmaker"],
            },
            {
                "id": "helmet_008",
                "prompt": _build_needle_prompt(
                    _FILLER_D + " " + _FILLER_A,
                    "The final coordinates of the shipwreck were 41.2°N, 28.7°E.",
                    _FILLER_B,
                    "What were the final coordinates of the shipwreck?",
                ),
                "needle_facts": ["41.2", "28.7"],
            },
            {
                "id": "helmet_009",
                "prompt": _build_needle_prompt(
                    _FILLER_A,
                    "The experimental drug reduced tumor size by exactly 73% in the clinical trial.",
                    _FILLER_C + " " + _FILLER_D,
                    "By what percentage did the experimental drug reduce tumor size in the clinical trial?",
                ),
                "needle_facts": ["73%", "73 percent"],
            },
            {
                "id": "helmet_010",
                "prompt": _build_needle_prompt(
                    _FILLER_B + " " + _FILLER_D,
                    "The emergency shutdown code for reactor unit 4 is OMEGA-DELTA-9.",
                    _FILLER_C,
                    "What is the emergency shutdown code for reactor unit 4?",
                ),
                "needle_facts": ["omega-delta-9", "omega delta 9"],
            },
            {
                "id": "helmet_011",
                "prompt": _build_needle_prompt(
                    _FILLER_C + " " + _FILLER_A,
                    "Professor Nakamura's lab is located in Building 17, Room 204.",
                    _FILLER_D,
                    "Where is Professor Nakamura's lab located according to the passage?",
                ),
                "needle_facts": ["building 17", "room 204"],
            },
            {
                "id": "helmet_012",
                "prompt": _build_needle_prompt(
                    _FILLER_D,
                    "The archaeological dig uncovered a bronze artifact dated to 2,800 BCE, labeled item KV-33.",
                    _FILLER_A + " " + _FILLER_B + " " + _FILLER_C,
                    "What artifact was uncovered in the archaeological dig and what is its label?",
                ),
                "needle_facts": ["2,800 bce", "kv-33", "bronze"],
            },
            # --- Multi-document summarization / retrieval prompts (13-20) ---
            {
                "id": "helmet_013",
                "prompt": (
                    "You are given summaries of three research papers. Identify the single finding that "
                    "appears in ALL THREE papers.\n\n"
                    "Paper 1: Researchers studied 500 patients over five years and found that daily aerobic "
                    "exercise of at least 30 minutes was associated with a 40% reduction in cardiovascular "
                    "events. They also noted improved sleep quality and reduced anxiety scores.\n\n"
                    "Paper 2: A meta-analysis of 22 randomized controlled trials concluded that regular "
                    "aerobic exercise significantly lowers the risk of heart disease. The study highlighted "
                    "that even moderate intensity activities like brisk walking produced measurable benefits.\n\n"
                    "Paper 3: An observational cohort study followed 12,000 adults and determined that "
                    "physically active individuals had substantially lower rates of cardiovascular mortality. "
                    "Aerobic exercise was identified as the most protective activity type.\n\n"
                    "What single finding is shared across all three papers?"
                ),
                "needle_facts": ["aerobic exercise", "cardiovascular", "heart"],
            },
            {
                "id": "helmet_014",
                "prompt": (
                    "Read the following two product reviews and identify the specific feature that BOTH "
                    "reviewers criticize.\n\n"
                    "Review 1: I bought this laptop expecting great battery life given the marketing claims. "
                    "The performance is excellent and the display is gorgeous. However, the keyboard is "
                    "absolutely terrible—the keys are mushy and have no tactile feedback whatsoever. "
                    "I also found the speakers to be surprisingly good.\n\n"
                    "Review 2: Decent machine overall but there are issues. The SSD speed is impressive "
                    "and boot times are fast. My main complaint is the keyboard: the travel is too shallow "
                    "and I keep making typos. The trackpad is also a bit small but workable.\n\n"
                    "What feature do both reviewers criticize?"
                ),
                "needle_facts": ["keyboard"],
            },
            {
                "id": "helmet_015",
                "prompt": (
                    "Below are excerpts from three historical documents. Find the specific year mentioned "
                    "in all three documents.\n\n"
                    "Document A (city council minutes): 'The new waterworks project was approved in 1887 "
                    "and the aqueduct construction began the following spring. The council also addressed "
                    "road maintenance issues and allocated funds for a new school building.'\n\n"
                    "Document B (newspaper archive): 'Looking back at our city's proud history, the "
                    "waterworks inaugurated in 1887 transformed public health. The decade also saw "
                    "the arrival of the first telegraph line and the founding of the chamber of commerce.'\n\n"
                    "Document C (engineering journal): 'Case study: the 1887 municipal waterworks "
                    "project remains an exemplary model of Victorian civil engineering. The system "
                    "served the city for over 60 years without major overhaul.'\n\n"
                    "What year appears in all three documents?"
                ),
                "needle_facts": ["1887"],
            },
            {
                "id": "helmet_016",
                "prompt": (
                    "Read the following two meeting transcripts and identify the action item that was "
                    "assigned to Sarah in BOTH meetings.\n\n"
                    "Meeting 1 Transcript (excerpt): '...James will finalize the budget proposal by "
                    "Friday. Sarah is responsible for updating the client contact database before the "
                    "end of the month. Tom will coordinate with the logistics team on the shipment. "
                    "We agreed to reconvene next Tuesday...'\n\n"
                    "Meeting 2 Transcript (excerpt): '...The marketing deck needs revision—Marcus will "
                    "handle that. Sarah, please make sure the client contact database is fully updated "
                    "before the board presentation. Legal review is assigned to Priya. Next steps will "
                    "be confirmed via email...'\n\n"
                    "What action item was assigned to Sarah in both meetings?"
                ),
                "needle_facts": ["client contact database", "database"],
            },
            {
                "id": "helmet_017",
                "prompt": (
                    "You have three employee records. Find the employee whose start date is the same "
                    "in all three data sources.\n\n"
                    "HR System export: 'Employee ID 4421, Name: Marco Delgado, Department: Engineering, "
                    "Start Date: 2019-06-10. Employee ID 4422, Name: Lisa Park, Department: Marketing, "
                    "Start Date: 2021-03-15.'\n\n"
                    "Payroll System: 'Pay record — Delgado, Marco: tenure start 10 June 2019. "
                    "Park, Lisa: tenure start 15 March 2021.'\n\n"
                    "Badge Access Log: 'First badge activation — Delgado M.: 2019-06-10. Park L.: "
                    "2021-03-15.'\n\n"
                    "What is Marco Delgado's start date as recorded consistently across all three sources?"
                ),
                "needle_facts": ["2019-06-10", "june 10 2019", "june 10, 2019", "10 june 2019"],
            },
            {
                "id": "helmet_018",
                "prompt": (
                    "Read the two scientific abstracts below and identify the specific chemical compound "
                    "that both studies focus on.\n\n"
                    "Abstract 1: 'This study investigates the anti-inflammatory properties of quercetin, "
                    "a flavonoid found in many fruits and vegetables. We measured cytokine levels in "
                    "50 human subjects and found significant reductions in IL-6 following quercetin "
                    "supplementation over eight weeks. Side effects were minimal.'\n\n"
                    "Abstract 2: 'Building on prior literature, we examined the bioavailability of "
                    "quercetin in combination with piperine. Our in vitro and in vivo results confirm "
                    "that piperine substantially increases quercetin absorption and potentiates its "
                    "antioxidant activity. Implications for dietary supplement formulation are discussed.'\n\n"
                    "What specific compound is the focus of both studies?"
                ),
                "needle_facts": ["quercetin"],
            },
            {
                "id": "helmet_019",
                "prompt": (
                    "The following is a long set of footnotes from a legal brief. Find the case name "
                    "cited more than once.\n\n"
                    "Footnote 1: See generally Smith v. Jones, 342 U.S. 100 (1952).\n"
                    "Footnote 2: For the standard of review, see Davis v. Monroe County Board of Education, "
                    "526 U.S. 629 (1999).\n"
                    "Footnote 3: The court applied strict scrutiny as outlined in Smith v. Jones, "
                    "342 U.S. 100 (1952).\n"
                    "Footnote 4: Cf. Gonzaga University v. Doe, 536 U.S. 273 (2002).\n"
                    "Footnote 5: The damages analysis follows Burlington Industries v. Ellerth, "
                    "524 U.S. 742 (1998).\n"
                    "Footnote 6: As noted in Davis v. Monroe County Board of Education, supra note 2, "
                    "the deliberate indifference standard applies.\n"
                    "Footnote 7: The procedural history mirrors that in Gebser v. Lago Vista Independent "
                    "School District, 524 U.S. 274 (1998).\n\n"
                    "Which case name is cited in more than one footnote?"
                ),
                "needle_facts": ["smith v. jones", "davis v. monroe"],
            },
            {
                "id": "helmet_020",
                "prompt": (
                    "Read the following passage describing a supply chain audit and answer the question "
                    "that follows.\n\n"
                    + _FILLER_D
                    + " During the audit, inspectors flagged Supplier ID SV-8821 as the sole vendor "
                    "whose delivery accuracy fell below the contractual threshold of 95%, recording "
                    "only 81% on-time delivery across the review period. All other suppliers met or "
                    "exceeded the threshold. "
                    + _FILLER_A
                    + "\n\nQuestion: Which supplier ID was flagged for falling below the delivery accuracy "
                    "threshold, and what was their recorded on-time delivery rate?"
                ),
                "needle_facts": ["sv-8821", "81%", "81 percent"],
            },
        ]

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score 1.0 if any needle fact is found in the response, 0.0 otherwise."""
        needle_facts: List[str] = prompt_data.get("needle_facts", [])
        response_lower = response.lower()

        def fact_found(fact: str) -> bool:
            return fact.lower() in response_lower

        found = any(fact_found(f) for f in needle_facts)
        matched = [f for f in needle_facts if fact_found(f)]

        return {
            "success": found,
            "score": 1.0 if found else 0.0,
            "metadata": {
                "needle_facts": needle_facts,
                "matched_facts": matched,
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are a careful reader. Answer questions based solely on the information "
            "provided in the passage. Be concise and precise."
        )
