"""FRAMES benchmark - multi-hop retrieval and reasoning over multiple documents."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class FRAMESBenchmark(Benchmark):
    """FRAMES - multi-hop retrieval + reasoning over multiple passages."""

    def __init__(self):
        config = BenchmarkConfig(
            name="frames",
            description="Multi-hop retrieval and reasoning requiring synthesis across 2+ documents",
            category="rag",
            version="1.0",
            timeout=90,
            max_tokens=1024,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load 20 multi-hop retrieval + reasoning prompts."""
        self.prompts = [
            {
                "id": "frames_001",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Eiffel Tower was constructed between 1887 and 1889 as the entrance arch "
                    "for the 1889 World's Fair. Its designer, Gustave Eiffel, also oversaw the internal "
                    "structural engineering of the Statue of Liberty. The tower stands 330 metres tall "
                    "including its broadcast antenna.\n\n"
                    "Passage B: The Statue of Liberty was a gift from France to the United States, dedicated "
                    "on October 28, 1886. The statue's copper exterior was crafted by sculptor Frédéric Auguste "
                    "Bartholdi. The internal iron framework, essential for the statue's stability, required "
                    "expertise from a renowned structural engineer.\n\n"
                    "Passage C: The 1889 World's Fair, held in Paris, commemorated the centennial of the French "
                    "Revolution. It attracted over 32 million visitors and showcased industrial achievements. "
                    "Several landmark structures were commissioned for the event.\n\n"
                    "Question: What structural engineer worked on both the Statue of Liberty and a landmark built "
                    "for the 1889 World's Fair, and what was that landmark?"
                ),
                "expected": "Gustave Eiffel worked on both. He designed the internal framework of the Statue of Liberty and constructed the Eiffel Tower for the 1889 World's Fair.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B"],
            },
            {
                "id": "frames_002",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Marie Curie was born in Warsaw, Poland, in 1867. She moved to Paris at age 24 "
                    "to study at the University of Paris. She is famous for her research on radioactivity.\n\n"
                    "Passage B: The Nobel Prize in Physics 1903 was awarded jointly to Henri Becquerel and "
                    "Pierre Curie and Marie Curie. This was in recognition of the extraordinary services they "
                    "rendered by their joint researches on the radiation phenomena discovered by Becquerel.\n\n"
                    "Passage C: In 1911 the Nobel Prize in Chemistry was awarded to Marie Curie for the "
                    "discovery of radium and polonium. With this award she became the first person to win "
                    "Nobel Prizes in two different scientific disciplines.\n\n"
                    "Question: In which city did Marie Curie study, and what unique distinction did she earn "
                    "across her two Nobel Prize wins?"
                ),
                "expected": "Marie Curie studied in Paris and became the first person to win Nobel Prizes in two different scientific disciplines (Physics and Chemistry).",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "C"],
            },
            {
                "id": "frames_003",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Amazon River discharges approximately 209,000 cubic metres of water per "
                    "second into the Atlantic Ocean, accounting for about 20% of all freshwater entering the "
                    "world's oceans. Its basin spans nine countries.\n\n"
                    "Passage B: Brazil contains approximately 60% of the Amazon rainforest. The forest plays "
                    "a critical role in regulating the global climate by absorbing carbon dioxide. "
                    "Deforestation has accelerated since the 1970s.\n\n"
                    "Passage C: The Atlantic Ocean is the second-largest ocean on Earth, covering roughly "
                    "106 million square kilometres. It separates the Americas from Europe and Africa and "
                    "receives freshwater inflows from numerous major rivers.\n\n"
                    "Question: Approximately what fraction of the Atlantic Ocean's freshwater input comes from "
                    "a single river that runs predominantly through Brazil?"
                ),
                "expected": "About 20% of all freshwater entering the world's oceans (and thus the Atlantic) comes from the Amazon River, which runs predominantly through Brazil.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B"],
            },
            {
                "id": "frames_004",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Nikola Tesla was born in 1856 in Smiljan, in present-day Croatia. He emigrated "
                    "to the United States in 1884 and worked briefly for Thomas Edison before striking out on "
                    "his own. Tesla held around 300 patents.\n\n"
                    "Passage B: The War of Currents was a series of events in the late 1880s surrounding the "
                    "introduction of competing electrical transmission systems. Edison championed direct current "
                    "(DC), while George Westinghouse and Tesla advocated for alternating current (AC).\n\n"
                    "Passage C: Alternating current became the standard for electrical power distribution "
                    "worldwide because it can be easily transformed to higher voltages for long-distance "
                    "transmission, reducing energy losses significantly compared to direct current.\n\n"
                    "Question: Why did the electrical system championed by Tesla ultimately prevail over "
                    "Edison's system, and with whom did Tesla ally to promote it?"
                ),
                "expected": "Tesla's alternating current (AC) prevailed because it can be transformed to higher voltages for efficient long-distance transmission with fewer energy losses. Tesla allied with George Westinghouse to promote AC.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B", "C"],
            },
            {
                "id": "frames_005",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Mount Everest, located in the Himalayas on the border of Nepal and Tibet, "
                    "is the highest peak on Earth at 8,849 metres above sea level as measured in 2020.\n\n"
                    "Passage B: The first confirmed ascent of Mount Everest was made on May 29, 1953, by "
                    "Edmund Hillary of New Zealand and Tenzing Norgay, a Sherpa from Nepal. The expedition "
                    "was organised by the Joint Himalayan Committee.\n\n"
                    "Passage C: Tenzing Norgay had previously attempted Everest six times before 1953. "
                    "After the successful summit, he was awarded the George Medal by the United Kingdom and "
                    "the Star of Nepal by the Nepalese government.\n\n"
                    "Question: How many total Everest attempts did Tenzing Norgay make before and including "
                    "the first successful summit, and what was the elevation of the peak he finally reached?"
                ),
                "expected": "Tenzing Norgay made seven total attempts (six prior plus the successful 1953 climb). The peak stands at 8,849 metres above sea level.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "C"],
            },
            {
                "id": "frames_006",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The human genome contains approximately 3 billion base pairs of DNA organized "
                    "into 23 pairs of chromosomes. Only about 1.5% of the genome encodes proteins.\n\n"
                    "Passage B: The Human Genome Project was an international scientific research project "
                    "that ran from 1990 to 2003. Its goal was to map all the genes of the human genome. "
                    "It was declared complete in April 2003, the 50th anniversary of the discovery of DNA's "
                    "double-helix structure.\n\n"
                    "Passage C: James Watson and Francis Crick published their description of the double-helix "
                    "structure of DNA in April 1953 in Nature. Their work built significantly on X-ray "
                    "crystallography data produced by Rosalind Franklin.\n\n"
                    "Question: How long after the discovery of DNA's double-helix structure was the Human "
                    "Genome Project completed, and approximately how many base pairs were mapped?"
                ),
                "expected": "The Human Genome Project was completed exactly 50 years after the double-helix structure was described in 1953, i.e., in 2003. Approximately 3 billion base pairs were mapped.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B"],
            },
            {
                "id": "frames_007",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Black Death reached Europe around 1347 via merchant ships docking at "
                    "Sicilian ports. The epidemic killed an estimated 30–60% of Europe's total population "
                    "over the following years.\n\n"
                    "Passage B: The plague was caused by the bacterium Yersinia pestis, transmitted primarily "
                    "through the bites of fleas that lived on rats. The disease manifested as bubonic, "
                    "septicaemic, or pneumonic plague depending on how infection occurred.\n\n"
                    "Passage C: Europe's population in 1340, just before the Black Death, is estimated at "
                    "about 75 million people. Recovery to pre-plague population levels took approximately "
                    "150–200 years in most regions.\n\n"
                    "Question: Given Europe's pre-plague population, approximately how many people perished "
                    "from the Black Death at its upper estimated mortality rate, and what bacterium caused it?"
                ),
                "expected": "At the upper estimate of 60% mortality, approximately 45 million of the 75 million Europeans died. The bacterium responsible was Yersinia pestis.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_008",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Apollo 11 mission launched on July 16, 1969, carrying astronauts Neil "
                    "Armstrong, Buzz Aldrin, and Michael Collins. Armstrong and Aldrin landed on the Moon "
                    "on July 20, 1969.\n\n"
                    "Passage B: Michael Collins remained in lunar orbit aboard the Command Module Columbia "
                    "while his crewmates descended to the surface. He orbited the Moon 30 times over 21 hours, "
                    "out of radio contact with Earth during each far-side pass.\n\n"
                    "Passage C: Neil Armstrong's first words upon stepping onto the lunar surface were: "
                    "'That's one small step for [a] man, one giant leap for mankind.' Armstrong and Aldrin "
                    "spent approximately 21 hours and 36 minutes on the lunar surface in total.\n\n"
                    "Question: Which Apollo 11 crew member never landed on the Moon, and for how long was "
                    "the mission's lunar surface phase conducted by the other two astronauts?"
                ),
                "expected": "Michael Collins never landed on the Moon; he orbited in the Command Module. Armstrong and Aldrin spent approximately 21 hours and 36 minutes on the lunar surface.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B", "C"],
            },
            {
                "id": "frames_009",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: William Shakespeare was born in Stratford-upon-Avon in April 1564 and died "
                    "in April 1616 at the age of 52. He wrote approximately 39 plays, 154 sonnets, and "
                    "several longer poems.\n\n"
                    "Passage B: The Globe Theatre was built in 1599 by Shakespeare's playing company, the "
                    "Lord Chamberlain's Men. It could hold up to 3,000 spectators and burned down in 1613 "
                    "when a theatrical cannon misfired during a performance of Henry VIII.\n\n"
                    "Passage C: Shakespeare is often credited with inventing over 1,700 words that entered "
                    "the English language, including 'bedroom', 'lonely', and 'generous'. His works have "
                    "been translated into every major language and are performed more than any other playwright.\n\n"
                    "Question: How many years after the Globe Theatre was built did it burn down, and what "
                    "incident caused the fire?"
                ),
                "expected": "The Globe Theatre burned down 14 years after it was built in 1599, so in 1613. The fire was caused by a theatrical cannon that misfired during a performance of Henry VIII.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B"],
            },
            {
                "id": "frames_010",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Photosynthesis converts light energy into chemical energy stored in glucose. "
                    "The overall reaction requires carbon dioxide and water as inputs and releases oxygen "
                    "as a byproduct.\n\n"
                    "Passage B: The light-dependent reactions of photosynthesis occur in the thylakoid "
                    "membranes of the chloroplast. They produce ATP and NADPH, which power the light-independent "
                    "reactions, and release oxygen by splitting water molecules.\n\n"
                    "Passage C: The Calvin cycle (light-independent reactions) takes place in the stroma of "
                    "the chloroplast. Using the ATP and NADPH produced by the light reactions, it fixes "
                    "carbon dioxide into three-carbon molecules that are eventually converted to glucose.\n\n"
                    "Question: Where in the chloroplast do the oxygen-releasing reactions occur, and what "
                    "energy carriers do they produce to drive glucose synthesis?"
                ),
                "expected": "Oxygen-releasing reactions occur in the thylakoid membranes. They produce ATP and NADPH, which are used by the Calvin cycle in the stroma to fix carbon dioxide into glucose.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B", "C"],
            },
            {
                "id": "frames_011",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Internet was developed from ARPANET, a US Department of Defense research "
                    "network that went online in 1969. Its early purpose was to enable communication between "
                    "research institutions.\n\n"
                    "Passage B: Tim Berners-Lee invented the World Wide Web in 1989 while working at CERN in "
                    "Switzerland. He proposed it as an information management system and wrote the first web "
                    "browser and server software.\n\n"
                    "Passage C: The first website went live on August 6, 1991. It was hosted on Berners-Lee's "
                    "own computer at CERN and described the World Wide Web project itself. The site is still "
                    "accessible today.\n\n"
                    "Question: How many years elapsed between the origin of the network infrastructure the "
                    "Web runs on and the publication of the first website, and where was the Web invented?"
                ),
                "expected": "The Internet originated with ARPANET in 1969, and the first website went live in 1991, so 22 years elapsed. The World Wide Web was invented at CERN in Switzerland.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_012",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Treaty of Versailles was signed on June 28, 1919, ending World War I. "
                    "It imposed heavy reparations and territorial losses on Germany, contributing to economic "
                    "instability in the Weimar Republic.\n\n"
                    "Passage B: The hyperinflation crisis in Germany peaked in November 1923, when one US "
                    "dollar was worth 4.2 trillion German marks. Workers were paid multiple times daily so "
                    "they could buy goods before prices rose further.\n\n"
                    "Passage C: Adolf Hitler's failed Beer Hall Putsch also occurred on November 8–9, 1923, "
                    "in Munich. The attempted coup was partly motivated by the economic chaos of that period. "
                    "Hitler was subsequently imprisoned and wrote Mein Kampf.\n\n"
                    "Question: What economic condition, stemming from post-WWI peace terms, coincided with "
                    "Hitler's first attempt to seize power, and in what year did both events occur?"
                ),
                "expected": "Hyperinflation, partly caused by the reparations imposed by the Treaty of Versailles, coincided with Hitler's Beer Hall Putsch. Both occurred in 1923.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_013",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The speed of light in a vacuum is exactly 299,792,458 metres per second. "
                    "This value is a defined constant and forms the basis of the metre's modern definition.\n\n"
                    "Passage B: The nearest star system to Earth is Alpha Centauri, located approximately "
                    "4.37 light-years away. A light-year is the distance light travels in one year.\n\n"
                    "Passage C: The Voyager 1 spacecraft, launched in 1977, is the most distant human-made "
                    "object. As of 2024 it is approximately 23.5 billion kilometres from Earth, travelling "
                    "at about 17 kilometres per second.\n\n"
                    "Question: How does the distance to the nearest star compare to Voyager 1's current "
                    "distance from Earth, and what unit is typically used to express interstellar distances?"
                ),
                "expected": "Alpha Centauri is 4.37 light-years away. A light-year is roughly 9.46 trillion km, making Alpha Centauri about 41 trillion km away — over 1,700 times farther than Voyager 1's ~23.5 billion km. Interstellar distances are typically expressed in light-years.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_014",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Penicillin was discovered by Alexander Fleming in 1928 when he noticed that "
                    "a mould (Penicillium notatum) had contaminated a bacterial culture and was killing the "
                    "surrounding bacteria.\n\n"
                    "Passage B: Howard Florey and Ernst Boris Chain developed penicillin into a practical "
                    "antibiotic drug in the early 1940s. Their work enabled mass production, which proved "
                    "critical during World War II for treating infected wounds.\n\n"
                    "Passage C: Fleming, Florey, and Chain jointly received the Nobel Prize in Physiology "
                    "or Medicine in 1945 for the discovery of penicillin and its curative effects in various "
                    "infectious diseases.\n\n"
                    "Question: How many years passed between Fleming's initial discovery and the Nobel Prize "
                    "recognition, and who shared that prize with him?"
                ),
                "expected": "17 years passed between Fleming's 1928 discovery and the 1945 Nobel Prize. He shared the prize with Howard Florey and Ernst Boris Chain.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "C"],
            },
            {
                "id": "frames_015",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Great Wall of China was built over many centuries, with major construction "
                    "during the Ming dynasty (1368–1644). The wall stretches approximately 21,196 kilometres "
                    "including all its branches.\n\n"
                    "Passage B: The Silk Road was an ancient network of trade routes connecting China to the "
                    "Mediterranean. It facilitated not only commerce but also the spread of culture, religion, "
                    "and disease across Eurasia for centuries.\n\n"
                    "Passage C: The Ming dynasty constructed large sections of the Great Wall partly to "
                    "defend against incursions from Mongol tribes from the north. The wall served as a "
                    "military barrier, communication corridor, and customs checkpoint.\n\n"
                    "Question: During which dynasty was most of the extant Great Wall built, why was it "
                    "constructed, and approximately how long is the total wall?"
                ),
                "expected": "Most of the extant Great Wall was built during the Ming dynasty (1368–1644) primarily to defend against Mongol incursions from the north. The total wall stretches approximately 21,196 kilometres.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "C"],
            },
            {
                "id": "frames_016",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Pacific Ocean is the largest and deepest ocean on Earth, covering more "
                    "than 165 million square kilometres — larger than all of Earth's landmasses combined.\n\n"
                    "Passage B: The Mariana Trench is located in the western Pacific Ocean and contains the "
                    "deepest known point on Earth, the Challenger Deep, at approximately 10,935 metres below "
                    "sea level.\n\n"
                    "Passage C: In 2012 filmmaker James Cameron reached the bottom of the Challenger Deep "
                    "solo in the submersible Deepsea Challenger, becoming only the third person to do so. "
                    "He collected samples and footage for scientific study.\n\n"
                    "Question: In which ocean is the deepest point on Earth located, how deep is it, and "
                    "who was the third person to reach it?"
                ),
                "expected": "The deepest point, Challenger Deep in the Mariana Trench, is in the Pacific Ocean at approximately 10,935 metres below sea level. James Cameron was the third person to reach it in 2012.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_017",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: Isaac Newton formulated his three laws of motion and the law of universal "
                    "gravitation in his 1687 work Principia Mathematica. These principles underpinned "
                    "classical mechanics for over two centuries.\n\n"
                    "Passage B: Albert Einstein published his special theory of relativity in 1905 and his "
                    "general theory of relativity in 1915. General relativity replaced Newtonian gravity "
                    "as the most accurate description of gravitational phenomena.\n\n"
                    "Passage C: GPS satellites must apply corrections from both special and general relativity "
                    "to maintain accuracy. Without these corrections, GPS positions would drift by roughly "
                    "10 kilometres per day due to relativistic time dilation effects.\n\n"
                    "Question: Which physicist's theory superseded Newton's gravitational model, and what "
                    "modern technology would fail without corrections based on that newer theory?"
                ),
                "expected": "Einstein's general theory of relativity (1915) superseded Newton's gravitational model. GPS technology would fail without relativistic corrections; positions would drift about 10 km per day.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B", "C"],
            },
            {
                "id": "frames_018",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Renaissance began in Florence, Italy, in the 14th century and spread "
                    "across Europe over the next two centuries. It was marked by renewed interest in "
                    "classical Greek and Roman culture, science, and the arts.\n\n"
                    "Passage B: Leonardo da Vinci (1452–1519) was the archetypal Renaissance polymath. "
                    "His notebooks contain detailed studies of anatomy, engineering, and hydraulics alongside "
                    "sketches of flying machines centuries ahead of their time.\n\n"
                    "Passage C: The printing press, invented by Johannes Gutenberg around 1440, dramatically "
                    "accelerated the spread of Renaissance ideas across Europe by making books cheaper and "
                    "more widely available. By 1500 an estimated 20 million books had been printed.\n\n"
                    "Question: Name one person who embodied Renaissance values across multiple fields and "
                    "identify the invention that helped spread those ideas so rapidly across Europe."
                ),
                "expected": "Leonardo da Vinci embodied Renaissance values across art, anatomy, engineering, and science. The printing press, invented by Gutenberg around 1440, spread Renaissance ideas rapidly by making books widely available.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["B", "C"],
            },
            {
                "id": "frames_019",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The ozone layer, located in Earth's stratosphere at altitudes of 15–35 km, "
                    "absorbs most of the Sun's ultraviolet (UV) radiation. Depletion of ozone increases "
                    "ground-level UV exposure, raising risks of skin cancer and cataracts.\n\n"
                    "Passage B: Chlorofluorocarbons (CFCs) were widely used as refrigerants and aerosol "
                    "propellants from the 1930s onward. Scientists discovered in the 1970s that CFCs "
                    "decompose in the stratosphere, releasing chlorine atoms that catalytically destroy "
                    "ozone molecules.\n\n"
                    "Passage C: The Montreal Protocol, signed in 1987, is an international treaty that "
                    "phased out the production of ozone-depleting substances including CFCs. It is "
                    "considered one of the most successful environmental agreements ever implemented.\n\n"
                    "Question: What chemical compounds caused ozone depletion, through what mechanism, "
                    "and what international agreement curtailed their use?"
                ),
                "expected": "CFCs (chlorofluorocarbons) depleted the ozone layer by decomposing in the stratosphere and releasing chlorine atoms that catalytically destroy ozone. The Montreal Protocol (1987) phased out their production.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
            {
                "id": "frames_020",
                "prompt": (
                    "Read the following passages and answer the question.\n\n"
                    "Passage A: The Wright brothers, Orville and Wilbur, made the first successful powered "
                    "aeroplane flights on December 17, 1903, at Kitty Hawk, North Carolina. The longest of "
                    "four flights that day lasted 59 seconds and covered 260 metres.\n\n"
                    "Passage B: Charles Lindbergh completed the first solo non-stop transatlantic flight on "
                    "May 20–21, 1927, flying from New York to Paris in 33.5 hours in his aircraft Spirit "
                    "of St. Louis. He won the $25,000 Orteig Prize for the feat.\n\n"
                    "Passage C: The Concorde supersonic passenger jet entered service in 1976 and could cross "
                    "the Atlantic in approximately 3.5 hours — cutting Lindbergh's journey time by 90%. It "
                    "was retired in 2003 after 27 years of commercial operation.\n\n"
                    "Question: How many years after the first powered flight did Lindbergh cross the Atlantic, "
                    "and by how much did the Concorde reduce that crossing time?"
                ),
                "expected": "Lindbergh's transatlantic flight in 1927 was 24 years after the first powered flight in 1903. The Concorde reduced the 33.5-hour crossing to about 3.5 hours, a reduction of roughly 90%.",
                "source_ids": ["A", "B", "C"],
                "required_sources": ["A", "B", "C"],
            },
        ]

    def _check_multi_source(self, prompt_data: Dict[str, Any], response: str) -> bool:
        """Return True if the response cites or references facts from multiple passages."""
        response_lower = response.lower()
        required = prompt_data.get("required_sources", ["A", "B"])
        # Look for passage labels or distinctive proper nouns/numbers from each source
        passage_markers = {
            "A": ["passage a", "first passage", "document a"],
            "B": ["passage b", "second passage", "document b"],
            "C": ["passage c", "third passage", "document c"],
        }
        hits = 0
        for src in required:
            for marker in passage_markers.get(src, []):
                if marker in response_lower:
                    hits += 1
                    break
        # Also accept if response is long and substantive (likely synthesised)
        if hits < len(required) and len(response.split()) > 40:
            # Heuristic: a long answer that doesn't quote passages may still be multi-source
            hits = max(hits, len(required) - 1)
        return hits >= max(1, len(required) - 1)

    def _check_correct_answer(self, prompt_data: Dict[str, Any], response: str) -> bool:
        """Return True if the response contains key facts from the expected answer."""
        expected = prompt_data.get("expected", "")
        response_lower = response.lower()
        # Extract significant tokens from expected answer (length > 4, not stop words)
        stop = {"from", "that", "this", "with", "were", "have", "been", "they",
                "their", "about", "which", "also", "both", "after", "into"}
        key_tokens = [
            w.strip(".,;:'\"()").lower()
            for w in expected.split()
            if len(w) > 4 and w.lower() not in stop
        ]
        if not key_tokens:
            return False
        matches = sum(1 for t in key_tokens if t in response_lower)
        return matches / len(key_tokens) >= 0.45

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score = 0.4 (multi-source synthesis) + 0.6 (correct answer)."""
        multi_source = self._check_multi_source(prompt_data, response)
        correct = self._check_correct_answer(prompt_data, response)

        score = 0.0
        if multi_source:
            score += 0.4
        if correct:
            score += 0.6

        return {
            "success": score >= 0.6,
            "score": round(score, 2),
            "metadata": {
                "multi_source_synthesis": multi_source,
                "correct_answer": correct,
                "prompt_id": prompt_data.get("id"),
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are a research assistant. Read all provided passages carefully, then answer "
            "the question by synthesising information from multiple sources. Clearly indicate "
            "which passages support your answer."
        )
