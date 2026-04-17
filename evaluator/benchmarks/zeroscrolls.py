"""ZeroScrolls benchmark - long document summarization and QA tasks."""

from typing import Dict, Any, List, Optional
from .base import Benchmark, BenchmarkConfig


class ZeroScrollsBenchmark(Benchmark):
    """ZeroScrolls - summarization and QA over multi-paragraph documents."""

    def __init__(self):
        config = BenchmarkConfig(
            name="zeroscrolls",
            description="Long document summarization and QA: news, books, meetings, legal",
            category="long_context",
            version="1.0",
            timeout=120,
            max_tokens=512,
            temperature=0.3,
        )
        super().__init__(config)

    def _load_prompts(self) -> None:
        self.prompts = [
            # --- News article summarization (1-5) ---
            {
                "id": "zs_001",
                "prompt": (
                    "Summarize the following news article in 3-5 sentences, capturing the most important facts.\n\n"
                    "ARTICLE:\n"
                    "City officials in Maplewood announced Tuesday that the long-delayed renovation of "
                    "Riverside Park will finally begin in April, following the approval of a $4.2 million "
                    "budget allocation by the city council last week. The project, first proposed in 2019, "
                    "was repeatedly postponed due to funding shortfalls exacerbated by the pandemic. The "
                    "renovation will include new playground equipment, resurfaced walking paths, upgraded "
                    "sports courts, and a new outdoor amphitheater designed for community events. "
                    "Mayor Sandra Holloway called the project 'long overdue' and said it would serve "
                    "residents for decades. Local contractor Pinnacle Construction Group won the bid "
                    "after a competitive tender process. Work is expected to be completed by October, "
                    "with the park remaining partially open during construction. Community groups have "
                    "expressed enthusiasm, with the Maplewood Youth Sports League citing the new courts "
                    "as a major benefit. A ribbon-cutting ceremony is planned for November 15. Funding "
                    "came from a combination of municipal bonds and a state infrastructure grant secured "
                    "in December 2024."
                ),
                "required_facts": [
                    "riverside park",
                    "4.2 million",
                    "maplewood",
                    "april",
                    "pinnacle construction",
                    "november",
                ],
            },
            {
                "id": "zs_002",
                "prompt": (
                    "Summarize the following news article in 3-5 sentences, capturing the most important facts.\n\n"
                    "ARTICLE:\n"
                    "Global semiconductor manufacturer NexChip Holdings reported record quarterly revenue "
                    "of $18.7 billion on Thursday, beating analyst expectations by nearly 12 percent. "
                    "The results were driven by surging demand for AI accelerator chips, which now "
                    "account for 43 percent of the company's total sales, up from 27 percent a year ago. "
                    "CEO Hiroshi Tanaka attributed the growth to multi-year supply agreements signed with "
                    "three major cloud computing providers. However, the company issued a cautious outlook "
                    "for the following quarter, citing potential export restrictions and rising raw "
                    "material costs. NexChip announced plans to invest $6 billion in a new fabrication "
                    "plant in Arizona, expected to create approximately 3,200 permanent jobs. The plant "
                    "will produce chips at the 2-nanometer node, the most advanced process currently "
                    "available for commercial production. Shares rose 8.4 percent in after-hours trading. "
                    "Industry analysts noted that the results reinforced NexChip's position as the "
                    "second-largest chipmaker by revenue globally."
                ),
                "required_facts": [
                    "nexchip",
                    "18.7 billion",
                    "ai accelerator",
                    "arizona",
                    "6 billion",
                    "2-nanometer",
                    "hiroshi tanaka",
                ],
            },
            {
                "id": "zs_003",
                "prompt": (
                    "Summarize the following news article in 3-5 sentences.\n\n"
                    "ARTICLE:\n"
                    "Scientists at the Polar Research Institute released a study Wednesday showing that "
                    "Arctic sea ice reached its third-lowest recorded extent this past summer, covering "
                    "just 3.76 million square kilometers at its minimum. The study, published in the "
                    "journal Climate Dynamics, analyzed satellite data going back to 1979 and found that "
                    "the rate of sea ice loss has accelerated significantly since 2010. Lead researcher "
                    "Dr. Ingrid Solvang warned that the Arctic could experience its first ice-free summer "
                    "within 15 to 20 years if current trends continue. Loss of sea ice affects global "
                    "weather patterns, ocean circulation, and the survival of species such as polar bears "
                    "and ringed seals. The study calls for urgent reductions in greenhouse gas emissions "
                    "and increased investment in Arctic monitoring infrastructure. The findings were "
                    "consistent with projections from the Intergovernmental Panel on Climate Change. "
                    "Co-authors from institutions in Norway, Canada, and the United States contributed "
                    "to the research."
                ),
                "required_facts": [
                    "arctic sea ice",
                    "3.76 million",
                    "dr. ingrid solvang",
                    "climate dynamics",
                    "15 to 20 years",
                    "polar bears",
                ],
            },
            {
                "id": "zs_004",
                "prompt": (
                    "Summarize the following news article in 3-5 sentences.\n\n"
                    "ARTICLE:\n"
                    "The national railway operator, TransRail, announced a major expansion plan Monday "
                    "that will add 1,200 kilometers of new high-speed track connecting twelve regional "
                    "cities to the capital by 2032. The $47 billion project, partially funded by the "
                    "European Investment Bank, aims to reduce car and air travel by making rail journeys "
                    "faster and more affordable. Phase one, covering four cities in the northern corridor, "
                    "will begin construction in 2026. Officials estimate the project will cut carbon "
                    "emissions by 2.4 million tonnes annually once fully operational. Transport Minister "
                    "Aleksandra Kowalski said the plan would create 85,000 construction jobs over the "
                    "decade. Environmental groups broadly welcomed the announcement but raised concerns "
                    "about habitat disruption in two protected forest areas on the southern route. "
                    "TransRail plans to release detailed environmental impact assessments in the "
                    "coming months."
                ),
                "required_facts": [
                    "transrail",
                    "1,200 kilometers",
                    "47 billion",
                    "2032",
                    "aleksandra kowalski",
                    "85,000",
                    "2.4 million tonnes",
                ],
            },
            {
                "id": "zs_005",
                "prompt": (
                    "Summarize the following news article in 3-5 sentences.\n\n"
                    "ARTICLE:\n"
                    "A coalition of 14 countries signed the Geneva Digital Rights Accord on Friday, "
                    "pledging to establish common standards for data privacy, algorithmic transparency, "
                    "and limits on government surveillance of citizens' online activity. The accord, "
                    "negotiated over 18 months under the auspices of the United Nations Digital "
                    "Governance Forum, requires signatory states to enact implementing legislation "
                    "within two years. Notably absent from the signatories were the United States, "
                    "China, and Russia, whose representatives said they needed more time to review "
                    "the text. Civil society organizations praised the agreement as a historic step "
                    "but noted that its enforceability depends entirely on domestic implementation. "
                    "The accord includes a dispute resolution mechanism administered by a new "
                    "independent body, the Digital Rights Arbitration Council. Observers expect "
                    "several additional countries to sign in the coming months."
                ),
                "required_facts": [
                    "14 countries",
                    "geneva digital rights accord",
                    "data privacy",
                    "united states",
                    "digital rights arbitration council",
                    "two years",
                ],
            },
            # --- Book chapter QA (6-10) ---
            {
                "id": "zs_006",
                "prompt": (
                    "Read the following book chapter excerpt and answer: What is the central conflict "
                    "in this chapter, who are the two main characters involved, and how is it resolved?\n\n"
                    "CHAPTER EXCERPT:\n"
                    "Eleanor had spent three years cataloguing the manuscripts in the monastery library, "
                    "and she had never once violated the abbot's rule against removing documents from "
                    "the reading room. Yet here she was at midnight, slipping a brittle 12th-century "
                    "codex into her satchel. The evidence it contained—a detailed land grant bearing "
                    "the seal of a king long thought to have died without heirs—could overturn the "
                    "inheritance dispute that had dragged through the courts for a decade.\n\n"
                    "Father Bernard found her at the door. He was 80 years old and moved slowly, but "
                    "his eyes were sharp. For a long moment neither spoke. Eleanor had always respected "
                    "him; he had given her the research post when no university would hire a woman. "
                    "She explained what she had found and what it meant. Bernard listened in silence. "
                    "Then, to her astonishment, he told her he had known about the codex for forty "
                    "years. He had hidden it precisely because the land grant would destroy a family "
                    "that had been generous benefactors of the monastery. He could not protect it "
                    "forever, he said. He handed her the keys and told her to make a proper copy, "
                    "return the original, and submit the evidence through legal channels. She agreed. "
                    "By morning they had worked together through the night to produce an authenticated "
                    "transcription."
                ),
                "required_facts": [
                    "eleanor",
                    "father bernard",
                    "codex",
                    "land grant",
                    "inheritance",
                    "transcription",
                ],
            },
            {
                "id": "zs_007",
                "prompt": (
                    "Read the following passage and answer: What scientific discovery is described, "
                    "who made it, and what was the immediate consequence?\n\n"
                    "PASSAGE:\n"
                    "In the summer of 1928, Alexander Fleming returned to his laboratory at St. Mary's "
                    "Hospital in London after a two-week vacation to find that one of his petri dishes "
                    "had been contaminated with a mold. Rather than discarding the dish, he noticed "
                    "something unusual: a clear halo around the mold colony where the surrounding "
                    "Staphylococcus bacteria had been destroyed. The mold was identified as Penicillium "
                    "notatum. Fleming realized the mold was producing a substance with powerful "
                    "antibacterial properties. He named this substance penicillin. Though Fleming "
                    "published his findings in 1929, the compound proved difficult to isolate in "
                    "stable form, and widespread medical use had to await the work of Howard Florey "
                    "and Ernst Boris Chain at Oxford in the early 1940s. Their purification and "
                    "clinical testing of penicillin transformed the treatment of bacterial infections "
                    "and saved millions of lives during World War II."
                ),
                "required_facts": [
                    "alexander fleming",
                    "penicillin",
                    "penicillium notatum",
                    "staphylococcus",
                    "howard florey",
                    "world war ii",
                ],
            },
            {
                "id": "zs_008",
                "prompt": (
                    "Read the following chapter excerpt and answer: What is the narrator's main goal, "
                    "what obstacle do they face, and what decision do they make at the end?\n\n"
                    "CHAPTER:\n"
                    "Marcus had saved for seven years to open his restaurant. The location on Canal Street "
                    "was perfect: high foot traffic, a corner spot with two big windows, affordable rent "
                    "by neighborhood standards. He had signed the lease, hired a chef named Doris, and "
                    "ordered the kitchen equipment. Then the city inspector arrived and informed him that "
                    "the building's electrical system could not support a commercial kitchen without a "
                    "full rewiring that would cost $65,000. His savings were already committed. The bank "
                    "had declined his loan application twice. He spent a week unable to sleep, running "
                    "numbers, calling contractors. His sister Renata offered to invest her own savings "
                    "of $40,000 if he could find the remaining $25,000 elsewhere. A local community "
                    "development lender agreed to provide the gap financing at a modest interest rate. "
                    "Marcus accepted both offers, knowing he was taking on more risk than he had planned. "
                    "He signed the loan documents on a Thursday morning and called Doris to tell her the "
                    "kitchen would be ready by spring."
                ),
                "required_facts": [
                    "marcus",
                    "canal street",
                    "65,000",
                    "renata",
                    "40,000",
                    "doris",
                    "electrical",
                ],
            },
            {
                "id": "zs_009",
                "prompt": (
                    "Read the passage and provide a summary identifying: the main topic, three key "
                    "claims made, and any conclusion stated.\n\n"
                    "PASSAGE:\n"
                    "The relationship between sleep duration and cognitive performance has been the "
                    "subject of extensive research over the past two decades. Studies consistently "
                    "show that adults who sleep fewer than six hours per night exhibit measurable "
                    "deficits in attention, working memory, and reaction time compared to those "
                    "sleeping seven to nine hours. A landmark 2003 study by Van Dongen et al. "
                    "demonstrated that chronic sleep restriction—even at levels that subjects did "
                    "not perceive as debilitating—produced cumulative cognitive impairment equivalent "
                    "to two to three nights of total sleep deprivation. More recent neuroimaging "
                    "research has linked insufficient sleep to reduced activity in the prefrontal "
                    "cortex, the region responsible for executive function and decision-making. "
                    "Conversely, studies of napping have shown that even short sleep episodes of "
                    "20 to 30 minutes can temporarily restore alertness and improve performance on "
                    "complex tasks. The consensus among sleep researchers is that prioritizing "
                    "adequate sleep is one of the most cost-effective interventions for maintaining "
                    "cognitive health across the lifespan."
                ),
                "required_facts": [
                    "sleep",
                    "cognitive",
                    "van dongen",
                    "prefrontal cortex",
                    "six hours",
                    "napping",
                ],
            },
            {
                "id": "zs_010",
                "prompt": (
                    "Summarize the following historical passage, identifying the key event, its cause, "
                    "its main actors, and its outcome.\n\n"
                    "PASSAGE:\n"
                    "The Boston Tea Party of December 16, 1773, was a pivotal act of political protest "
                    "by American colonists against British taxation policy. The immediate trigger was "
                    "the Tea Act of 1773, which granted the British East India Company a monopoly on "
                    "tea sales in the American colonies, effectively cutting out local merchants and "
                    "maintaining a tax that colonists regarded as illegitimate given their lack of "
                    "representation in the British Parliament. A group of colonists calling themselves "
                    "the Sons of Liberty, led in part by Samuel Adams, organized a mass meeting at "
                    "the Old South Meeting House in Boston. When Governor Hutchinson refused to allow "
                    "the tea ships to return to England, approximately 116 men disguised as Mohawk "
                    "Indians boarded three ships in Boston Harbor and dumped 342 chests of tea into "
                    "the water. The British Parliament responded with the Coercive Acts of 1774, which "
                    "further inflamed colonial resistance and accelerated the path toward the "
                    "American Revolution."
                ),
                "required_facts": [
                    "boston tea party",
                    "december 16, 1773",
                    "tea act",
                    "samuel adams",
                    "342 chests",
                    "coercive acts",
                ],
            },
            # --- Meeting transcript summarization (11-15) ---
            {
                "id": "zs_011",
                "prompt": (
                    "Summarize the following meeting transcript, listing all decisions made and "
                    "action items assigned.\n\n"
                    "TRANSCRIPT:\n"
                    "MODERATOR (Jamie): Let's get started. First agenda item is the Q3 marketing budget.\n"
                    "PRIYA: Finance has approved $180,000 for Q3. We agreed last time to allocate 60% "
                    "to digital and 40% to events.\n"
                    "JAMES: I'd like to revisit that split. Our last event had poor ROI.\n"
                    "JAMIE: Let's keep the agreed split for now and review after the July campaign. "
                    "Priya, can you draft the budget breakdown by Friday?\n"
                    "PRIYA: Sure.\n"
                    "JAMIE: Next, the new product launch date. Engineering says October 14 is realistic.\n"
                    "CARLOS: Sales needs at least three weeks of advance notice for retailer briefings.\n"
                    "JAMIE: So we lock in October 14. Carlos, please prepare the retailer briefing deck "
                    "by September 20.\n"
                    "CARLOS: Understood.\n"
                    "JAMIE: Last item—customer support staffing. We received 40% more tickets last month.\n"
                    "SARA: I recommend hiring two additional agents before the product launch.\n"
                    "JAMIE: Agreed. Sara, submit the job requisitions to HR by end of week.\n"
                    "SARA: Will do.\n"
                    "JAMIE: Great. We'll reconvene in two weeks."
                ),
                "required_facts": [
                    "180,000",
                    "october 14",
                    "priya",
                    "carlos",
                    "sara",
                    "retailer briefing",
                    "two additional agents",
                ],
            },
            {
                "id": "zs_012",
                "prompt": (
                    "Read the following meeting transcript and answer: What problem is being discussed, "
                    "what solution was agreed upon, and who is responsible for the next step?\n\n"
                    "TRANSCRIPT:\n"
                    "FACILITATOR (Dana): The issue today is the deployment pipeline. We've had three "
                    "failed releases in the past month.\n"
                    "VIKRAM: Each failure was caused by untested database migrations running in production.\n"
                    "JULIA: We need a staging environment that mirrors production more closely. "
                    "Right now staging has different data volumes and we're not catching issues.\n"
                    "DANA: What would it take to fix that?\n"
                    "VIKRAM: We could spin up a new staging cluster with anonymized production data. "
                    "Cost would be roughly $2,000 a month.\n"
                    "DANA: That's within our ops budget. Can you scope it out, Vikram?\n"
                    "VIKRAM: I'll have a technical spec ready by next Wednesday.\n"
                    "JULIA: We should also add a required migration test step to the CI pipeline. "
                    "I can implement that this sprint.\n"
                    "DANA: Perfect. Vikram on the staging spec, Julia on CI. Let's reconvene Thursday."
                ),
                "required_facts": [
                    "deployment pipeline",
                    "staging",
                    "vikram",
                    "julia",
                    "2,000",
                    "database migrations",
                    "wednesday",
                ],
            },
            {
                "id": "zs_013",
                "prompt": (
                    "Summarize the key points from the following board meeting transcript.\n\n"
                    "TRANSCRIPT:\n"
                    "CHAIR (Margaret): I call this meeting to order. First item: annual financial results.\n"
                    "CFO (Robert): Revenue came in at $142 million, up 11% from last year. Net profit "
                    "margin improved to 14.3%. We reduced long-term debt by $8 million.\n"
                    "MARGARET: Excellent. Any concerns?\n"
                    "BOARD MEMBER (Theresa): Accounts receivable aging has worsened. Average days "
                    "outstanding is now 52 days versus our 40-day target.\n"
                    "ROBERT: We're working with sales to tighten credit terms. We expect improvement "
                    "by Q3.\n"
                    "MARGARET: Second item: proposed acquisition of Hartwell Systems for $28 million.\n"
                    "BOARD MEMBER (David): Due diligence is complete. Hartwell adds a complementary "
                    "SaaS product and approximately 200 enterprise customers.\n"
                    "MARGARET: Motion to approve the acquisition?\n"
                    "ALL: Approved.\n"
                    "MARGARET: Third item: dividend. Robert proposes $0.35 per share.\n"
                    "ALL: Approved.\n"
                    "MARGARET: Meeting adjourned."
                ),
                "required_facts": [
                    "142 million",
                    "11%",
                    "14.3%",
                    "hartwell",
                    "28 million",
                    "0.35",
                    "52 days",
                ],
            },
            {
                "id": "zs_014",
                "prompt": (
                    "Read the following project kickoff meeting transcript and summarize: the project "
                    "goal, timeline, team roles, and identified risks.\n\n"
                    "TRANSCRIPT:\n"
                    "PM (LISA): Welcome everyone. Project Helix goal: migrate our customer database from "
                    "on-premise Oracle to Google Cloud Spanner by end of Q4.\n"
                    "DEVLEAD (AARON): I'll lead the technical migration. My team will handle schema "
                    "conversion and ETL pipeline development.\n"
                    "DBA (FATIMA): I'll manage data validation and rollback procedures.\n"
                    "INFRA (BEN): I'm responsible for provisioning the Spanner instances and configuring "
                    "network security.\n"
                    "LISA: Key milestones: schema design complete by July 31, pilot migration of 10% of "
                    "data by August 31, full cutover by November 30.\n"
                    "AARON: Main risk is data integrity during migration—any corruption would be "
                    "catastrophic. We need extensive checksumming.\n"
                    "FATIMA: Also concerned about downtime. We should target a maintenance window "
                    "of no more than four hours.\n"
                    "BEN: Network latency between on-prem and cloud may slow the ETL. I recommend "
                    "using a Dedicated Interconnect.\n"
                    "LISA: All noted. Let's plan weekly syncs every Monday."
                ),
                "required_facts": [
                    "project helix",
                    "google cloud spanner",
                    "oracle",
                    "november 30",
                    "august 31",
                    "fatima",
                    "four hours",
                ],
            },
            {
                "id": "zs_015",
                "prompt": (
                    "Summarize the following customer feedback review meeting, identifying the top "
                    "issues raised and the proposed solutions.\n\n"
                    "TRANSCRIPT:\n"
                    "LEAD (NINA): Today we're reviewing Q2 support tickets. We had 4,300 tickets, "
                    "up 25% from Q1.\n"
                    "ANALYST (TOM): The top issue was login failures—1,100 tickets, mostly caused "
                    "by the new SSO rollout. We've since patched the SSO provider and tickets dropped.\n"
                    "NINA: Good. Second issue?\n"
                    "TOM: Slow report generation—800 tickets. The database query for the summary "
                    "report isn't indexed properly. Engineering is scheduled to fix it in the next sprint.\n"
                    "NINA: Third?\n"
                    "TOM: Missing email notifications—600 tickets. A misconfigured Sendgrid webhook "
                    "was the root cause. It's been corrected.\n"
                    "NINA: Anything systemic?\n"
                    "TOM: Our first-response time averaged 18 hours, above our 12-hour SLA. "
                    "We need to either hire more agents or implement a chatbot triage.\n"
                    "NINA: Let's evaluate chatbot options this quarter. Tom, prepare a vendor "
                    "comparison by July 15."
                ),
                "required_facts": [
                    "4,300 tickets",
                    "login failures",
                    "1,100",
                    "sso",
                    "sendgrid",
                    "18 hours",
                    "chatbot",
                    "july 15",
                ],
            },
            # --- Legal document key-point extraction (16-20) ---
            {
                "id": "zs_016",
                "prompt": (
                    "Extract the key points from the following contract clause, including: parties "
                    "involved, main obligation, duration, and consequences of breach.\n\n"
                    "CONTRACT CLAUSE:\n"
                    "NON-DISCLOSURE AGREEMENT — CLAUSE 4: CONFIDENTIALITY OBLIGATIONS\n\n"
                    "4.1 Each party (the 'Receiving Party') agrees to hold all Confidential Information "
                    "disclosed by the other party (the 'Disclosing Party') in strict confidence and not "
                    "to disclose such information to any third party without the prior written consent "
                    "of the Disclosing Party. This obligation shall remain in effect for a period of "
                    "five (5) years from the date of disclosure of each item of Confidential Information.\n\n"
                    "4.2 In the event of an unauthorized disclosure, the Receiving Party shall promptly "
                    "notify the Disclosing Party in writing and shall take all reasonable steps to "
                    "mitigate any harm. The Disclosing Party shall be entitled to seek injunctive relief "
                    "and/or monetary damages, including reasonable attorneys' fees, in any court of "
                    "competent jurisdiction."
                ),
                "required_facts": [
                    "five",
                    "confidential",
                    "injunctive relief",
                    "monetary damages",
                    "five (5) years",
                    "unauthorized disclosure",
                ],
            },
            {
                "id": "zs_017",
                "prompt": (
                    "Summarize the following legal clause, highlighting: the payment terms, late "
                    "payment consequences, and dispute resolution procedure.\n\n"
                    "CONTRACT CLAUSE:\n"
                    "SECTION 7: PAYMENT TERMS\n\n"
                    "7.1 Client shall pay all invoices within thirty (30) calendar days of the invoice "
                    "date ('Due Date'). All payments shall be made in US Dollars by wire transfer to "
                    "the account specified in Schedule B.\n\n"
                    "7.2 Any amount not paid by the Due Date shall accrue interest at the rate of 1.5% "
                    "per month (18% per annum) from the Due Date until the date of actual payment.\n\n"
                    "7.3 In the event of a payment dispute, Client shall provide written notice to "
                    "Vendor within ten (10) business days of receipt of the disputed invoice, specifying "
                    "the nature of the dispute in reasonable detail. The parties shall attempt to resolve "
                    "the dispute through good-faith negotiation within thirty (30) days of such notice. "
                    "If unresolved, the dispute shall be submitted to binding arbitration under the rules "
                    "of the American Arbitration Association in New York, New York."
                ),
                "required_facts": [
                    "30",
                    "thirty",
                    "1.5%",
                    "18%",
                    "arbitration",
                    "american arbitration association",
                    "new york",
                    "10 business days",
                ],
            },
            {
                "id": "zs_018",
                "prompt": (
                    "Extract the key points from the following employment contract clause regarding "
                    "termination, including grounds, notice period, and severance.\n\n"
                    "CONTRACT CLAUSE:\n"
                    "SECTION 12: TERMINATION\n\n"
                    "12.1 Either party may terminate this Agreement without cause upon sixty (60) days' "
                    "written notice to the other party.\n\n"
                    "12.2 The Company may terminate this Agreement immediately for cause, which includes "
                    "but is not limited to: (a) material breach of this Agreement; (b) conviction of a "
                    "felony; (c) willful misconduct or gross negligence in the performance of duties; "
                    "or (d) persistent failure to perform assigned duties after written warning.\n\n"
                    "12.3 In the event of termination without cause, the Employee shall receive a "
                    "severance payment equal to three (3) months' base salary, subject to the Employee "
                    "executing a release of claims in favor of the Company within 21 days of separation. "
                    "No severance shall be payable in the event of termination for cause."
                ),
                "required_facts": [
                    "sixty",
                    "60 days",
                    "three",
                    "3 months",
                    "severance",
                    "release of claims",
                    "21 days",
                ],
            },
            {
                "id": "zs_019",
                "prompt": (
                    "Summarize the following regulatory compliance notice, identifying the regulation "
                    "cited, the required action, the deadline, and the penalty for non-compliance.\n\n"
                    "NOTICE:\n"
                    "COMPLIANCE NOTICE — DATA PROTECTION\n\n"
                    "This notice is issued pursuant to Article 32 of the General Data Protection "
                    "Regulation (GDPR). Our records indicate that your organization processes personal "
                    "data of EU residents but has not registered a Data Protection Officer (DPO) as "
                    "required under Article 37 of the GDPR.\n\n"
                    "You are required to appoint a qualified DPO and submit the DPO's contact details "
                    "to this authority within 30 days of receipt of this notice. Failure to comply may "
                    "result in an administrative fine of up to €10 million or 2% of your total annual "
                    "worldwide turnover, whichever is higher, in accordance with Article 83(4) of the GDPR.\n\n"
                    "If you believe this notice has been issued in error, you may submit a written "
                    "response with supporting documentation within 15 days."
                ),
                "required_facts": [
                    "gdpr",
                    "data protection officer",
                    "dpo",
                    "30 days",
                    "10 million",
                    "2%",
                    "article 37",
                ],
            },
            {
                "id": "zs_020",
                "prompt": (
                    "Read the following software license clause and extract key points: what is "
                    "permitted, what is prohibited, and what are the warranty limitations.\n\n"
                    "LICENSE CLAUSE:\n"
                    "GRANT OF LICENSE AND RESTRICTIONS\n\n"
                    "Subject to the terms of this Agreement, Licensor grants to Licensee a non-exclusive, "
                    "non-transferable, worldwide license to use, reproduce, and distribute the Software "
                    "solely for Licensee's internal business purposes. Licensee may make up to three (3) "
                    "backup copies of the Software for archival purposes.\n\n"
                    "Licensee shall not: (a) sublicense, sell, rent, lease, or otherwise transfer the "
                    "Software to any third party; (b) reverse engineer, decompile, or disassemble the "
                    "Software; (c) remove or alter any proprietary notices or labels on the Software; "
                    "or (d) use the Software to develop competing products.\n\n"
                    "THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT WARRANTY OF ANY KIND. LICENSOR EXPRESSLY "
                    "DISCLAIMS ALL WARRANTIES, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, "
                    "INCLUDING WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. "
                    "IN NO EVENT SHALL LICENSOR'S TOTAL LIABILITY EXCEED THE AMOUNTS PAID BY LICENSEE "
                    "IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM."
                ),
                "required_facts": [
                    "non-exclusive",
                    "three",
                    "backup",
                    "reverse engineer",
                    "as is",
                    "12 months",
                    "sublicense",
                ],
            },
        ]

    def evaluate_response(self, prompt_data: Dict[str, Any], response: str) -> Dict[str, Any]:
        """Score = fraction of required_facts present in response (case-insensitive)."""
        required_facts: List[str] = prompt_data.get("required_facts", [])
        response_lower = response.lower()

        def fact_present(fact: str) -> bool:
            return fact.lower() in response_lower

        if not required_facts:
            return {"success": False, "score": 0.0, "metadata": {"required_facts": []}}

        matched = [f for f in required_facts if fact_present(f)]
        score = len(matched) / len(required_facts)
        success = score >= 0.5

        return {
            "success": success,
            "score": round(score, 4),
            "metadata": {
                "required_facts": required_facts,
                "matched_facts": matched,
                "missing_facts": [f for f in required_facts if not fact_present(f)],
                "fact_coverage": f"{len(matched)}/{len(required_facts)}",
            },
        }

    def get_system_prompt(self) -> Optional[str]:
        return (
            "You are a skilled summarizer and analyst. Read documents carefully and produce "
            "accurate, well-structured responses that include all key facts, names, figures, "
            "and conclusions from the source material."
        )
