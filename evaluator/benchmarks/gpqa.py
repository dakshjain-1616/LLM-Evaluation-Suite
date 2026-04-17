"""GPQA Diamond benchmark - Graduate-level science QA."""

from typing import Dict, Any, List
import re
from .base import Benchmark, BenchmarkConfig


class GPQABenchmark(Benchmark):
    """GPQA Diamond - Graduate-level science QA benchmark."""
    
    def __init__(self):
        config = BenchmarkConfig(
            name="gpqa_diamond",
            description="Graduate-level science QA",
            category="reasoning",
            version="1.0",
            timeout=60,
            max_tokens=512,
            temperature=0.1
        )
        super().__init__(config)
    
    def _load_prompts(self) -> None:
        """Load synthetic graduate-level science prompts."""
        self.prompts = [
            {
                "id": "gpqa_001",
                "prompt": """Answer this graduate-level physics question:

In quantum mechanics, the uncertainty principle states that certain pairs of physical properties cannot both be known to arbitrary precision. If the position of a particle is known with certainty, what can be said about its momentum?

A) The momentum is also known with certainty
B) The momentum is completely uncertain
C) The momentum uncertainty is inversely proportional to position uncertainty
D) The momentum can be known within Planck's constant

Select the correct answer.""",
                "expected": "B",
                "explanation": "Heisenberg uncertainty principle: precise position means completely uncertain momentum"
            },
            {
                "id": "gpqa_002",
                "prompt": """Answer this graduate-level chemistry question:

In organic chemistry, which factor most significantly affects the rate of an SN2 reaction?

A) The stability of the carbocation intermediate
B) The steric hindrance at the reaction center
C) The aromaticity of the product
D) The conjugation in the substrate

Select the correct answer.""",
                "expected": "B",
                "explanation": "SN2 reactions are highly sensitive to steric hindrance at the reaction center"
            },
            {
                "id": "gpqa_003",
                "prompt": """Answer this graduate-level biology question:

In cellular biology, what is the primary function of the Golgi apparatus?

A) Protein synthesis
B) Post-translational modification and sorting of proteins
C) ATP production
D) DNA replication

Select the correct answer.""",
                "expected": "B",
                "explanation": "Golgi apparatus modifies, packages, and sorts proteins for secretion or delivery"
            },
            {
                "id": "gpqa_004",
                "prompt": """Answer this graduate-level physics question:

In general relativity, what does the Einstein field equation relate?

A) Mass and velocity
B) Spacetime curvature and energy-momentum
C) Electric and magnetic fields
D) Temperature and entropy

Select the correct answer.""",
                "expected": "B",
                "explanation": "Einstein field equations relate spacetime curvature to energy-momentum content"
            },
            {
                "id": "gpqa_005",
                "prompt": """Answer this graduate-level chemistry question:

Which quantum number determines the shape of an atomic orbital?

A) Principal quantum number (n)
B) Angular momentum quantum number (l)
C) Magnetic quantum number (ml)
D) Spin quantum number (ms)

Select the correct answer.""",
                "expected": "B",
                "explanation": "Angular momentum quantum number l determines orbital shape (s, p, d, f)"
            },
            {
                "id": "gpqa_006",
                "prompt": """Answer this graduate-level biology question:

What is the primary role of tRNA in protein synthesis?

A) To carry genetic information from nucleus to ribosome
B) To bring amino acids to the ribosome
C) To catalyze peptide bond formation
D) To terminate translation

Select the correct answer.""",
                "expected": "B",
                "explanation": "tRNA carries specific amino acids to the ribosome during translation"
            },
            {
                "id": "gpqa_007",
                "prompt": """Answer this graduate-level physics question:

In thermodynamics, what does the second law state about entropy in an isolated system?

A) Entropy always decreases
B) Entropy remains constant
C) Entropy never decreases
D) Entropy is conserved

Select the correct answer.""",
                "expected": "C",
                "explanation": "Second law: entropy of isolated system never decreases, increases for irreversible processes"
            },
            {
                "id": "gpqa_008",
                "prompt": """Answer this graduate-level chemistry question:

In electrochemistry, what happens at the anode during electrolysis?

A) Reduction occurs
B) Oxidation occurs
C) Electrons are gained
D) Metal is deposited

Select the correct answer.""",
                "expected": "B",
                "explanation": "At anode, oxidation occurs (loss of electrons); at cathode, reduction occurs"
            },
            {
                "id": "gpqa_009",
                "prompt": """Answer this graduate-level biology question:

Which process produces the most ATP per glucose molecule in cellular respiration?

A) Glycolysis
B) Pyruvate oxidation
C) Krebs cycle
D) Oxidative phosphorylation

Select the correct answer.""",
                "expected": "D",
                "explanation": "Oxidative phosphorylation produces ~28-34 ATP, most of the total ~30-32 ATP"
            },
            {
                "id": "gpqa_010",
                "prompt": """Answer this graduate-level physics question:

What is the de Broglie wavelength of a particle?

A) Proportional to its mass
B) Inversely proportional to its momentum
C) Equal to its Compton wavelength
D) Independent of its velocity

Select the correct answer.""",
                "expected": "B",
                "explanation": "de Broglie wavelength λ = h/p, inversely proportional to momentum"
            },
            {
                "id": "gpqa_011",
                "prompt": """Answer this graduate-level chemistry question:

What is the hybridization of carbon in ethene (C2H4)?

A) sp
B) sp2
C) sp3
D) dsp3

Select the correct answer.""",
                "expected": "B",
                "explanation": "Carbon in ethene has sp2 hybridization with one pi bond"
            },
            {
                "id": "gpqa_012",
                "prompt": """Answer this graduate-level biology question:

What is the function of restriction enzymes in molecular biology?

A) To synthesize DNA
B) To cut DNA at specific sequences
C) To repair DNA damage
D) To transcribe RNA

Select the correct answer.""",
                "expected": "B",
                "explanation": "Restriction enzymes recognize and cut DNA at specific nucleotide sequences"
            },
            {
                "id": "gpqa_013",
                "prompt": """Answer this graduate-level physics question:

In special relativity, what happens to the length of an object moving at relativistic speeds as measured by a stationary observer?

A) It increases
B) It decreases (Lorentz contraction)
C) It remains unchanged
D) It becomes infinite

Select the correct answer.""",
                "expected": "B",
                "explanation": "Length contraction: moving objects appear shorter in direction of motion"
            },
            {
                "id": "gpqa_014",
                "prompt": """Answer this graduate-level chemistry question:

What is the primary intermolecular force in liquid water?

A) London dispersion forces
B) Dipole-dipole interactions
C) Hydrogen bonding
D) Ionic bonding

Select the correct answer.""",
                "expected": "C",
                "explanation": "Hydrogen bonding is the dominant intermolecular force in water"
            },
            {
                "id": "gpqa_015",
                "prompt": """Answer this graduate-level biology question:

What is the primary function of the rough endoplasmic reticulum?

A) Lipid synthesis
B) Protein synthesis and processing
C) Cellular respiration
D) Waste removal

Select the correct answer.""",
                "expected": "B",
                "explanation": "Rough ER with ribosomes synthesizes and processes proteins"
            },
            {
                "id": "gpqa_016",
                "prompt": """Answer this graduate-level physics question:

In quantum field theory, what mediates the electromagnetic force?

A) Gluons
B) Photons
C) W and Z bosons
D) Gravitons

Select the correct answer.""",
                "expected": "B",
                "explanation": "Photons mediate electromagnetic force in quantum electrodynamics"
            },
            {
                "id": "gpqa_017",
                "prompt": """Answer this graduate-level chemistry question:

What is the effect of a catalyst on a chemical reaction?

A) It increases the equilibrium constant
B) It lowers the activation energy
C) It changes the reaction enthalpy
D) It shifts the equilibrium position

Select the correct answer.""",
                "expected": "B",
                "explanation": "Catalysts lower activation energy without affecting equilibrium or thermodynamics"
            },
            {
                "id": "gpqa_018",
                "prompt": """Answer this graduate-level biology question:

What is the primary function of the enzyme DNA polymerase?

A) To unwind DNA
B) To synthesize new DNA strands
C) To seal nicks in DNA
D) To degrade RNA primers

Select the correct answer.""",
                "expected": "B",
                "explanation": "DNA polymerase synthesizes new DNA strands during replication"
            },
            {
                "id": "gpqa_019",
                "prompt": """Answer this graduate-level physics question:

What is the relationship between electric field and electric potential?

A) E = -∇V (electric field is negative gradient of potential)
B) E = V/d
C) E = V^2
D) E = -V

Select the correct answer.""",
                "expected": "A",
                "explanation": "Electric field is the negative gradient of electric potential"
            },
            {
                "id": "gpqa_020",
                "prompt": """Answer this graduate-level chemistry question:

In a galvanic cell, which electrode is the cathode?

A) The electrode where oxidation occurs
B) The electrode where reduction occurs
C) The negative electrode
D) The electrode that loses mass

Select the correct answer.""",
                "expected": "B",
                "explanation": "Cathode is where reduction occurs; anode is where oxidation occurs"
            }
        ]
    
    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Evaluate a GPQA response."""
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
        return "You are a science expert. Answer the graduate-level question by selecting the correct letter (A, B, C, or D)."
