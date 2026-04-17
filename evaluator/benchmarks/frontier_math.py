"""Frontier Math benchmark - Research-level graduate mathematics problems."""

import re
from typing import Dict, Any, List
from .base import Benchmark, BenchmarkConfig


class FrontierMathBenchmark(Benchmark):
    """Frontier Math: graduate/research-level problems in abstract algebra,
    topology, real analysis, and number theory. Scoring is keyword-based,
    assessing whether the response uses the correct mathematical concepts."""

    def __init__(self):
        config = BenchmarkConfig(
            name="frontier_math",
            description=(
                "Research-level math: abstract algebra, topology, real analysis, "
                "number theory at graduate level"
            ),
            category="math",
            version="1.0",
            timeout=300,
            max_tokens=4096,
            temperature=0.0,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- Abstract Algebra (5 problems) ---
            {
                "id": "fmath_001",
                "prompt": (
                    "Prove that every finite group of prime order is cyclic. "
                    "Sketch the key steps of the proof and identify which theorem "
                    "about group order you rely on."
                ),
                "expected": "Every element (other than the identity) generates the group by Lagrange's theorem.",
                "expected_keywords": [
                    "lagrange", "prime", "cyclic", "generator", "order", "subgroup",
                    "divides", "identity",
                ],
                "domain": "abstract_algebra",
            },
            {
                "id": "fmath_002",
                "prompt": (
                    "State and prove the First Isomorphism Theorem for groups. "
                    "What is the relationship between the kernel, the image, and the "
                    "quotient group?"
                ),
                "expected": "G/ker(φ) ≅ im(φ), where the kernel is a normal subgroup.",
                "expected_keywords": [
                    "kernel", "image", "isomorphism", "normal", "quotient",
                    "homomorphism", "surjective", "bijection",
                ],
                "domain": "abstract_algebra",
            },
            {
                "id": "fmath_003",
                "prompt": (
                    "Describe the classification of finitely generated abelian groups. "
                    "Write down the structure theorem and give an example of a group "
                    "isomorphic to $\\mathbb{Z}_2 \\oplus \\mathbb{Z}_4 \\oplus \\mathbb{Z}$."
                ),
                "expected": "Direct sum of cyclic groups Z_{d_1} ⊕ ... ⊕ Z_{d_k} ⊕ Z^r with d_1 | d_2 | ... | d_k.",
                "expected_keywords": [
                    "cyclic", "direct sum", "invariant factor", "primary decomposition",
                    "torsion", "free", "rank",
                ],
                "domain": "abstract_algebra",
            },
            {
                "id": "fmath_004",
                "prompt": (
                    "Let $R$ be a commutative ring with unity. Define what it means for "
                    "an ideal $I$ to be prime and what it means to be maximal. "
                    "Prove that every maximal ideal is prime."
                ),
                "expected": "Maximal ideals are prime because R/I is a field implies R/I is an integral domain.",
                "expected_keywords": [
                    "prime ideal", "maximal ideal", "integral domain", "field",
                    "quotient ring", "zero divisor", "containment",
                ],
                "domain": "abstract_algebra",
            },
            {
                "id": "fmath_005",
                "prompt": (
                    "Explain Sylow's theorems. For a finite group $G$ with $|G| = p^a m$ "
                    "where $p \\nmid m$, what do the three Sylow theorems assert about "
                    "Sylow $p$-subgroups?"
                ),
                "expected": (
                    "Existence: a Sylow p-subgroup exists. "
                    "Conjugacy: all Sylow p-subgroups are conjugate. "
                    "Count: n_p ≡ 1 (mod p) and n_p | m."
                ),
                "expected_keywords": [
                    "sylow", "p-subgroup", "conjugate", "existence", "congruent",
                    "divides", "normalizer", "index",
                ],
                "domain": "abstract_algebra",
            },
            # --- Topology (4 problems) ---
            {
                "id": "fmath_006",
                "prompt": (
                    "State the definition of compactness for a topological space using "
                    "open covers. Prove that a closed subset of a compact space is compact."
                ),
                "expected": "Every open cover has a finite subcover; closed subsets inherit this.",
                "expected_keywords": [
                    "open cover", "finite subcover", "compact", "closed", "subset",
                    "complement", "intersection",
                ],
                "domain": "topology",
            },
            {
                "id": "fmath_007",
                "prompt": (
                    "State the Brouwer Fixed-Point Theorem for the $n$-disk $D^n$. "
                    "Sketch a proof for the case $n = 1$ using the Intermediate Value Theorem, "
                    "and explain why the general case requires algebraic topology."
                ),
                "expected": "Every continuous f: D^n -> D^n has a fixed point; n=1 via IVT; general case via homology/degree theory.",
                "expected_keywords": [
                    "fixed point", "continuous", "intermediate value", "homotopy",
                    "homology", "retraction", "degree", "disk",
                ],
                "domain": "topology",
            },
            {
                "id": "fmath_008",
                "prompt": (
                    "Define the fundamental group $\\pi_1(X, x_0)$ of a topological space. "
                    "Compute $\\pi_1(S^1, 1)$ and explain why it is isomorphic to $\\mathbb{Z}$."
                ),
                "expected": "π_1(S^1) ≅ Z via winding number; loops classified by homotopy classes.",
                "expected_keywords": [
                    "fundamental group", "loop", "homotopy", "winding number",
                    "isomorphic", "integer", "base point", "path",
                ],
                "domain": "topology",
            },
            {
                "id": "fmath_009",
                "prompt": (
                    "State Urysohn's Lemma and explain its significance in the context of "
                    "normal topological spaces. What does it guarantee about the existence "
                    "of continuous functions?"
                ),
                "expected": "In a normal space, disjoint closed sets can be separated by a continuous function to [0,1].",
                "expected_keywords": [
                    "urysohn", "normal", "closed sets", "disjoint", "continuous",
                    "separation", "function", "zero", "one",
                ],
                "domain": "topology",
            },
            # --- Real Analysis (4 problems) ---
            {
                "id": "fmath_010",
                "prompt": (
                    "State the Hahn-Banach Theorem for normed spaces. "
                    "What does it imply about the dual space of a normed vector space?"
                ),
                "expected": "Any bounded linear functional on a subspace extends to the whole space with preserved norm; dual space is rich.",
                "expected_keywords": [
                    "hahn-banach", "linear functional", "extension", "norm",
                    "subspace", "dual", "bounded", "dominated",
                ],
                "domain": "real_analysis",
            },
            {
                "id": "fmath_011",
                "prompt": (
                    "Define the Lebesgue integral and explain how it differs from the "
                    "Riemann integral. Give an example of a function that is Lebesgue "
                    "integrable but not Riemann integrable."
                ),
                "expected": "Lebesgue integrates with respect to measure; the Dirichlet function is L-integrable but not R-integrable.",
                "expected_keywords": [
                    "lebesgue", "riemann", "measure", "measurable", "simple function",
                    "dirichlet", "indicator", "almost everywhere",
                ],
                "domain": "real_analysis",
            },
            {
                "id": "fmath_012",
                "prompt": (
                    "State the Banach Fixed-Point (Contraction Mapping) Theorem. "
                    "Describe its hypotheses precisely and outline a proof sketch."
                ),
                "expected": "A contraction on a complete metric space has a unique fixed point, found by iterating the map.",
                "expected_keywords": [
                    "contraction", "complete", "metric space", "fixed point", "unique",
                    "lipschitz", "iteration", "cauchy",
                ],
                "domain": "real_analysis",
            },
            {
                "id": "fmath_013",
                "prompt": (
                    "Prove or disprove: if $f: \\mathbb{R} \\to \\mathbb{R}$ is measurable "
                    "and $f^2$ is integrable, then $f$ is integrable. "
                    "Provide a concrete counterexample if false."
                ),
                "expected": "False; f(x) = 1/sqrt(x) on (0,1] has f^2 integrable but f is not square-integrable in L^1.",
                "expected_keywords": [
                    "counterexample", "integrable", "measurable", "square",
                    "l1", "l2", "diverge", "unbounded",
                ],
                "domain": "real_analysis",
            },
            # --- Number Theory (4 problems) ---
            {
                "id": "fmath_014",
                "prompt": (
                    "State the Riemann Hypothesis. Describe its connection to the "
                    "distribution of prime numbers via the explicit formula linking "
                    "primes and zeros of $\\zeta(s)$."
                ),
                "expected": "All non-trivial zeros of ζ(s) have real part 1/2; zeros control error term in prime counting function.",
                "expected_keywords": [
                    "riemann hypothesis", "zeta function", "zeros", "critical strip",
                    "real part", "prime counting", "explicit formula", "nontrivial",
                ],
                "domain": "number_theory",
            },
            {
                "id": "fmath_015",
                "prompt": (
                    "Describe $p$-adic numbers $\\mathbb{Q}_p$. "
                    "How does the $p$-adic absolute value differ from the usual absolute value, "
                    "and what is Hensel's Lemma used for?"
                ),
                "expected": "Q_p is the completion of Q under the p-adic norm; Hensel's Lemma lifts solutions mod p to Z_p.",
                "expected_keywords": [
                    "p-adic", "completion", "absolute value", "hensel", "lift",
                    "ultrametric", "valuation", "congruence",
                ],
                "domain": "number_theory",
            },
            {
                "id": "fmath_016",
                "prompt": (
                    "Explain the Langlands Program in one paragraph. "
                    "What is the central conjecture and which two mathematical worlds "
                    "does it seek to unify?"
                ),
                "expected": "The Langlands Program conjectures a deep correspondence between Galois representations and automorphic forms.",
                "expected_keywords": [
                    "langlands", "galois", "automorphic", "representation",
                    "l-function", "correspondence", "functoriality",
                ],
                "domain": "number_theory",
            },
            {
                "id": "fmath_017",
                "prompt": (
                    "Prove that $\\sqrt{2}$ is irrational using a proof by contradiction. "
                    "Then generalise: for which integers $n$ is $\\sqrt{n}$ irrational?"
                ),
                "expected": "sqrt(n) is irrational iff n is not a perfect square; proof uses infinite descent or unique factorisation.",
                "expected_keywords": [
                    "irrational", "contradiction", "even", "odd", "perfect square",
                    "unique factorisation", "prime", "infinite descent",
                ],
                "domain": "number_theory",
            },
            # --- Cross-domain / Proof-sketch (3 problems) ---
            {
                "id": "fmath_018",
                "prompt": (
                    "Describe Gödel's First Incompleteness Theorem. "
                    "What does it assert about any sufficiently strong consistent formal "
                    "system, and what is the role of the Gödel sentence?"
                ),
                "expected": "Any consistent system strong enough to encode arithmetic has a true but unprovable statement.",
                "expected_keywords": [
                    "godel", "incomplete", "consistent", "unprovable", "formal system",
                    "arithmetic", "self-reference", "sentence",
                ],
                "domain": "logic",
            },
            {
                "id": "fmath_019",
                "prompt": (
                    "State the Cauchy-Schwarz inequality in an inner product space "
                    "$\\langle \\cdot, \\cdot \\rangle$. Prove it and describe one "
                    "important application in probability theory."
                ),
                "expected": "|<u,v>|^2 <= <u,u><v,v>; applied to prove the correlation coefficient is in [-1,1].",
                "expected_keywords": [
                    "cauchy-schwarz", "inner product", "inequality", "norm",
                    "correlation", "covariance", "variance", "proof",
                ],
                "domain": "real_analysis",
            },
            {
                "id": "fmath_020",
                "prompt": (
                    "Explain the concept of a sheaf on a topological space. "
                    "Define presheaf and the sheaf condition. "
                    "Give one example from algebraic geometry or complex analysis."
                ),
                "expected": "A sheaf assigns data to open sets satisfying gluing; e.g., holomorphic functions form a sheaf.",
                "expected_keywords": [
                    "sheaf", "presheaf", "gluing", "open set", "restriction",
                    "local", "section", "holomorphic",
                ],
                "domain": "algebraic_geometry",
            },
        ]

    # ------------------------------------------------------------------
    # evaluate_response
    # ------------------------------------------------------------------

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score based on fraction of expected keywords present in the response."""
        keywords: List[str] = prompt_data.get("expected_keywords", [])
        if not keywords:
            return {
                "success": False,
                "score": 0.0,
                "metadata": {"reason": "no expected_keywords defined"},
            }

        response_lower = response.lower()
        found = [kw for kw in keywords if kw.lower() in response_lower]
        fraction = len(found) / len(keywords)

        # Partial-credit thresholds
        success = fraction >= 0.6

        return {
            "success": success,
            "score": round(fraction, 4),
            "metadata": {
                "keywords_found": found,
                "keywords_missing": [kw for kw in keywords if kw.lower() not in response_lower],
                "keywords_total": len(keywords),
                "keywords_matched": len(found),
                "domain": prompt_data.get("domain", ""),
            },
        }

    def get_system_prompt(self) -> str:
        return (
            "You are a research-level mathematician with expertise across abstract "
            "algebra, topology, real analysis, and number theory. "
            "Provide rigorous, detailed responses to the following graduate-level "
            "mathematics problems. Use precise mathematical terminology and, where "
            "appropriate, sketch proof strategies."
        )
