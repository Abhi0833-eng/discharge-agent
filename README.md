# Discharge Summary Agent
### Agentic AI System for Clinical Discharge Summaries
**Built for: Dscribe (Unriddle Technologies) — AI Engineer Take-Home Assignment**

---

## Quick Start

### Prerequisites
- Python 3.10+
- Groq API key (free at console.groq.com)

### Installation
```bash
pip install groq pymupdf python-dotenv
```

### Setup
1. Add your Groq API key to `.env`:
GROQ_API_KEY=your_key_here

2. Place patient PDF(s) in `patient_data/` folder

3. Run the agent:
```bash
python agent.py
```

### Output
- Discharge summary → `output/discharge_summary_*.txt`
- Agent step trace → `traces/trace_*.json`
- Extracted data → `output/extracted_data_*.json`

---

## System Architecture

### Agent Loop Design
The agent follows a **plan-then-execute** loop with a hard step cap of 15 iterations:
READ PDF
↓
STEP 1: PLAN

LLM reads patient notes
Identifies immediate concerns
Lists missing critical info
↓
STEP 2: DETECT CONFLICTS
Scans all documents for contradictions
Auto-escalates HIGH severity conflicts
Calls escalation tool for each conflict found
↓
STEP 3: EXTRACT SECTIONS (7 sections)
Demographics
Diagnoses
Hospital Course
Medications
Investigations
Allergies
Follow-up
↓
STEP 4: MEDICATION SAFETY
Drug interaction checker tool
Medication reconciliation tool
Flags MAJOR/MODERATE interactions
↓
STEP 5: CHECK PENDING RESULTS
Identifies investigations without results
Flags pending items for clinician
↓
STEP 6: ASSEMBLE SUMMARY
Combines all extracted data
Produces structured draft
Saves outputs


This is a **real agent loop** — not a hardcoded pipeline. The LLM plans, decides which tools to call, re-evaluates after each step, and the loop enforces a hard cap to prevent runaway execution.

---

## No-Fabrication Guardrail

This is the most important safety property of the system.

**How it is enforced:**

1. **System prompt** explicitly forbids inventing facts — stated as NEVER BREAK rules
2. **Extraction prompts** instruct the LLM to use `[MISSING]` for anything not in the documents
3. **Conflict detection** — agent never resolves conflicts, only surfaces them
4. **Pending results** — agent never fills in a plausible value, always marks as `[PENDING]`
5. **Draft notice** — every output is explicitly marked as a DRAFT requiring clinician sign-off
6. **Low temperature (0.1)** — reduces hallucination by keeping LLM deterministic

**Evidence in output:**
- Patient name/age/IP not documented → shown as `[MISSING]`
- Discharge medications not formally documented → flagged, not invented
- 5 conflicting diagnoses across documents → all listed, none chosen
- Urine C/S negative vs CT showing pyelonephritis → conflict flagged

---

## Failure & Conflict Handling

### PDF Ingestion Failures
- PyMuPDF attempts direct text extraction first
- If PDF is image-based → graceful fallback to pre-extracted text
- Pre-extracted text generated from careful manual reading of all 71 pages
- In production: would be replaced by a proper OCR pipeline (e.g. AWS Textract)

### LLM Call Failures
- Every LLM call wrapped in retry logic (3 attempts)
- Exponential backoff between retries
- On total failure: returns error string, never crashes
- Agent continues with remaining steps

### Conflict Handling (Patient 2 example)
Five conflicting diagnoses found across documents:
1. ER Chart: DKA
2. Admission Record (provisional): TAFE + Uncontrolled T2DM  
3. Admission Record (final): ? Synovitis + Cholelithiasis
4. Consultation sheets: AFI + DKA + Uncontrolled T2DM + B/L Pyelonephritis
5. Latest consultation: AFI + DKA + Uncontrolled T2DM + B/L Polynephritis

**Agent action:** All conflicts flagged with ⚠️ CONFLICT markers. 
Escalation tool called for each HIGH severity conflict.
Clinician must resolve — agent never picks one.

### Missing Data
- Urine C/S result negative vs pyelonephritis diagnosis → flagged
- No formal discharge prescription found → flagged as MISSING
- IV cannula not removed at discharge → flagged
- Discharge BP 170/80 + HR 110 (not normalized) → flagged as safety concern

---

## Tools

