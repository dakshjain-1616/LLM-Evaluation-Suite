"""VideoMME benchmark - Video understanding tasks via scene-by-scene descriptions."""

from typing import Dict, Any, List, Optional
import re
from .base import Benchmark, BenchmarkConfig


class VideoMMEBenchmark(Benchmark):
    """VideoMME - Video multi-modal evaluation via textual scene descriptions."""

    def __init__(self):
        config = BenchmarkConfig(
            name="video_mme",
            description="Video understanding via temporal scene descriptions",
            category="multimodal",
            version="1.0",
            timeout=90,
            max_tokens=2048,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load video scene description prompts covering temporal, causal, counting, and summarization tasks."""
        self.prompts = [
            {
                "id": "vmme_001",
                "prompt": (
                    "The following is a scene-by-scene description of a 3-minute cooking video:\n\n"
                    "Scene 1 (0:00–0:20): A chef stands at a counter. She places a cutting board, a knife, "
                    "two onions, three cloves of garlic, and a red bell pepper on the counter.\n"
                    "Scene 2 (0:20–0:45): She dices the onions and minces the garlic. Her eyes water visibly.\n"
                    "Scene 3 (0:45–1:10): She heats olive oil in a pan over medium heat, then adds the onions "
                    "and garlic. She stirs them for 30 seconds.\n"
                    "Scene 4 (1:10–1:35): She slices the red bell pepper and adds it to the pan. The vegetables "
                    "begin to sizzle loudly.\n"
                    "Scene 5 (1:35–2:05): She opens a can of crushed tomatoes and pours it into the pan. "
                    "She adds salt, pepper, and dried oregano.\n"
                    "Scene 6 (2:05–2:40): The sauce simmers. She stirs it occasionally and tastes it with a spoon.\n"
                    "Scene 7 (2:40–3:00): She ladles the finished sauce over a bowl of pasta and garnishes with fresh basil.\n\n"
                    "Question: What did the chef add to the pan immediately BEFORE the crushed tomatoes?"
                ),
                "expected": "red bell pepper",
                "question_type": "temporal",
                "key_facts": ["red bell pepper", "bell pepper"],
            },
            {
                "id": "vmme_002",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute documentary clip about a beehive:\n\n"
                    "Scene 1 (0:00–0:30): A beekeeper in full protective gear approaches a wooden hive box in a garden.\n"
                    "Scene 2 (0:30–1:00): She uses a smoker to puff white smoke into the hive entrance. "
                    "The bees visibly slow their movement.\n"
                    "Scene 3 (1:00–1:40): She lifts the hive cover and removes a honeycomb frame. "
                    "Thousands of bees cover the frame.\n"
                    "Scene 4 (1:40–2:20): She inspects the frame closely, pointing out capped honey cells "
                    "and open brood cells with larvae.\n"
                    "Scene 5 (2:20–3:00): She spots the queen bee – larger than the others – moving slowly "
                    "across the frame. Worker bees cluster around her.\n"
                    "Scene 6 (3:00–3:30): She carefully replaces the frame and closes the hive.\n"
                    "Scene 7 (3:30–4:00): A narrator explains that healthy hives are inspected every 7–10 days "
                    "during the active season.\n\n"
                    "Question: Why did the beekeeper use smoke before opening the hive?"
                ),
                "expected": "to calm the bees",
                "question_type": "causal",
                "key_facts": ["calm", "slow", "bees", "smoke"],
            },
            {
                "id": "vmme_003",
                "prompt": (
                    "The following is a scene-by-scene description of a 2-minute sports highlight reel:\n\n"
                    "Scene 1 (0:00–0:18): A basketball player dribbles past two defenders and scores a layup.\n"
                    "Scene 2 (0:18–0:35): The opposing team attempts a three-pointer; it misses and is rebounded.\n"
                    "Scene 3 (0:35–0:52): The same player drives baseline and scores with a reverse layup.\n"
                    "Scene 4 (0:52–1:10): A teammate hits a mid-range jump shot from the elbow.\n"
                    "Scene 5 (1:10–1:28): The player receives a pass, pump-fakes a defender, and scores a floater.\n"
                    "Scene 6 (1:28–1:45): A fast-break opportunity results in the player's fourth basket – a dunk.\n"
                    "Scene 7 (1:45–2:00): Final scoreboard shows Home 98, Visitors 91. Post-game handshakes.\n\n"
                    "Question: How many times did the featured player score during this highlight reel?"
                ),
                "expected": "4",
                "question_type": "counting",
                "key_facts": ["4", "four"],
            },
            {
                "id": "vmme_004",
                "prompt": (
                    "The following is a scene-by-scene description of a 5-minute time-lapse video of a plant growing:\n\n"
                    "Scene 1 (Day 0): A seed is planted in a small pot of dark soil. The pot is placed on a windowsill.\n"
                    "Scene 2 (Days 1–3): No visible change above the soil surface.\n"
                    "Scene 3 (Days 4–6): A small white sprout breaks through the soil.\n"
                    "Scene 4 (Days 7–10): The sprout grows upright; two small seed leaves (cotyledons) unfurl.\n"
                    "Scene 5 (Days 11–16): True leaves appear above the cotyledons; stem thickens.\n"
                    "Scene 6 (Days 17–22): Plant reaches ~8 cm tall; stem is clearly green and sturdy.\n"
                    "Scene 7 (Days 23–30): Plant stands ~14 cm tall with multiple leaf pairs. A small flower bud "
                    "is visible at the top.\n\n"
                    "Question: What happened to the plant between Days 7 and 10?"
                ),
                "expected": "two seed leaves unfurled",
                "question_type": "temporal",
                "key_facts": ["leaves", "cotyledons", "unfurl", "upright", "seed leaves"],
            },
            {
                "id": "vmme_005",
                "prompt": (
                    "The following is a scene-by-scene description of a 6-minute tutorial video on changing a tire:\n\n"
                    "Scene 1 (0:00–0:30): Presenter introduces the video. A flat tire on a sedan is shown.\n"
                    "Scene 2 (0:30–1:10): She retrieves the spare tire, car jack, and lug wrench from the trunk.\n"
                    "Scene 3 (1:10–1:50): She loosens (but does not remove) the lug nuts before jacking up the car.\n"
                    "Scene 4 (1:50–2:30): She positions the jack under the vehicle frame near the flat tire and raises it.\n"
                    "Scene 5 (2:30–3:10): She removes the lug nuts fully, then pulls off the flat tire.\n"
                    "Scene 6 (3:10–3:55): She mounts the spare tire and hand-tightens the lug nuts in a star pattern.\n"
                    "Scene 7 (3:55–4:40): She lowers the car, then torques the lug nuts fully in a star pattern.\n"
                    "Scene 8 (4:40–5:20): She stows the flat tire and tools in the trunk.\n"
                    "Scene 9 (5:20–6:00): She reminds viewers to check the spare's tire pressure and visit a shop soon.\n\n"
                    "Question: Why did she loosen the lug nuts BEFORE jacking up the car rather than after?"
                ),
                "expected": "to prevent the wheel from spinning",
                "question_type": "causal",
                "key_facts": ["spin", "rotate", "wheel", "before", "prevent"],
            },
            {
                "id": "vmme_006",
                "prompt": (
                    "The following is a scene-by-scene description of a 3-minute news segment:\n\n"
                    "Scene 1 (0:00–0:25): Anchor introduces a story about a new bridge opening in the city.\n"
                    "Scene 2 (0:25–1:00): Reporter on-site interviews the mayor, who cuts a ribbon.\n"
                    "Scene 3 (1:00–1:30): B-roll footage shows cars crossing the bridge for the first time.\n"
                    "Scene 4 (1:30–2:00): Reporter interviews a commuter who says the bridge cuts her commute "
                    "from 45 minutes to 12 minutes.\n"
                    "Scene 5 (2:00–2:30): An engineer explains it took 3 years and $240 million to build.\n"
                    "Scene 6 (2:30–3:00): Anchor summarizes: the bridge is expected to reduce downtown traffic "
                    "congestion by 30%.\n\n"
                    "Question: How much did the bridge cost to build, and how long did construction take?"
                ),
                "expected": "$240 million, 3 years",
                "question_type": "extraction",
                "key_facts": ["240 million", "3 years", "three years"],
            },
            {
                "id": "vmme_007",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute wildlife documentary clip:\n\n"
                    "Scene 1 (0:00–0:30): A lioness is shown resting in tall savanna grass at dawn.\n"
                    "Scene 2 (0:30–1:10): She spots a herd of zebras grazing 200 meters away and crouches low.\n"
                    "Scene 3 (1:10–1:50): She stalks slowly, using the tall grass as cover, closing to 50 meters.\n"
                    "Scene 4 (1:50–2:20): She charges at full speed toward the herd. The zebras scatter.\n"
                    "Scene 5 (2:20–2:55): She isolates a young zebra from the herd and brings it down.\n"
                    "Scene 6 (2:55–3:30): Two other lionesses arrive and all three feed on the carcass.\n"
                    "Scene 7 (3:30–4:00): A narrator states that lions are successful in only about 20–25% of hunts.\n\n"
                    "Question: How many lionesses fed on the prey at the end of the hunt?"
                ),
                "expected": "3",
                "question_type": "counting",
                "key_facts": ["3", "three", "three lionesses"],
            },
            {
                "id": "vmme_008",
                "prompt": (
                    "The following is a scene-by-scene description of a 5-minute product review video:\n\n"
                    "Scene 1 (0:00–0:30): Reviewer unboxes a new laptop, describing the packaging.\n"
                    "Scene 2 (0:30–1:15): He describes the physical design: slim profile, aluminum chassis, "
                    "14-inch display, USB-C and USB-A ports.\n"
                    "Scene 3 (1:15–2:00): He powers it on and notes the fast boot time (~8 seconds).\n"
                    "Scene 4 (2:00–2:45): He runs a benchmark test, showing a score of 12,400 in Cinebench R23.\n"
                    "Scene 5 (2:45–3:30): He tests the display, calling the color accuracy 'excellent' but the "
                    "brightness 'adequate, not exceptional'.\n"
                    "Scene 6 (3:30–4:15): He criticizes the single speaker placement and calls the audio quality "
                    "'mediocre for the price point'.\n"
                    "Scene 7 (4:15–5:00): Summary: overall rating 8.2/10. Recommended for professionals but "
                    "not for audio/media creatives.\n\n"
                    "Question: What were the two main criticisms the reviewer raised about the laptop?"
                ),
                "expected": "speaker placement and audio quality, display brightness",
                "question_type": "summarization",
                "key_facts": ["audio", "speaker", "brightness", "mediocre", "criticism"],
            },
            {
                "id": "vmme_009",
                "prompt": (
                    "The following is a scene-by-scene description of a 3-minute educational video about volcanoes:\n\n"
                    "Scene 1 (0:00–0:30): Animation shows Earth's cross-section with the mantle and tectonic plates.\n"
                    "Scene 2 (0:30–1:00): Narrator explains how magma rises through fissures when plates separate.\n"
                    "Scene 3 (1:00–1:30): Animation shows lava erupting from a shield volcano in Hawaii.\n"
                    "Scene 4 (1:30–2:00): Narrator contrasts shield volcanoes (low viscosity, gentle eruptions) "
                    "with stratovolcanoes (high viscosity, explosive eruptions).\n"
                    "Scene 5 (2:00–2:30): Footage of the 1980 Mount St. Helens eruption is shown. Narrator "
                    "states it expelled 1 cubic mile of material.\n"
                    "Scene 6 (2:30–3:00): Narrator explains pyroclastic flows as superheated gas and rock "
                    "traveling at up to 700 km/h.\n\n"
                    "Question: What is the key difference between a shield volcano and a stratovolcano, "
                    "according to the video?"
                ),
                "expected": "lava viscosity and eruption style",
                "question_type": "causal",
                "key_facts": ["viscosity", "explosive", "gentle", "shield", "stratovolcano"],
            },
            {
                "id": "vmme_010",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute interview video:\n\n"
                    "Scene 1 (0:00–0:25): Host introduces guest Dr. Elena Vasquez, a climate scientist from MIT.\n"
                    "Scene 2 (0:25–1:05): Dr. Vasquez discusses rising CO2 levels, citing 421 ppm as of 2023.\n"
                    "Scene 3 (1:05–1:45): She explains the greenhouse effect using a simple analogy: a car "
                    "with windows trapping heat.\n"
                    "Scene 4 (1:45–2:25): Host asks about solutions. Dr. Vasquez names carbon capture, "
                    "renewable energy expansion, and reforestation as the top three.\n"
                    "Scene 5 (2:25–3:05): Dr. Vasquez says the biggest obstacle is political will, not technology.\n"
                    "Scene 6 (3:05–3:40): Host asks what individuals can do. She suggests reducing meat consumption, "
                    "using public transit, and supporting carbon-pricing policies.\n"
                    "Scene 7 (3:40–4:00): Host thanks her; screen shows her new book title: 'The Tipping Clock'.\n\n"
                    "Question: According to Dr. Vasquez, what is the biggest obstacle to addressing climate change?"
                ),
                "expected": "political will",
                "question_type": "causal",
                "key_facts": ["political will", "political", "not technology"],
            },
            {
                "id": "vmme_011",
                "prompt": (
                    "The following is a scene-by-scene description of a 5-minute gym workout tutorial:\n\n"
                    "Scene 1 (0:00–0:30): Trainer introduces a 4-exercise circuit for core strength.\n"
                    "Scene 2 (0:30–1:20): Exercise 1 – Plank: demonstrated for 30 seconds. Form tips given.\n"
                    "Scene 3 (1:20–2:10): Exercise 2 – Bicycle crunches: 20 reps shown. Breathing cues provided.\n"
                    "Scene 4 (2:10–3:00): Exercise 3 – Russian twists with a 5 kg weight: 16 reps demonstrated.\n"
                    "Scene 5 (3:00–3:50): Exercise 4 – Leg raises: 12 reps shown. Trainer emphasizes lower back contact.\n"
                    "Scene 6 (3:50–4:20): Trainer recommends doing the circuit 3 times with 60-second rest between rounds.\n"
                    "Scene 7 (4:20–5:00): Cool-down stretches are shown. Trainer reminds viewers to hydrate.\n\n"
                    "Question: How many total reps of bicycle crunches would a person complete if they do the "
                    "full recommended circuit?"
                ),
                "expected": "60",
                "question_type": "counting",
                "key_facts": ["60", "sixty"],
            },
            {
                "id": "vmme_012",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute travel vlog in Tokyo:\n\n"
                    "Scene 1 (0:00–0:30): Vlogger arrives at Tokyo Station and navigates the subway map.\n"
                    "Scene 2 (0:30–1:05): She visits Senso-ji Temple in Asakusa, photographs the giant lantern.\n"
                    "Scene 3 (1:05–1:40): She walks along Nakamise shopping street, buys ningyo-yaki pastries.\n"
                    "Scene 4 (1:40–2:15): She takes the subway to Shibuya and films the famous scramble crossing.\n"
                    "Scene 5 (2:15–2:50): She shops in a vintage clothing store, finding a jacket for ¥3,500.\n"
                    "Scene 6 (2:50–3:25): She visits a ramen shop in Shinjuku and orders a bowl of tonkotsu ramen.\n"
                    "Scene 7 (3:25–4:00): She arrives at her hostel and summarizes: 4 neighborhoods, 6 hours, "
                    "approximately ¥6,200 spent.\n\n"
                    "Question: What did the vlogger do immediately AFTER visiting Senso-ji Temple?"
                ),
                "expected": "walked along Nakamise shopping street",
                "question_type": "temporal",
                "key_facts": ["nakamise", "shopping street", "pastries", "ningyo"],
            },
            {
                "id": "vmme_013",
                "prompt": (
                    "The following is a scene-by-scene description of a 3-minute science experiment video:\n\n"
                    "Scene 1 (0:00–0:20): A teacher shows a glass of water, a dropper of food coloring, and salt.\n"
                    "Scene 2 (0:20–0:50): She drops three drops of blue food coloring into the water; it slowly disperses.\n"
                    "Scene 3 (0:50–1:20): She stirs the water vigorously for 10 seconds; color becomes uniform.\n"
                    "Scene 4 (1:20–1:50): She adds two heaping tablespoons of salt and stirs; the water becomes cloudy.\n"
                    "Scene 5 (1:50–2:20): She lets the glass sit undisturbed for 90 seconds; visible layers begin to form.\n"
                    "Scene 6 (2:20–2:50): Two distinct layers are visible – a denser salt-water layer at the bottom.\n"
                    "Scene 7 (2:50–3:00): Teacher explains: salt increases water density, causing stratification.\n\n"
                    "Question: What caused the two distinct layers to form in the glass?"
                ),
                "expected": "salt increased the water density",
                "question_type": "causal",
                "key_facts": ["salt", "density", "stratification", "denser", "layers"],
            },
            {
                "id": "vmme_014",
                "prompt": (
                    "The following is a scene-by-scene description of a 6-minute historical documentary segment:\n\n"
                    "Scene 1 (0:00–0:35): Narrator introduces the Apollo 11 mission, July 1969.\n"
                    "Scene 2 (0:35–1:15): Footage of launch from Kennedy Space Center on July 16, 1969. "
                    "Three astronauts: Armstrong, Aldrin, Collins.\n"
                    "Scene 3 (1:15–2:00): Animation shows the 3-day journey to the Moon.\n"
                    "Scene 4 (2:00–2:45): The Eagle lunar module separates from Columbia and descends.\n"
                    "Scene 5 (2:45–3:30): Landing on the Sea of Tranquility, July 20, 1969. "
                    "Armstrong reports 'The Eagle has landed.'\n"
                    "Scene 6 (3:30–4:30): Armstrong's moonwalk is shown. He spends 2 hours 31 minutes on the surface. "
                    "He plants the US flag and collects 21.5 kg of rock samples.\n"
                    "Scene 7 (4:30–5:15): Both astronauts return to Eagle; ascent stage launches.\n"
                    "Scene 8 (5:15–6:00): Re-docking with Columbia; safe splashdown in the Pacific on July 24.\n\n"
                    "Question: Which astronaut did NOT walk on the Moon during Apollo 11, and what was his role?"
                ),
                "expected": "Michael Collins, he orbited in the command module Columbia",
                "question_type": "extraction",
                "key_facts": ["collins", "michael collins", "columbia", "orbit"],
            },
            {
                "id": "vmme_015",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute home renovation video:\n\n"
                    "Scene 1 (0:00–0:25): Host shows a plain white wall and announces he will create a wood accent wall.\n"
                    "Scene 2 (0:25–1:00): He measures the wall (8 ft x 12 ft) and calculates the number of planks needed.\n"
                    "Scene 3 (1:00–1:40): He cuts wood planks on a miter saw, wearing safety glasses and ear protection.\n"
                    "Scene 4 (1:40–2:20): He applies construction adhesive to the back of each plank.\n"
                    "Scene 5 (2:20–3:00): He presses planks to the wall horizontally, using a level. "
                    "He places 3 planks per row.\n"
                    "Scene 6 (3:00–3:40): He fills nail holes with wood filler and sands them smooth.\n"
                    "Scene 7 (3:40–4:00): Final reveal: the finished accent wall with alternating natural and stained wood.\n\n"
                    "Question: Provide a brief summary of the steps taken to build the accent wall."
                ),
                "expected": "measure, cut planks, apply adhesive, mount planks, fill and sand holes",
                "question_type": "summarization",
                "key_facts": ["measure", "cut", "adhesive", "mount", "sand", "planks"],
            },
            {
                "id": "vmme_016",
                "prompt": (
                    "The following is a scene-by-scene description of a 3-minute animated explainer video on photosynthesis:\n\n"
                    "Scene 1 (0:00–0:25): Animation shows a green leaf with sunlight hitting its surface.\n"
                    "Scene 2 (0:25–0:55): Narrator explains chlorophyll in chloroplasts absorbs red and blue light.\n"
                    "Scene 3 (0:55–1:30): Light-dependent reactions are shown: water molecules split, oxygen released.\n"
                    "Scene 4 (1:30–2:00): ATP and NADPH produced in the light reactions are shown moving to the stroma.\n"
                    "Scene 5 (2:00–2:30): Calvin cycle animation: CO2 fixed, glucose synthesized using ATP and NADPH.\n"
                    "Scene 6 (2:30–3:00): Summary equation shown: 6CO2 + 6H2O + light → C6H12O6 + 6O2.\n\n"
                    "Question: What two products from the light-dependent reactions are used in the Calvin cycle?"
                ),
                "expected": "ATP and NADPH",
                "question_type": "temporal",
                "key_facts": ["atp", "nadph"],
            },
            {
                "id": "vmme_017",
                "prompt": (
                    "The following is a scene-by-scene description of a 5-minute customer service training video:\n\n"
                    "Scene 1 (0:00–0:30): A trainer introduces the HEARD model for handling complaints.\n"
                    "Scene 2 (0:30–1:10): H = Hear: role-play of agent listening without interrupting an angry customer.\n"
                    "Scene 3 (1:10–1:50): E = Empathize: agent says 'I completely understand your frustration.'\n"
                    "Scene 4 (1:50–2:30): A = Apologize: agent offers a sincere apology without deflecting blame.\n"
                    "Scene 5 (2:30–3:10): R = Resolve: agent offers a refund or replacement option.\n"
                    "Scene 6 (3:10–3:50): D = Diagnose: agent asks follow-up questions to prevent future issues.\n"
                    "Scene 7 (3:50–4:30): A counter-example shows a poorly handled call: agent interrupts and deflects.\n"
                    "Scene 8 (4:30–5:00): Trainer summarizes: 92% of customers who have complaints resolved well "
                    "become loyal customers.\n\n"
                    "Question: How many steps are in the HEARD model, and what does each letter stand for?"
                ),
                "expected": "5 steps: Hear, Empathize, Apologize, Resolve, Diagnose",
                "question_type": "summarization",
                "key_facts": ["hear", "empathize", "apologize", "resolve", "diagnose", "5"],
            },
            {
                "id": "vmme_018",
                "prompt": (
                    "The following is a scene-by-scene description of a 4-minute car accident reconstruction video:\n\n"
                    "Scene 1 (0:00–0:30): Animation shows a two-lane road at an intersection with a traffic light.\n"
                    "Scene 2 (0:30–1:00): Car A approaches from the north at 45 mph. The light turns yellow.\n"
                    "Scene 3 (1:00–1:35): Instead of braking, Car A accelerates through the intersection as light turns red.\n"
                    "Scene 4 (1:35–2:00): Car B, heading east, enters the intersection on a green light.\n"
                    "Scene 5 (2:00–2:30): Car A strikes Car B on the driver's side. Car B spins 90 degrees.\n"
                    "Scene 6 (2:30–3:10): Investigators measure skid marks at 22 feet for Car A, none for Car B.\n"
                    "Scene 7 (3:10–3:40): Expert explains Car A ran a red light as the primary cause.\n"
                    "Scene 8 (3:40–4:00): Statistics shown: red-light running causes 800+ US fatalities per year.\n\n"
                    "Question: What was the primary cause of the collision, and what evidence supported this conclusion?"
                ),
                "expected": "Car A ran a red light; evidence was skid marks and traffic light timing",
                "question_type": "causal",
                "key_facts": ["red light", "car a", "accelerated", "skid marks", "primary cause"],
            },
            {
                "id": "vmme_019",
                "prompt": (
                    "The following is a scene-by-scene description of a 5-minute coding tutorial video on Python list comprehensions:\n\n"
                    "Scene 1 (0:00–0:30): Instructor introduces list comprehensions as a concise way to create lists.\n"
                    "Scene 2 (0:30–1:10): She shows a for-loop creating a list of squares: "
                    "squares = []; for i in range(10): squares.append(i**2).\n"
                    "Scene 3 (1:10–1:50): She rewrites it as a list comprehension: squares = [i**2 for i in range(10)].\n"
                    "Scene 4 (1:50–2:30): She adds a conditional: [i**2 for i in range(10) if i % 2 == 0] "
                    "to get even squares only.\n"
                    "Scene 5 (2:30–3:10): She shows a nested comprehension for a multiplication table.\n"
                    "Scene 6 (3:10–3:50): She demonstrates a dict comprehension: {k: v for k, v in zip(keys, values)}.\n"
                    "Scene 7 (3:50–4:30): She shows a common pitfall: overly complex comprehensions that hurt readability.\n"
                    "Scene 8 (4:30–5:00): Summary: use comprehensions for simple transformations; use loops for complex logic.\n\n"
                    "Question: What was the instructor's advice about when NOT to use list comprehensions?"
                ),
                "expected": "when the logic is too complex and hurts readability",
                "question_type": "summarization",
                "key_facts": ["complex", "readability", "loop", "pitfall"],
            },
            {
                "id": "vmme_020",
                "prompt": (
                    "The following is a scene-by-scene description of a 6-minute nature video about salmon migration:\n\n"
                    "Scene 1 (0:00–0:40): Narrator introduces Pacific salmon, which are born in freshwater rivers.\n"
                    "Scene 2 (0:40–1:20): Young salmon (smolts) are shown traveling downstream to the ocean.\n"
                    "Scene 3 (1:20–2:00): Animation shows salmon spending 2–5 years feeding in the open Pacific.\n"
                    "Scene 4 (2:00–2:45): Narrator explains that salmon use Earth's magnetic field and olfactory memory "
                    "to navigate back to their birth river.\n"
                    "Scene 5 (2:45–3:30): Adult salmon are shown swimming upstream, leaping over waterfalls.\n"
                    "Scene 6 (3:30–4:15): Bears are shown catching salmon at a waterfall – five catches shown in the clip.\n"
                    "Scene 7 (4:15–5:00): Salmon reach their spawning grounds, lay eggs, and most die within days.\n"
                    "Scene 8 (5:00–6:00): Narrator explains salmon carcasses enrich the forest ecosystem with marine nutrients.\n\n"
                    "Question: How do salmon navigate back to their birth river after years in the ocean?"
                ),
                "expected": "magnetic field and olfactory memory",
                "question_type": "causal",
                "key_facts": ["magnetic field", "olfactory", "smell", "memory", "navigate"],
            },
        ]

    def _count_key_facts(self, response: str, key_facts: List[str]) -> int:
        """Count how many key facts appear in the response (case-insensitive)."""
        response_lower = response.lower()
        return sum(1 for fact in key_facts if fact.lower() in response_lower)

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """
        Evaluate a VideoMME response based on key facts present in the expected answer.

        Scoring:
          1.0 - majority (>= 60%) of key facts present
          0.5 - some (>= 30%) of key facts present
          0.0 - fewer key facts or empty response
        """
        key_facts: List[str] = prompt_data.get("key_facts", [])
        expected: str = str(prompt_data.get("expected", ""))
        question_type: str = prompt_data.get("question_type", "extraction")
        response_lower = response.lower().strip()

        if not response_lower:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"reason": "empty_response", "question_type": question_type},
            }

        # Direct expected string check (fast path for short answers)
        if expected.lower() in response_lower:
            return {
                "success": True,
                "score": 1.0,
                "metadata": {
                    "match_type": "exact",
                    "question_type": question_type,
                    "key_facts_found": len(key_facts),
                    "key_facts_total": len(key_facts),
                },
            }

        # Key-facts based scoring
        if not key_facts:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"reason": "no_key_facts", "question_type": question_type},
            }

        found = self._count_key_facts(response, key_facts)
        ratio = found / len(key_facts)

        if ratio >= 0.6:
            score = 1.0
            success = True
            match_type = "key_facts_full"
        elif ratio >= 0.3:
            score = 0.5
            success = False
            match_type = "key_facts_partial"
        else:
            score = 0.0
            success = False
            match_type = "key_facts_insufficient"

        return {
            "success": success,
            "score": score,
            "metadata": {
                "match_type": match_type,
                "question_type": question_type,
                "key_facts_found": found,
                "key_facts_total": len(key_facts),
                "ratio": round(ratio, 2),
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are a video understanding assistant. You will be given a detailed scene-by-scene "
            "description of a video. Answer questions about temporal order, causal relationships, "
            "counts, and summaries based solely on the described content. Be concise and precise."
        )
