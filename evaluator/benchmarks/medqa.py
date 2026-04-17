"""MedQA benchmark - USMLE-style multiple choice medical questions."""

import re
from typing import Dict, Any, Optional
from .base import Benchmark, BenchmarkConfig

_SYSTEM_PROMPT = (
    "You are a medical expert. Read the clinical scenario carefully and select "
    "the best answer. Respond with the letter of your choice (A, B, C, D, or E) "
    "followed by a brief justification."
)


class MedQABenchmark(Benchmark):
    """MedQA - USMLE-style clinical vignette MCQ evaluation."""

    def __init__(self):
        config = BenchmarkConfig(
            name="medqa",
            description="USMLE-style medical MCQ covering pharmacology, pathophysiology, diagnosis, and anatomy",
            category="knowledge",
            version="1.0",
            timeout=60,
            max_tokens=512,
            temperature=0.0,
        )
        super().__init__(config)

    def get_system_prompt(self) -> str:
        return _SYSTEM_PROMPT

    def _load_prompts(self) -> None:
        self.prompts = [
            {
                "id": "medqa_001",
                "prompt": (
                    "A 45-year-old man presents with severe chest pain radiating to his left arm "
                    "and jaw for the past 90 minutes. ECG shows ST-elevation in leads II, III, and aVF. "
                    "Troponin is elevated. He has no contraindications to fibrinolytics. "
                    "The nearest PCI-capable centre is 3 hours away. "
                    "Which is the most appropriate immediate intervention?\n\n"
                    "A) Aspirin only\n"
                    "B) IV heparin drip and observation\n"
                    "C) Fibrinolytic therapy\n"
                    "D) Emergency coronary artery bypass grafting\n"
                    "E) Calcium channel blocker"
                ),
                "expected": "C",
                "topic": "cardiology / STEMI management",
            },
            {
                "id": "medqa_002",
                "prompt": (
                    "A 28-year-old woman with a history of asthma presents with acute onset wheezing, "
                    "urticaria, and hypotension 10 minutes after eating peanuts. "
                    "Blood pressure is 80/50 mmHg, heart rate is 120 bpm. "
                    "What is the first-line treatment?\n\n"
                    "A) IV diphenhydramine\n"
                    "B) IV corticosteroids\n"
                    "C) Intramuscular epinephrine\n"
                    "D) Nebulised salbutamol\n"
                    "E) IV normal saline bolus only"
                ),
                "expected": "C",
                "topic": "anaphylaxis management",
            },
            {
                "id": "medqa_003",
                "prompt": (
                    "A 60-year-old man with type 2 diabetes and CKD stage 3 (eGFR 38 mL/min) "
                    "needs improved glycaemic control. His HbA1c is 9.2%. "
                    "Which medication is CONTRAINDICATED in this patient?\n\n"
                    "A) Insulin glargine\n"
                    "B) Sitagliptin\n"
                    "C) Metformin at full dose\n"
                    "D) Empagliflozin (with dose adjustment)\n"
                    "E) Linagliptin"
                ),
                "expected": "C",
                "topic": "pharmacology / diabetes + CKD",
            },
            {
                "id": "medqa_004",
                "prompt": (
                    "A 3-year-old boy is brought in by his parents for a barky, 'seal-like' cough "
                    "that worsens at night. He has a low-grade fever and inspiratory stridor. "
                    "A lateral neck X-ray shows the 'steeple sign'. "
                    "What is the most likely diagnosis?\n\n"
                    "A) Epiglottitis\n"
                    "B) Foreign body aspiration\n"
                    "C) Croup (laryngotracheobronchitis)\n"
                    "D) Peritonsillar abscess\n"
                    "E) Bacterial tracheitis"
                ),
                "expected": "C",
                "topic": "paediatrics / croup",
            },
            {
                "id": "medqa_005",
                "prompt": (
                    "A 55-year-old woman presents with a 2-cm mass in the right breast. "
                    "Core biopsy confirms invasive ductal carcinoma: ER+, PR+, HER2-. "
                    "Axillary lymph nodes are negative on sentinel node biopsy. "
                    "Which adjuvant systemic therapy is most appropriate?\n\n"
                    "A) Trastuzumab\n"
                    "B) Tamoxifen or aromatase inhibitor\n"
                    "C) CHOP chemotherapy regimen\n"
                    "D) Bevacizumab\n"
                    "E) No systemic therapy required"
                ),
                "expected": "B",
                "topic": "oncology / breast cancer",
            },
            {
                "id": "medqa_006",
                "prompt": (
                    "A 70-year-old man develops fever, productive cough, and right lower lobe "
                    "consolidation on chest X-ray 5 days after elective hip replacement surgery. "
                    "Sputum Gram stain shows Gram-positive cocci in clusters. "
                    "Blood cultures grow MRSA. "
                    "Which antibiotic is most appropriate?\n\n"
                    "A) Amoxicillin-clavulanate\n"
                    "B) Ciprofloxacin\n"
                    "C) Vancomycin\n"
                    "D) Cephalexin\n"
                    "E) Piperacillin-tazobactam"
                ),
                "expected": "C",
                "topic": "infectious disease / MRSA",
            },
            {
                "id": "medqa_007",
                "prompt": (
                    "A 25-year-old man presents with photophobia, neck stiffness, fever (39.5°C), "
                    "and a non-blanching petechial rash. Lumbar puncture shows cloudy CSF with "
                    "neutrophilia, elevated protein, and low glucose. "
                    "What is the most important immediate action?\n\n"
                    "A) Wait for CSF culture results before starting antibiotics\n"
                    "B) IV ceftriaxone immediately\n"
                    "C) Oral amoxicillin\n"
                    "D) CT head before any treatment\n"
                    "E) IV acyclovir only"
                ),
                "expected": "B",
                "topic": "neurology / bacterial meningitis",
            },
            {
                "id": "medqa_008",
                "prompt": (
                    "A 40-year-old woman presents with fatigue, weight gain, constipation, "
                    "cold intolerance, and dry skin over several months. "
                    "TSH is 18 mIU/L (normal 0.4–4.0), free T4 is low. "
                    "Anti-TPO antibodies are markedly elevated. "
                    "What is the most likely diagnosis?\n\n"
                    "A) Graves' disease\n"
                    "B) Subacute thyroiditis\n"
                    "C) Secondary hypothyroidism\n"
                    "D) Hashimoto's thyroiditis\n"
                    "E) Thyroid lymphoma"
                ),
                "expected": "D",
                "topic": "endocrinology / Hashimoto's",
            },
            {
                "id": "medqa_009",
                "prompt": (
                    "A 65-year-old man with a 40 pack-year smoking history presents with haemoptysis, "
                    "a 5-kg weight loss, and a 3-cm spiculated right upper lobe mass on CT. "
                    "Bronchoscopy biopsy shows small cell carcinoma. "
                    "Staging shows disseminated disease (bone, liver). "
                    "What is the primary treatment modality?\n\n"
                    "A) Surgical resection followed by radiotherapy\n"
                    "B) Platinum-based chemotherapy\n"
                    "C) Targeted therapy with erlotinib\n"
                    "D) Immunotherapy with pembrolizumab alone\n"
                    "E) Palliative radiotherapy to the primary only"
                ),
                "expected": "B",
                "topic": "oncology / SCLC",
            },
            {
                "id": "medqa_010",
                "prompt": (
                    "A 22-year-old college student presents with fever, sore throat, "
                    "cervical lymphadenopathy, and fatigue for 10 days. "
                    "Examination reveals splenomegaly. "
                    "Monospot test is positive. "
                    "Which complication should most concern you?\n\n"
                    "A) Meningitis\n"
                    "B) Splenic rupture\n"
                    "C) Acute kidney injury\n"
                    "D) Pulmonary embolism\n"
                    "E) Agranulocytosis"
                ),
                "expected": "B",
                "topic": "infectious disease / EBV/mono",
            },
            {
                "id": "medqa_011",
                "prompt": (
                    "A 30-year-old woman at 28 weeks gestation is found to have blood pressure "
                    "of 158/102 mmHg on two occasions 6 hours apart. Urinalysis shows 3+ protein. "
                    "She denies headache or visual changes. "
                    "Which of the following is the DEFINITIVE treatment for her condition?\n\n"
                    "A) Bed rest and antihypertensives until term\n"
                    "B) Magnesium sulphate infusion\n"
                    "C) Delivery of the fetus\n"
                    "D) Low-dose aspirin\n"
                    "E) IV hydralazine alone"
                ),
                "expected": "C",
                "topic": "obstetrics / preeclampsia",
            },
            {
                "id": "medqa_012",
                "prompt": (
                    "A 50-year-old man with alcoholic cirrhosis presents with sudden onset "
                    "haematemesis. Endoscopy reveals bleeding oesophageal varices. "
                    "After initial resuscitation, which pharmacological agent reduces portal "
                    "hypertension and should be started immediately?\n\n"
                    "A) Adrenaline injection\n"
                    "B) Terlipressin\n"
                    "C) Furosemide\n"
                    "D) Propranolol\n"
                    "E) Spironolactone"
                ),
                "expected": "B",
                "topic": "gastroenterology / variceal bleeding",
            },
            {
                "id": "medqa_013",
                "prompt": (
                    "A 48-year-old man is brought to the ER with sudden severe headache "
                    "described as 'the worst headache of my life', onset during exertion. "
                    "Neurological exam is normal. CT head is negative for blood. "
                    "What is the next most important diagnostic step?\n\n"
                    "A) MRI brain with gadolinium\n"
                    "B) Lumbar puncture for xanthochromia\n"
                    "C) EEG\n"
                    "D) Carotid Doppler ultrasound\n"
                    "E) Discharge with analgesia"
                ),
                "expected": "B",
                "topic": "neurology / SAH",
            },
            {
                "id": "medqa_014",
                "prompt": (
                    "A 7-year-old boy presents with generalised oedema, frothy urine, "
                    "and serum albumin of 1.8 g/dL. Urinalysis shows 4+ protein, no haematuria. "
                    "Renal biopsy shows normal light microscopy, no immune deposits on "
                    "immunofluorescence. "
                    "What is the first-line treatment?\n\n"
                    "A) Cyclophosphamide\n"
                    "B) Rituximab\n"
                    "C) Oral prednisolone\n"
                    "D) ACE inhibitor alone\n"
                    "E) Plasmapheresis"
                ),
                "expected": "C",
                "topic": "nephrology / minimal change disease",
            },
            {
                "id": "medqa_015",
                "prompt": (
                    "A 35-year-old woman presents with episodic hypertension (BP 200/110), "
                    "palpitations, diaphoresis, and severe headache. "
                    "24-hour urine shows markedly elevated catecholamines and metanephrines. "
                    "CT abdomen reveals a 4-cm right adrenal mass. "
                    "Before surgical resection, which medication must be started first?\n\n"
                    "A) Beta-blocker (propranolol)\n"
                    "B) ACE inhibitor\n"
                    "C) Alpha-blocker (phenoxybenzamine)\n"
                    "D) Calcium channel blocker\n"
                    "E) IV magnesium"
                ),
                "expected": "C",
                "topic": "endocrinology / phaeochromocytoma",
            },
            {
                "id": "medqa_016",
                "prompt": (
                    "A 68-year-old woman with atrial fibrillation is on warfarin (INR target 2–3). "
                    "She presents with frank haematuria and her INR is 7.2. She is haemodynamically "
                    "stable with no active major bleeding. "
                    "What is the most appropriate management?\n\n"
                    "A) Emergency fresh frozen plasma\n"
                    "B) IV vitamin K 10 mg\n"
                    "C) Hold warfarin and give oral vitamin K 1–5 mg\n"
                    "D) Idarucizumab\n"
                    "E) No intervention; recheck INR in 48 hours"
                ),
                "expected": "C",
                "topic": "haematology / warfarin reversal",
            },
            {
                "id": "medqa_017",
                "prompt": (
                    "A 52-year-old man presents with progressive bilateral proximal muscle weakness. "
                    "He has difficulty rising from a chair and raising his arms above his head. "
                    "Serum CK is 4,500 U/L. EMG shows myopathic changes. "
                    "Muscle biopsy shows perifascicular atrophy with CD4+ T-cell infiltrates. "
                    "What is the most likely diagnosis?\n\n"
                    "A) Inclusion body myositis\n"
                    "B) Duchenne muscular dystrophy\n"
                    "C) Dermatomyositis\n"
                    "D) Lambert-Eaton myasthenic syndrome\n"
                    "E) Hypothyroid myopathy"
                ),
                "expected": "C",
                "topic": "rheumatology / inflammatory myopathy",
            },
            {
                "id": "medqa_018",
                "prompt": (
                    "A 19-year-old woman presents with recurrent episodes of binge eating followed "
                    "by self-induced vomiting for 2 years. BMI is 21 kg/m². "
                    "Labs show hypokalaemia and metabolic alkalosis. "
                    "Dental enamel erosion is noted. "
                    "Which pharmacotherapy has the strongest evidence for this condition?\n\n"
                    "A) Bupropion\n"
                    "B) Fluoxetine\n"
                    "C) Olanzapine\n"
                    "D) Lithium\n"
                    "E) Naltrexone"
                ),
                "expected": "B",
                "topic": "psychiatry / bulimia nervosa pharmacotherapy",
            },
            {
                "id": "medqa_019",
                "prompt": (
                    "A 5-day-old neonate develops bilious vomiting and abdominal distension. "
                    "Plain abdominal X-ray shows a 'double bubble' sign with no distal gas. "
                    "The infant has trisomy 21. "
                    "What is the most likely diagnosis?\n\n"
                    "A) Pyloric stenosis\n"
                    "B) Midgut volvulus\n"
                    "C) Duodenal atresia\n"
                    "D) Hirschsprung's disease\n"
                    "E) Meconium ileus"
                ),
                "expected": "C",
                "topic": "paediatric surgery / duodenal atresia",
            },
            {
                "id": "medqa_020",
                "prompt": (
                    "A 72-year-old man presents with a gradual decline in cognition over 3 years. "
                    "His family reports personality changes and he has developed a resting tremor, "
                    "bradykinesia, and rigidity. Neuropsychological testing confirms dementia. "
                    "Post-mortem would most likely reveal which pathological finding?\n\n"
                    "A) Neurofibrillary tangles and amyloid plaques\n"
                    "B) TDP-43 inclusions\n"
                    "C) Lewy bodies in the substantia nigra and cortex\n"
                    "D) Spongiform change with prion protein deposition\n"
                    "E) Pick bodies in the frontal lobe"
                ),
                "expected": "C",
                "topic": "neurology / Lewy body dementia",
            },
        ]

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def _extract_choice(self, response: str) -> Optional[str]:
        """Extract the letter choice (A–E) from the response."""
        # Priority 1: explicit patterns like "Answer: B" or "The answer is C"
        for pattern in [
            r'(?i)(?:answer\s*(?:is|:)\s*)([A-E])\b',
            r'(?i)(?:i\s*(?:choose|select|pick)\s*)([A-E])\b',
            r'(?i)(?:correct\s*(?:answer|choice|option)\s*(?:is|:)\s*)([A-E])\b',
            r'(?i)(?:^|\s)([A-E])\s*(?:is correct|is the best|is the answer)',
        ]:
            match = re.search(pattern, response)
            if match:
                return match.group(1).upper()

        # Priority 2: standalone letter at the very start of the response
        start_match = re.match(r'^\s*([A-E])\s*[\.\):]', response)
        if start_match:
            return start_match.group(1).upper()

        # Priority 3: first standalone A–E anywhere in the response
        general_match = re.search(r'\b([A-E])\b', response)
        if general_match:
            return general_match.group(1).upper()

        return None

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score 1.0 for correct letter choice, 0.0 otherwise."""
        if not response or not response.strip():
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"error": "empty response"},
            }

        expected: str = prompt_data.get("expected", "")
        extracted = self._extract_choice(response)
        correct = extracted == expected.upper() if extracted else False

        return {
            "success": correct,
            "score": 1.0 if correct else 0.0,
            "metadata": {
                "expected": expected,
                "extracted_choice": extracted,
                "topic": prompt_data.get("topic", ""),
            },
        }
