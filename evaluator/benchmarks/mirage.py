"""MIRAGE benchmark - medical RAG evaluation with distractor passages."""

from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


class MIRAGEBenchmark(Benchmark):
    """MIRAGE - medical retrieval-augmented generation evaluation."""

    def __init__(self):
        config = BenchmarkConfig(
            name="mirage",
            description="Medical RAG evaluation with clinical passages and distractors",
            category="rag",
            version="1.0",
            timeout=90,
            max_tokens=1024,
            temperature=0.1,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        """Load 20 medical RAG evaluation tasks."""
        self.prompts = [
            {
                "id": "mirage_001",
                "context_passage": (
                    "Metformin is the first-line pharmacological treatment for type 2 diabetes mellitus "
                    "in adults without contraindications. It works primarily by reducing hepatic glucose "
                    "production and improving peripheral insulin sensitivity. Common adverse effects include "
                    "gastrointestinal upset such as nausea and diarrhoea, particularly at treatment initiation. "
                    "Metformin is contraindicated in patients with an eGFR below 30 mL/min/1.73 m² due to "
                    "the risk of lactic acidosis. Dosing typically starts at 500 mg twice daily and is "
                    "titrated up to a maximum of 2,000–2,550 mg per day."
                ),
                "distractor_passage": (
                    "Insulin therapy remains an important option for glycaemic control in type 2 diabetes "
                    "when oral agents are insufficient. Basal insulin analogues such as glargine and detemir "
                    "provide stable 24-hour coverage. Injection site rotation is essential to prevent "
                    "lipohypertrophy. Hypoglycaemia is the most common adverse effect of insulin therapy."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: At what eGFR threshold is metformin contraindicated, and why?"
                ),
                "expected": "Metformin is contraindicated when eGFR is below 30 mL/min/1.73 m² due to the risk of lactic acidosis.",
                "correct_source": "context",
                "answer_keywords": ["30", "egfr", "lactic acidosis", "contraindicated"],
                "distractor_keywords": ["insulin", "glargine", "hypoglycaemia", "basal"],
            },
            {
                "id": "mirage_002",
                "context_passage": (
                    "Warfarin acts by inhibiting vitamin K epoxide reductase, thereby blocking the "
                    "synthesis of vitamin K-dependent clotting factors II, VII, IX, and X, as well as "
                    "the anticoagulant proteins C and S. Its anticoagulant effect is monitored using the "
                    "international normalised ratio (INR). The therapeutic INR range for most indications "
                    "such as atrial fibrillation and venous thromboembolism is 2.0–3.0. Foods high in "
                    "vitamin K, such as leafy green vegetables, can significantly reduce warfarin's "
                    "effectiveness and must be consumed consistently."
                ),
                "distractor_passage": (
                    "Direct oral anticoagulants (DOACs) such as rivaroxaban and apixaban do not require "
                    "routine INR monitoring. They have predictable pharmacokinetics and fewer food "
                    "interactions than warfarin. DOACs are now preferred over warfarin for non-valvular "
                    "atrial fibrillation in most guidelines."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What is the therapeutic INR range for warfarin in atrial fibrillation, "
                    "and what dietary factor can reduce its effectiveness?"
                ),
                "expected": "The therapeutic INR range is 2.0–3.0. Foods high in vitamin K, such as leafy green vegetables, can reduce warfarin's effectiveness.",
                "correct_source": "context",
                "answer_keywords": ["2.0", "3.0", "vitamin k", "inr"],
                "distractor_keywords": ["rivaroxaban", "apixaban", "doac", "monitoring"],
            },
            {
                "id": "mirage_003",
                "context_passage": (
                    "Acute myocardial infarction (AMI) presenting with ST-elevation (STEMI) requires "
                    "emergent reperfusion therapy. Primary percutaneous coronary intervention (PCI) is "
                    "the preferred reperfusion strategy when it can be performed within 120 minutes of "
                    "first medical contact. If timely PCI is not available, fibrinolytic therapy should "
                    "be administered within 30 minutes of hospital arrival. Aspirin 300 mg loading dose "
                    "should be given immediately upon diagnosis unless contraindicated."
                ),
                "distractor_passage": (
                    "Stable angina is managed with lifestyle modification and pharmacotherapy including "
                    "beta-blockers, long-acting nitrates, and calcium channel blockers. Coronary angiography "
                    "is reserved for patients with refractory symptoms or high-risk features on non-invasive "
                    "testing. Exercise stress testing is a common initial investigation."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What is the maximum time window for primary PCI in STEMI, and what "
                    "alternative reperfusion therapy should be used if PCI is unavailable?"
                ),
                "expected": "Primary PCI should be performed within 120 minutes of first medical contact. If PCI is unavailable, fibrinolytic therapy should be given within 30 minutes of hospital arrival.",
                "correct_source": "context",
                "answer_keywords": ["120 minutes", "fibrinolytic", "pci", "30 minutes"],
                "distractor_keywords": ["stable angina", "beta-blocker", "stress testing", "nitrate"],
            },
            {
                "id": "mirage_004",
                "context_passage": (
                    "Community-acquired pneumonia (CAP) severity should be assessed using validated tools "
                    "such as the CURB-65 score, which assigns one point each for: Confusion, Urea >7 mmol/L, "
                    "Respiratory rate ≥30/min, Blood pressure (systolic <90 or diastolic ≤60 mmHg), and age "
                    "≥65 years. A score of 0–1 suggests low severity suitable for outpatient treatment; "
                    "2 indicates moderate severity requiring hospitalisation; and 3–5 indicates high severity "
                    "with consideration of ICU admission."
                ),
                "distractor_passage": (
                    "Hospital-acquired pneumonia (HAP) typically involves resistant organisms such as "
                    "Pseudomonas aeruginosa and methicillin-resistant Staphylococcus aureus (MRSA). "
                    "Empirical antibiotic therapy for HAP should include anti-pseudomonal agents. "
                    "Bronchoalveolar lavage may be used to guide microbiological diagnosis."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What does a CURB-65 score of 2 indicate, and what management is recommended?"
                ),
                "expected": "A CURB-65 score of 2 indicates moderate severity CAP and requires hospitalisation.",
                "correct_source": "context",
                "answer_keywords": ["2", "moderate", "hospitalisation", "curb-65"],
                "distractor_keywords": ["pseudomonas", "mrsa", "hap", "bronchoalveolar"],
            },
            {
                "id": "mirage_005",
                "context_passage": (
                    "Anaphylaxis is a severe, life-threatening systemic hypersensitivity reaction. "
                    "The first-line treatment is intramuscular adrenaline (epinephrine) 0.5 mg (1:1000 "
                    "concentration) administered into the anterolateral thigh. This may be repeated after "
                    "5 minutes if there is no improvement. Patients should be placed in a supine position "
                    "with legs elevated unless they have respiratory compromise, in which case they should "
                    "sit up. Intravenous fluids are given for haemodynamic instability."
                ),
                "distractor_passage": (
                    "Allergic rhinitis is managed with intranasal corticosteroids as first-line therapy. "
                    "Antihistamines provide symptomatic relief. Allergen immunotherapy can reduce sensitivity "
                    "over time. Oral corticosteroids are reserved for severe exacerbations."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What is the first-line treatment for anaphylaxis, what dose is used, "
                    "and at what site is it administered?"
                ),
                "expected": "First-line treatment is intramuscular adrenaline (epinephrine) 0.5 mg (1:1000) given into the anterolateral thigh.",
                "correct_source": "context",
                "answer_keywords": ["adrenaline", "epinephrine", "0.5 mg", "anterolateral thigh", "intramuscular"],
                "distractor_keywords": ["rhinitis", "antihistamine", "immunotherapy", "corticosteroid"],
            },
            {
                "id": "mirage_006",
                "context_passage": (
                    "Chronic obstructive pulmonary disease (COPD) is characterised by persistent airflow "
                    "limitation that is not fully reversible. The diagnosis requires post-bronchodilator "
                    "spirometry showing a FEV1/FVC ratio of less than 0.70. COPD severity is staged by "
                    "the GOLD classification based on FEV1 % predicted: GOLD 1 (mild) ≥80%, GOLD 2 "
                    "(moderate) 50–79%, GOLD 3 (severe) 30–49%, and GOLD 4 (very severe) <30%. "
                    "Long-acting bronchodilators are the cornerstone of maintenance therapy."
                ),
                "distractor_passage": (
                    "Asthma is characterised by variable airflow obstruction and airway hyperresponsiveness. "
                    "Unlike COPD, asthma typically shows significant reversibility on spirometry. "
                    "Inhaled corticosteroids are the mainstay of long-term asthma control. Step-up "
                    "therapy follows national guidelines such as the BTS/SIGN asthma guidelines."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What spirometry finding confirms a COPD diagnosis, and what FEV1 % "
                    "predicted defines GOLD stage 3 (severe) COPD?"
                ),
                "expected": "A post-bronchodilator FEV1/FVC ratio below 0.70 confirms COPD. GOLD stage 3 (severe) corresponds to FEV1 30–49% predicted.",
                "correct_source": "context",
                "answer_keywords": ["fev1/fvc", "0.70", "30", "49", "gold 3", "severe"],
                "distractor_keywords": ["asthma", "reversibility", "inhaled corticosteroid", "bts"],
            },
            {
                "id": "mirage_007",
                "context_passage": (
                    "Hypertensive emergency is defined as severely elevated blood pressure (typically "
                    "≥180/120 mmHg) with evidence of acute target-organ damage, such as hypertensive "
                    "encephalopathy, acute left ventricular failure, or aortic dissection. Management "
                    "requires controlled reduction of blood pressure in an intensive care setting. The "
                    "mean arterial pressure should be reduced by no more than 25% in the first hour to "
                    "avoid precipitating ischaemia in vital organs."
                ),
                "distractor_passage": (
                    "Hypertensive urgency refers to severely elevated blood pressure without acute "
                    "target-organ damage. It can often be managed in the outpatient setting with oral "
                    "antihypertensives and close follow-up. Lifestyle modifications including sodium "
                    "restriction and weight loss are important adjuncts."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What distinguishes a hypertensive emergency from urgency, and by how much "
                    "should blood pressure be reduced in the first hour?"
                ),
                "expected": "A hypertensive emergency involves severely elevated BP with acute target-organ damage, unlike urgency which lacks organ damage. The mean arterial pressure should be reduced by no more than 25% in the first hour.",
                "correct_source": "context",
                "answer_keywords": ["target-organ damage", "25%", "first hour", "emergency"],
                "distractor_keywords": ["outpatient", "urgency", "sodium restriction", "lifestyle"],
            },
            {
                "id": "mirage_008",
                "context_passage": (
                    "Sepsis is defined as life-threatening organ dysfunction caused by a dysregulated host "
                    "response to infection. According to the Sepsis-3 definition, organ dysfunction is "
                    "identified by an acute increase in the SOFA score of ≥2 points. Septic shock is a "
                    "subset of sepsis with circulatory and cellular/metabolic abnormalities, characterised "
                    "by the need for vasopressors to maintain a mean arterial pressure ≥65 mmHg and a "
                    "serum lactate >2 mmol/L despite adequate fluid resuscitation."
                ),
                "distractor_passage": (
                    "The systemic inflammatory response syndrome (SIRS) criteria include tachycardia, "
                    "tachypnoea, abnormal temperature, and leucocyte count abnormalities. SIRS was used "
                    "in older definitions of sepsis but has been replaced by SOFA-based criteria due to "
                    "its lack of specificity for infection-driven organ dysfunction."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: According to Sepsis-3, what lactate level and vasopressor requirement "
                    "define septic shock?"
                ),
                "expected": "Septic shock requires vasopressors to maintain MAP ≥65 mmHg and serum lactate >2 mmol/L despite adequate fluid resuscitation.",
                "correct_source": "context",
                "answer_keywords": ["lactate", "2 mmol", "65 mmhg", "vasopressor", "map"],
                "distractor_keywords": ["sirs", "tachycardia", "tachypnoea", "leucocyte"],
            },
            {
                "id": "mirage_009",
                "context_passage": (
                    "Pulmonary embolism (PE) risk stratification using the Wells score assigns points for "
                    "clinical signs of DVT (3), alternative diagnosis less likely than PE (3), heart rate "
                    ">100 bpm (1.5), immobilisation/surgery in prior 4 weeks (1.5), previous DVT/PE (1.5), "
                    "haemoptysis (1), and malignancy (1). A Wells score ≤4 indicates low-to-moderate "
                    "probability; a score >4 indicates high probability. In low-probability patients, a "
                    "negative D-dimer effectively excludes PE."
                ),
                "distractor_passage": (
                    "CT pulmonary angiography (CTPA) is the imaging gold standard for diagnosing PE. "
                    "V/Q scanning is an alternative in patients with contrast allergy or renal impairment. "
                    "Echocardiography can assess right heart strain as a prognostic tool but is not "
                    "routinely used for PE diagnosis."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: How many points does a Wells score assign for clinical signs of DVT, and "
                    "what test can exclude PE in low-probability patients?"
                ),
                "expected": "Clinical signs of DVT score 3 points on the Wells score. A negative D-dimer effectively excludes PE in low-probability patients.",
                "correct_source": "context",
                "answer_keywords": ["3 points", "d-dimer", "low probability", "dvt"],
                "distractor_keywords": ["ctpa", "v/q", "echocardiography", "contrast"],
            },
            {
                "id": "mirage_010",
                "context_passage": (
                    "Beta-blocker overdose can cause bradycardia, hypotension, and heart block. Initial "
                    "management includes atropine for bradycardia. High-dose insulin euglycaemic therapy "
                    "(HIET) is a key treatment, using insulin infusions of 1 unit/kg/hr or more alongside "
                    "dextrose to maintain normoglycaemia. Glucagon 5–10 mg IV bolus can restore heart rate "
                    "and blood pressure by bypassing beta-receptor blockade. Lipid emulsion therapy may "
                    "be used as a rescue agent."
                ),
                "distractor_passage": (
                    "Calcium channel blocker overdose presents similarly to beta-blocker toxicity with "
                    "bradycardia and hypotension, but may additionally cause hyperglycaemia. Calcium "
                    "chloride or calcium gluconate is a specific antidote. HIET is also used for calcium "
                    "channel blocker toxicity. The management approach may differ in the type of CCB involved."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What is the dose of glucagon used in beta-blocker overdose, and what is "
                    "its mechanism of action in this context?"
                ),
                "expected": "Glucagon is given as a 5–10 mg IV bolus in beta-blocker overdose. It works by bypassing beta-receptor blockade to restore heart rate and blood pressure.",
                "correct_source": "context",
                "answer_keywords": ["glucagon", "5", "10 mg", "bypass", "beta-receptor"],
                "distractor_keywords": ["calcium chloride", "calcium gluconate", "hyperglycaemia", "ccb"],
            },
            {
                "id": "mirage_011",
                "context_passage": (
                    "Diabetic ketoacidosis (DKA) is characterised by the triad of hyperglycaemia "
                    "(blood glucose >11 mmol/L), ketonaemia or ketonuria, and metabolic acidosis (pH "
                    "<7.3 or bicarbonate <15 mmol/L). Initial management involves intravenous 0.9% sodium "
                    "chloride at 1 litre over the first hour. Fixed-rate insulin infusion at 0.1 unit/kg/hr "
                    "is started after the first fluid bolus. Potassium replacement is essential because "
                    "insulin therapy shifts potassium intracellularly, risking hypokalaemia."
                ),
                "distractor_passage": (
                    "Hyperosmolar hyperglycaemic state (HHS) occurs mainly in type 2 diabetes and is "
                    "characterised by severe hyperglycaemia (often >30 mmol/L), hyperosmolarity, and "
                    "dehydration without significant ketosis or acidosis. Fluid replacement is the "
                    "cornerstone of management; insulin is used cautiously."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: Why is potassium replacement essential in DKA management?"
                ),
                "expected": "Potassium replacement is essential because insulin therapy shifts potassium intracellularly, which can cause dangerous hypokalaemia.",
                "correct_source": "context",
                "answer_keywords": ["potassium", "insulin", "intracellularly", "hypokalaemia"],
                "distractor_keywords": ["hhs", "hyperosmolar", "type 2", "osmolarity"],
            },
            {
                "id": "mirage_012",
                "context_passage": (
                    "Ischaemic stroke management within the first 4.5 hours of symptom onset includes "
                    "intravenous thrombolysis with alteplase 0.9 mg/kg (maximum 90 mg), with 10% given "
                    "as a bolus over 1 minute and the rest over 60 minutes. Mechanical thrombectomy is "
                    "indicated for large vessel occlusion and can be performed up to 24 hours from symptom "
                    "onset in selected patients. Aspirin 300 mg should be given 24 hours after thrombolysis "
                    "or immediately if thrombolysis is not given."
                ),
                "distractor_passage": (
                    "Haemorrhagic stroke management focuses on supportive care, blood pressure control, "
                    "and reversal of anticoagulation if applicable. Surgical intervention may be needed "
                    "for large haematomas causing mass effect. Thrombolysis is absolutely contraindicated "
                    "in haemorrhagic stroke."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What is the time window for IV alteplase in ischaemic stroke and what "
                    "is the maximum dose?"
                ),
                "expected": "IV alteplase must be given within 4.5 hours of symptom onset. The maximum dose is 90 mg (0.9 mg/kg).",
                "correct_source": "context",
                "answer_keywords": ["4.5 hours", "alteplase", "90 mg", "0.9 mg/kg"],
                "distractor_keywords": ["haemorrhagic", "anticoagulation", "haematoma", "contraindicated"],
            },
            {
                "id": "mirage_013",
                "context_passage": (
                    "Clostridium difficile infection (CDI) is the leading cause of antibiotic-associated "
                    "diarrhoea. First-line treatment for a non-severe initial episode is oral vancomycin "
                    "125 mg four times daily for 10 days, or fidaxomicin 200 mg twice daily for 10 days. "
                    "Metronidazole is no longer recommended as first-line therapy. Contact precautions and "
                    "hand hygiene with soap and water (not alcohol gel, which is ineffective against "
                    "C. diff spores) are essential infection control measures."
                ),
                "distractor_passage": (
                    "Irritable bowel syndrome (IBS) is a functional gastrointestinal disorder characterised "
                    "by abdominal pain and altered bowel habits without structural abnormality. Management "
                    "includes dietary modification, fibre supplementation, and antispasmodic agents. "
                    "Psychological therapies such as cognitive behavioural therapy may also be beneficial."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: Why is alcohol gel ineffective for C. difficile infection control, and "
                    "what is the first-line antibiotic treatment?"
                ),
                "expected": "Alcohol gel is ineffective against C. diff spores. First-line treatment is oral vancomycin 125 mg four times daily or fidaxomicin 200 mg twice daily for 10 days.",
                "correct_source": "context",
                "answer_keywords": ["spores", "alcohol gel", "vancomycin", "fidaxomicin"],
                "distractor_keywords": ["irritable bowel", "ibs", "antispasmodic", "fibre"],
            },
            {
                "id": "mirage_014",
                "context_passage": (
                    "Lithium is a mood stabiliser used in bipolar disorder. Its therapeutic window is "
                    "narrow: target serum levels are 0.6–1.0 mmol/L for maintenance therapy. Signs of "
                    "toxicity (levels >1.5 mmol/L) include tremor, ataxia, confusion, nausea, and, in "
                    "severe cases, seizures and cardiac arrhythmias. NSAIDs, ACE inhibitors, and thiazide "
                    "diuretics can raise lithium levels by reducing renal clearance and must be used with "
                    "caution or avoided."
                ),
                "distractor_passage": (
                    "Sodium valproate is an anticonvulsant and mood stabiliser used for epilepsy and "
                    "bipolar disorder. It is teratogenic and must not be used in women of childbearing "
                    "potential without a pregnancy prevention programme. Common side effects include "
                    "weight gain, hair loss, and tremor. Liver function tests should be monitored."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What drug classes can increase lithium toxicity risk, and at what serum "
                    "level does toxicity typically manifest?"
                ),
                "expected": "NSAIDs, ACE inhibitors, and thiazide diuretics can raise lithium levels and increase toxicity risk. Toxicity typically occurs at levels above 1.5 mmol/L.",
                "correct_source": "context",
                "answer_keywords": ["nsaid", "ace inhibitor", "thiazide", "1.5 mmol"],
                "distractor_keywords": ["valproate", "teratogenic", "epilepsy", "liver"],
            },
            {
                "id": "mirage_015",
                "context_passage": (
                    "Acute kidney injury (AKI) is defined by the KDIGO criteria as any of: increase in "
                    "serum creatinine ≥26.5 µmol/L within 48 hours; increase in serum creatinine to ≥1.5 "
                    "times baseline within 7 days; or urine output <0.5 mL/kg/hr for ≥6 hours. AKI is "
                    "staged 1–3 based on degree of creatinine rise and urine output reduction. All "
                    "nephrotoxic medications including NSAIDs, aminoglycosides, and contrast agents should "
                    "be withheld or used with caution."
                ),
                "distractor_passage": (
                    "Chronic kidney disease (CKD) is defined by persistent kidney damage or reduced GFR "
                    "for more than 3 months. It is staged G1–G5 based on eGFR. CKD is a major risk factor "
                    "for cardiovascular disease and progression to end-stage renal disease. ACE inhibitors "
                    "or ARBs are first-line antihypertensives in CKD with proteinuria."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: According to KDIGO criteria, what urine output threshold defines AKI, "
                    "and which medication class should be withheld?"
                ),
                "expected": "Urine output below 0.5 mL/kg/hr for 6 or more hours defines AKI by KDIGO criteria. NSAIDs (and other nephrotoxins such as aminoglycosides and contrast agents) should be withheld.",
                "correct_source": "context",
                "answer_keywords": ["0.5 ml/kg", "6 hours", "nsaid", "nephrotoxic"],
                "distractor_keywords": ["ckd", "gfr", "cardiovascular", "proteinuria"],
            },
            {
                "id": "mirage_016",
                "context_passage": (
                    "Rheumatoid arthritis (RA) is a chronic inflammatory joint disease managed with "
                    "disease-modifying antirheumatic drugs (DMARDs). Methotrexate is the anchor DMARD "
                    "and is initiated early after diagnosis. Patients must be counselled on the need for "
                    "folate supplementation (folic acid 5 mg weekly) to reduce methotrexate toxicity. "
                    "Regular monitoring of full blood count and liver function tests is mandatory. "
                    "Alcohol should be minimised due to additive hepatotoxicity risk."
                ),
                "distractor_passage": (
                    "Osteoarthritis (OA) is a degenerative joint disease managed with paracetamol and "
                    "topical NSAIDs as first-line therapy. Intra-articular steroid injections provide "
                    "short-term relief. Joint replacement surgery is the definitive treatment for severe "
                    "end-stage disease. Unlike RA, OA is not primarily inflammatory."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: Why is folic acid prescribed alongside methotrexate in rheumatoid arthritis, "
                    "and what lifestyle factor increases hepatotoxicity risk?"
                ),
                "expected": "Folic acid (5 mg weekly) reduces methotrexate toxicity. Alcohol increases hepatotoxicity risk due to additive effects with methotrexate.",
                "correct_source": "context",
                "answer_keywords": ["folic acid", "folate", "methotrexate toxicity", "alcohol", "hepatotoxicity"],
                "distractor_keywords": ["osteoarthritis", "paracetamol", "joint replacement", "steroid injection"],
            },
            {
                "id": "mirage_017",
                "context_passage": (
                    "Hypothyroidism is treated with levothyroxine. The initial dose in young otherwise "
                    "healthy adults is 1.6 µg/kg/day. In elderly patients or those with ischaemic heart "
                    "disease, treatment is started at a lower dose (25–50 µg/day) to avoid precipitating "
                    "angina or arrhythmia. Monitoring is by TSH levels, which should be checked 6–8 weeks "
                    "after any dose change. The target TSH for most patients is 0.5–2.5 mIU/L."
                ),
                "distractor_passage": (
                    "Hyperthyroidism caused by Graves' disease is managed with carbimazole, radioactive "
                    "iodine, or thyroidectomy. Block-and-replace regimens use high-dose carbimazole "
                    "combined with levothyroxine to maintain euthyroidism. Ophthalmopathy may require "
                    "specialist management."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: Why is levothyroxine started at a lower dose in elderly patients, and "
                    "how soon after a dose change should TSH be rechecked?"
                ),
                "expected": "Levothyroxine is started at a lower dose in elderly patients to avoid precipitating angina or arrhythmia. TSH should be rechecked 6–8 weeks after any dose change.",
                "correct_source": "context",
                "answer_keywords": ["angina", "arrhythmia", "6", "8 weeks", "tsh"],
                "distractor_keywords": ["carbimazole", "graves", "radioactive iodine", "ophthalmopathy"],
            },
            {
                "id": "mirage_018",
                "context_passage": (
                    "Paracetamol overdose causes hepatotoxicity through accumulation of the toxic "
                    "metabolite NAPQI when glutathione stores are depleted. The antidote is N-acetylcysteine "
                    "(NAC), which replenishes glutathione. NAC is most effective when given within 8–10 hours "
                    "of ingestion. The Rumack-Matthew nomogram is used to assess the need for NAC treatment "
                    "based on the paracetamol concentration and time since ingestion."
                ),
                "distractor_passage": (
                    "Opioid overdose is characterised by the triad of miosis, respiratory depression, "
                    "and reduced consciousness. Naloxone is the antidote and can be given intravenously, "
                    "intramuscularly, or intranasally. Repeated doses may be required due to naloxone's "
                    "short half-life relative to some opioids."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What toxic metabolite causes paracetamol-induced hepatotoxicity, and what "
                    "is the antidote?"
                ),
                "expected": "NAPQI is the toxic metabolite responsible for paracetamol hepatotoxicity when glutathione is depleted. The antidote is N-acetylcysteine (NAC).",
                "correct_source": "context",
                "answer_keywords": ["napqi", "n-acetylcysteine", "nac", "glutathione"],
                "distractor_keywords": ["naloxone", "opioid", "miosis", "respiratory depression"],
            },
            {
                "id": "mirage_019",
                "context_passage": (
                    "Heart failure with reduced ejection fraction (HFrEF) is defined by a left ventricular "
                    "ejection fraction (LVEF) below 40%. Evidence-based therapies that reduce mortality "
                    "include: ACE inhibitors or ARBs (or ARNI sacubitril/valsartan), beta-blockers, "
                    "mineralocorticoid receptor antagonists (MRAs) such as spironolactone, and SGLT2 "
                    "inhibitors. The 'four pillars' of HFrEF therapy together reduce all-cause mortality "
                    "by approximately 60–70% compared to placebo."
                ),
                "distractor_passage": (
                    "Heart failure with preserved ejection fraction (HFpEF) is defined by LVEF ≥50% "
                    "with evidence of diastolic dysfunction. Unlike HFrEF, no therapy has convincingly "
                    "reduced mortality in HFpEF. SGLT2 inhibitors have shown benefit in reducing "
                    "hospitalisations. Diuretics relieve congestion symptoms."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What LVEF threshold defines HFrEF and which four drug classes form the "
                    "pillars of its treatment?"
                ),
                "expected": "HFrEF is defined by LVEF below 40%. The four pillars are ACE inhibitors/ARBs (or ARNI), beta-blockers, MRAs (e.g. spironolactone), and SGLT2 inhibitors.",
                "correct_source": "context",
                "answer_keywords": ["40%", "ace inhibitor", "beta-blocker", "sglt2", "spironolactone"],
                "distractor_keywords": ["hfpef", "50%", "diastolic", "preserved"],
            },
            {
                "id": "mirage_020",
                "context_passage": (
                    "Tuberculosis (TB) treatment uses a standardised regimen for drug-sensitive disease. "
                    "The initial (intensive) phase lasts 2 months and uses four drugs: isoniazid (H), "
                    "rifampicin (R), pyrazinamide (Z), and ethambutol (E) — abbreviated 2HRZE. "
                    "The continuation phase lasts 4 months using isoniazid and rifampicin — abbreviated "
                    "4HR. Pyridoxine (vitamin B6) is co-prescribed with isoniazid to prevent peripheral "
                    "neuropathy."
                ),
                "distractor_passage": (
                    "Non-tuberculous mycobacteria (NTM) infections are caused by environmental mycobacteria "
                    "and do not require the same regimen as TB. Macrolide-based regimens are commonly used. "
                    "Infection control measures differ from TB as NTM is generally not transmissible "
                    "between humans."
                ),
                "prompt": (
                    "Using the provided medical passage, answer the following question:\n\n"
                    "Context passage: {context_passage}\n\n"
                    "Distractor passage: {distractor_passage}\n\n"
                    "Question: What drugs are used in the 2-month intensive phase of TB treatment, and "
                    "why is pyridoxine co-prescribed?"
                ),
                "expected": "The 2-month intensive phase uses isoniazid, rifampicin, pyrazinamide, and ethambutol (2HRZE). Pyridoxine is co-prescribed with isoniazid to prevent peripheral neuropathy.",
                "correct_source": "context",
                "answer_keywords": ["isoniazid", "rifampicin", "pyrazinamide", "ethambutol", "pyridoxine", "neuropathy"],
                "distractor_keywords": ["ntm", "macrolide", "environmental", "non-tuberculous"],
            },
        ]
        # Format the prompt text with passage content
        for item in self.prompts:
            item["prompt"] = item["prompt"].format(
                context_passage=item["context_passage"],
                distractor_passage=item["distractor_passage"],
            )

    def _response_uses_distractor(self, prompt_data: Dict[str, Any], response: str) -> bool:
        """Return True if the response appears to draw from the distractor passage."""
        response_lower = response.lower()
        distractor_keywords = prompt_data.get("distractor_keywords", [])
        hits = sum(1 for kw in distractor_keywords if kw.lower() in response_lower)
        return hits >= 2

    def _response_is_correct(self, prompt_data: Dict[str, Any], response: str) -> bool:
        """Return True if the response contains the key answer facts."""
        response_lower = response.lower()
        answer_keywords = prompt_data.get("answer_keywords", [])
        if not answer_keywords:
            return False
        hits = sum(1 for kw in answer_keywords if kw.lower() in response_lower)
        return hits / len(answer_keywords) >= 0.5

    def _response_is_partial(self, prompt_data: Dict[str, Any], response: str) -> bool:
        """Return True if the response is partially correct (some keywords present)."""
        response_lower = response.lower()
        answer_keywords = prompt_data.get("answer_keywords", [])
        if not answer_keywords:
            return False
        hits = sum(1 for kw in answer_keywords if kw.lower() in response_lower)
        ratio = hits / len(answer_keywords)
        return 0.25 <= ratio < 0.5

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score: 1.0 correct, 0.5 partial, 0.0 wrong or from distractor."""
        uses_distractor = self._response_uses_distractor(prompt_data, response)
        is_correct = self._response_is_correct(prompt_data, response)
        is_partial = self._response_is_partial(prompt_data, response)

        if uses_distractor and not is_correct:
            score = 0.0
            reason = "Response appears to draw from distractor passage"
        elif is_correct:
            score = 1.0
            reason = "Correct answer from context passage"
        elif is_partial:
            score = 0.5
            reason = "Partially correct answer"
        else:
            score = 0.0
            reason = "Incorrect or insufficient answer"

        return {
            "success": score == 1.0,
            "score": score,
            "metadata": {
                "uses_distractor": uses_distractor,
                "is_correct": is_correct,
                "is_partial": is_partial,
                "reason": reason,
                "prompt_id": prompt_data.get("id"),
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are a clinical information specialist. Answer the question using only the "
            "information in the context passage provided. Do not use the distractor passage "
            "or external knowledge. Be precise and cite specific values where relevant."
        )