| Tool | Purpose | When Called |
|------|---------|-------------|
| `check_drug_interactions` | Checks medication pairs for interactions | Always — after medications extracted |
| `flag_for_clinician_review` | Escalates safety concerns | When conflict/safety issue detected |
| `reconcile_medications` | Compares admission vs discharge meds | Always — surfaces changes |
| `check_pending_results` | Identifies pending investigations | Always — before final assembly |

All tools are mocked but designed to be swapped with real APIs.

---

## Files
discharge_agent/
├── agent.py              # Main agent loop
├── tools.py              # Mock clinical tools
├── pdf_reader.py         # PDF ingestion + fallback
├── prompts.py            # All LLM prompts
├── extracted_data.py     # Pre-extracted patient text
├── requirements.txt      # Dependencies
├── .env                  # API key (not committed)
├── README.md             # This file
├── patient_data/         # Input PDFs
├── output/               # Discharge summaries + extracted data
└── traces/               # Agent step traces

---

## Patient 2 — Key Clinical Findings

**Admission:** 26/02/2026 | **Discharge:** 03/03/2026 | **Duration:** 6 days

**Critical flags raised by agent:**
- ⚠️ 5 conflicting diagnoses across documents
- ⚠️ Urine C/S negative vs clinical pyelonephritis diagnosis
- ⚠️ No formal discharge prescription documented
- ⚠️ Blood culture result PENDING at discharge
- ⚠️ Contrast CT KUB recommended but not performed
- ⚠️ IV cannula not removed at discharge
- ⚠️ Discharge vitals not normalized (BP 170/80, HR 110)
- ⚠️ Drug interaction: Tramadol + Ondansetron (QT prolongation risk)
- ⚠️ Ayurvedic DM medication — status at discharge undocumented
- ⚠️ Patient discharged on request against medical advice

---

## Limitations

### Current Limitations
1. **OCR:** Image-based PDFs require pre-extracted text. 
   Production system needs Textract/Google Vision integration.
2. **Single patient:** Tested on one patient. 
   Multi-patient batching needs queue management.
3. **Mock tools:** Drug interaction DB is simplified. 
   Production needs integration with real pharmacovigilance APIs.
4. **Context window:** Very long PDFs may exceed LLM context. 
   Production needs chunking strategy.
5. **No memory:** Each run is stateless. 
   Production needs patient history integration.

### What I Would Do With More Time
1. Integrate AWS Textract for proper OCR of scanned documents
2. Connect to real drug interaction API (OpenFDA, DrugBank)
3. Add multi-patient batch processing with progress tracking
4. Build a web UI for clinician review and sign-off
5. Add unit tests for each agent step
6. Implement proper logging with structured log levels
7. Add confidence scores to each extracted field
8. Build Part 2 learning loop with real DPO fine-tuning

---

## Part 2 — Learning from Doctor Edits (Stretch)

*Status: Design documented, implementation pending due to time constraints.*

### Design

**Reward Signal:**
Normalized edit distance between agent draft and clinician-corrected version.
Lower edit distance = higher reward = better draft quality.
reward = 1 - (edit_distance(draft, corrected) / max(len(draft), len(corrected)))

**Simulated Reviewer:**
A "doctor" LLM (separate prompt) that applies a consistent editing policy:
- Fills in [MISSING] fields with plausible values
- Resolves diagnosis conflicts using clinical reasoning
- Rewrites vague sentences to be more specific
- Adds missing follow-up details

This produces (draft, corrected) pairs for training.

**Learning Mechanism:**
Contextual bandit over prompt templates:
- Maintain K prompt variants (different levels of detail, structure)
- Track average reward per variant
- Sample variants with epsilon-greedy exploration
- Update weights based on edit distance reward

**Improvement Curve:**
Expected: edit distance decreases over 20-50 iterations as
bandit learns which prompt templates produce drafts closest
to clinician preferences.

**Limitations of Learning Loop:**
- Cold start: needs minimum 10-20 (draft, corrected) pairs before signal is meaningful
- Gaming risk: agent can lower edit distance by being vaguer (shorter = fewer edits)
  Mitigation: penalize missing fields in reward, not just raw edit distance
- Style vs substance: model may learn clinician writing style without improving
  clinical accuracy. Mitigation: section-level scoring weights clinical fields higher
- Safety guarantee: learning never modifies the no-fabrication system prompt.
  Only the output formatting and detail level are tunable — core guardrails are frozen.

---

*Assignment submitted by: [Abhishek Gupta]*  
*Model used: llama-3.3-70b-versatile (Groq)*  
*Date: June 2026*
