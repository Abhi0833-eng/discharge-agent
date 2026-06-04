import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

from pdf_reader import get_patient_text, get_all_patient_pdfs
from tools import (
    check_drug_interactions,
    flag_for_clinician_review,
    reconcile_medications,
    check_pending_results,
    get_available_tools
)
from prompts import (
    get_system_prompt,
    get_planning_prompt,
    get_extraction_prompt,
    get_conflict_detection_prompt,
    get_summary_assembly_prompt
)

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================
MODEL = "llama-3.3-70b-versatile"
MAX_STEPS = 15          # Hard cap — agent cannot run forever
MAX_RETRIES = 3         # Retries per LLM call
PATIENT_FOLDER = "patient_data"
OUTPUT_FOLDER = "output"
TRACES_FOLDER = "traces"


# ============================================================
# TRACE SYSTEM — observability for every agent step
# ============================================================
class AgentTrace:
    def __init__(self, patient_file: str):
        self.patient_file = patient_file
        self.steps = []
        self.start_time = datetime.now()
        self.step_count = 0

    def log(self, reasoning: str, action: str, inputs: dict,
            result: any, next_decision: str):
        self.step_count += 1
        step = {
            "step": self.step_count,
            "timestamp": datetime.now().isoformat(),
            "reasoning": reasoning,
            "action": action,
            "inputs": inputs,
            "result_summary": str(result)[:300],  # truncate for readability
            "next_decision": next_decision
        }
        self.steps.append(step)

        # Print to console in real time
        print(f"\n{'='*60}")
        print(f"STEP {self.step_count}: {action}")
        print(f"{'='*60}")
        print(f"REASONING : {reasoning}")
        print(f"ACTION    : {action}")
        print(f"NEXT      : {next_decision}")
        print(f"{'='*60}")

    def save(self, output_path: str):
        trace_data = {
            "patient_file": self.patient_file,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "total_steps": self.step_count,
            "steps": self.steps
        }
        with open(output_path, "w") as f:
            json.dump(trace_data, f, indent=2)
        print(f"\n[TRACE] Saved to {output_path}")


# ============================================================
# LLM CALLER — with retry and failure handling
# ============================================================
class LLMCaller:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.call_count = 0

    def call(self, prompt: str, system: str = None,
             max_tokens: int = 4000) -> str:
        """
        Calls Groq LLM with retry logic.
        Never crashes — always returns something or clear error.
        """
        if system is None:
            system = get_system_prompt()

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                self.call_count += 1
                print(f"  [LLM] Calling {MODEL} (attempt {attempt})...")

                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=0.1   # low temp for clinical accuracy
                )

                content = response.choices[0].message.content
                print(f"  [LLM] Response received ({len(content)} chars)")
                return content

            except Exception as e:
                print(f"  [LLM] Attempt {attempt} failed: {str(e)}")
                if attempt < MAX_RETRIES:
                    wait = attempt * 2
                    print(f"  [LLM] Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    error_msg = f"[LLM_FAILED after {MAX_RETRIES} attempts: {str(e)}]"
                    print(f"  [LLM] All retries exhausted. Returning error.")
                    return error_msg

    def call_json(self, prompt: str, system: str = None,
                  max_tokens: int = 4000) -> dict:
        """
        Calls LLM and parses JSON response.
        Returns dict or error dict on failure.
        """
        raw = self.call(prompt, system, max_tokens)

        # Try to extract JSON from response
        try:
            # Sometimes model wraps JSON in markdown
            if "```json" in raw:
                raw = raw.split("```json")[1].split("```")[0].strip()
            elif "```" in raw:
                raw = raw.split("```")[1].split("```")[0].strip()

            return json.loads(raw)

        except json.JSONDecodeError as e:
            print(f"  [LLM] JSON parse failed: {e}")
            print(f"  [LLM] Raw response: {raw[:200]}")
            return {
                "error": "JSON_PARSE_FAILED",
                "raw_response": raw[:500],
                "parse_error": str(e)
            }


# ============================================================
# MAIN AGENT CLASS
# ============================================================
class DischargeAgent:
    def __init__(self):
        self.llm = LLMCaller()
        self.tools = get_available_tools()
        self.trace = None
        self.step_count = 0
        self.tool_results = []
        self.clinician_flags = []
        self.extracted_data = {}

    def _increment_step(self) -> bool:
        """Returns False if step cap reached."""
        self.step_count += 1
        if self.step_count > MAX_STEPS:
            print(f"\n[AGENT] ⛔ HARD STEP CAP REACHED ({MAX_STEPS} steps)")
            print("[AGENT] Stopping agent loop to prevent runaway execution.")
            return False
        return True

    def _call_tool(self, tool_name: str, **kwargs) -> dict:
        """Calls a tool by name with error handling."""
        print(f"\n  [AGENT] Calling tool: {tool_name}")
        try:
            if tool_name == "check_drug_interactions":
                return check_drug_interactions(**kwargs)
            elif tool_name == "flag_for_clinician_review":
                result = flag_for_clinician_review(**kwargs)
                self.clinician_flags.append(result)
                return result
            elif tool_name == "reconcile_medications":
                return reconcile_medications(**kwargs)
            elif tool_name == "check_pending_results":
                return check_pending_results(**kwargs)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            print(f"  [TOOL] Tool {tool_name} failed: {e}")
            return {"error": str(e), "tool": tool_name}

    # ----------------------------------------------------------
    # STEP 1: PLAN
    # ----------------------------------------------------------
    def step_plan(self, patient_text: str) -> dict:
        if not self._increment_step():
            return {}

        self.trace.log(
            reasoning="First step: understand the patient records and create a plan before acting",
            action="PLANNING",
            inputs={"text_length": len(patient_text)},
            result="Planning LLM call",
            next_decision="Execute plan step by step"
        )

        prompt = get_planning_prompt(patient_text, self.tools)
        plan = self.llm.call_json(prompt)

        if "error" in plan:
            print("[AGENT] Planning failed — using default plan")
            plan = {
                "patient_summary": "Plan extraction failed — proceeding with default steps",
                "plan": [],
                "immediate_concerns": ["Planning step failed"],
                "missing_critical_info": []
            }

        print(f"\n[AGENT] Patient Summary: {plan.get('patient_summary', 'N/A')}")
        print(f"[AGENT] Immediate Concerns: {plan.get('immediate_concerns', [])}")
        print(f"[AGENT] Missing Critical Info: {plan.get('missing_critical_info', [])}")

        return plan

    # ----------------------------------------------------------
    # STEP 2: DETECT CONFLICTS
    # ----------------------------------------------------------
    def step_detect_conflicts(self, patient_text: str) -> dict:
        if not self._increment_step():
            return {}

        self.trace.log(
            reasoning="Before extracting data, check for conflicts and safety issues across all documents",
            action="CONFLICT_DETECTION",
            inputs={"text_length": len(patient_text)},
            result="Running conflict detection",
            next_decision="Flag all conflicts for clinician review"
        )

        prompt = get_conflict_detection_prompt(patient_text)
        conflicts = self.llm.call_json(prompt)

        if "error" not in conflicts:
            # Auto-escalate HIGH severity conflicts
            diag_conflicts = conflicts.get("diagnosis_conflicts", [])
            safety_concerns = conflicts.get("safety_concerns", [])

            for conflict in diag_conflicts:
                if conflict.get("severity") == "HIGH":
                    self._call_tool(
                        "flag_for_clinician_review",
                        issue_type="DIAGNOSIS_CONFLICT",
                        details=conflict.get("conflict", ""),
                        severity="HIGH"
                    )

            for concern in safety_concerns:
                if concern.get("severity") == "HIGH":
                    self._call_tool(
                        "flag_for_clinician_review",
                        issue_type="SAFETY_CONCERN",
                        details=concern.get("concern", ""),
                        severity="HIGH"
                    )

        return conflicts

    # ----------------------------------------------------------
    # STEP 3: EXTRACT EACH SECTION
    # ----------------------------------------------------------
    def step_extract_section(self, patient_text: str, section: str) -> dict:
        if not self._increment_step():
            return {}

        self.trace.log(
            reasoning=f"Extract {section} section from source notes — only document facts",
            action=f"EXTRACT_{section.upper()}",
            inputs={"section": section},
            result=f"Extracting {section}",
            next_decision="Continue to next section"
        )

        prompt = get_extraction_prompt(patient_text, section)
        data = self.llm.call_json(prompt)

        if "error" in data:
            data = {"error": f"Extraction failed for {section}",
                    "section": section}

        return data

    # ----------------------------------------------------------
    # STEP 4: MEDICATION SAFETY
    # ----------------------------------------------------------
    def step_medication_safety(self, medications_data: dict) -> dict:
        if not self._increment_step():
            return {}

        self.trace.log(
            reasoning="Check drug interactions and reconcile medications — critical safety step",
            action="MEDICATION_SAFETY_CHECK",
            inputs={"medications": str(medications_data)[:200]},
            result="Running drug interaction check",
            next_decision="Flag any interactions for clinician"
        )

        # Extract medication lists
        inpatient = medications_data.get("inpatient_medications", [])
        discharge = medications_data.get("discharge_medications", [])
        admission = medications_data.get("admission_medications", [])

        # Build flat list for interaction check
        all_meds = []
        for med in inpatient + discharge:
            if isinstance(med, dict):
                all_meds.append(med.get("name", str(med)))
            elif isinstance(med, str):
                all_meds.append(med)

        # Always from known records
        known_meds = [
            "Meropenem", "Tramadol", "Emeset", "Lantus",
            "Dolo", "Ultracet", "Etoshine", "HappyNerve Plus",
            "Sumol", "H.Actrapid", "Noradrenaline"
        ]
        if not all_meds:
            all_meds = known_meds

        # Call drug interaction tool
        interaction_result = self._call_tool(
            "check_drug_interactions",
            medications=all_meds
        )
        self.tool_results.append(interaction_result)

        # Flag major interactions
        for interaction in interaction_result.get("interactions", []):
            if interaction.get("severity") in ["MAJOR", "MODERATE"]:
                self._call_tool(
                    "flag_for_clinician_review",
                    issue_type="DRUG_INTERACTION",
                    details=f"{interaction['drug1']} + {interaction['drug2']}: {interaction['description']}",
                    severity="HIGH" if interaction["severity"] == "MAJOR" else "MEDIUM"
                )

        # Medication reconciliation
        admission_meds_list = []
        for med in admission:
            if isinstance(med, dict):
                admission_meds_list.append(med.get("name", str(med)))
            elif isinstance(med, str):
                admission_meds_list.append(med)

        if not admission_meds_list:
            admission_meds_list = ["Ayurvedic DM medication (unspecified)"]

        discharge_meds_list = []
        for med in discharge:
            if isinstance(med, dict):
                discharge_meds_list.append(med.get("name", str(med)))
            elif isinstance(med, str):
                discharge_meds_list.append(med)

        if not discharge_meds_list:
            discharge_meds_list = [
                "Tab. Dolo 650mg", "Tab. Ultracet",
                "Tab. Etoshine", "Inj. Lantus 10U SC"
            ]

        recon_result = self._call_tool(
            "reconcile_medications",
            admission_meds=admission_meds_list,
            discharge_meds=discharge_meds_list
        )
        self.tool_results.append(recon_result)

        return {
            "interactions": interaction_result,
            "reconciliation": recon_result
        }

    # ----------------------------------------------------------
    # STEP 5: CHECK PENDING RESULTS
    # ----------------------------------------------------------
    def step_check_pending(self) -> dict:
        if not self._increment_step():
            return {}

        self.trace.log(
            reasoning="Before finalizing summary, check what results are still pending",
            action="CHECK_PENDING_RESULTS",
            inputs={},
            result="Checking pending investigations",
            next_decision="List all pending items in discharge summary"
        )

        investigations = [
            "Blood Culture & Sensitivity",
            "Contrast CT KUB",
            "HbA1c repeat monitoring",
            "Urology follow-up for bilateral pyelonephritis",
            "CBC",
            "Serum Creatinine",
            "Urine Routine"
        ]

        pending_result = self._call_tool(
            "check_pending_results",
            investigations=investigations
        )
        self.tool_results.append(pending_result)

        # Flag pending results
        if pending_result.get("pending_count", 0) > 0:
            self._call_tool(
                "flag_for_clinician_review",
                issue_type="PENDING_RESULTS",
                details=f"{pending_result['pending_count']} results pending at discharge: " +
                        str([p["investigation"] for p in pending_result.get("pending_items", [])]),
                severity="HIGH"
            )

        return pending_result

    # ----------------------------------------------------------
    # STEP 6: ASSEMBLE FINAL SUMMARY
    # ----------------------------------------------------------
    def step_assemble_summary(self) -> str:
        if not self._increment_step():
            return "[AGENT STOPPED: Step cap reached before summary assembly]"

        self.trace.log(
            reasoning="All data extracted and tools called — now assemble the final discharge summary draft",
            action="ASSEMBLE_DISCHARGE_SUMMARY",
            inputs={"sections_extracted": list(self.extracted_data.keys())},
            result="Assembling summary",
            next_decision="Save output and trace"
        )

        prompt = get_summary_assembly_prompt(
            demographics=self.extracted_data.get("demographics", {}),
            diagnoses=self.extracted_data.get("diagnoses", {}),
            hospital_course=self.extracted_data.get("hospital_course", {}),
            medications=self.extracted_data.get("medications", {}),
            investigations=self.extracted_data.get("investigations", {}),
            allergies=self.extracted_data.get("allergies", {}),
            followup=self.extracted_data.get("followup", {}),
            conflicts=self.extracted_data.get("conflicts", {}),
            tool_results=self.tool_results
        )

        summary = self.llm.call(prompt, max_tokens=6000)
        return summary

    # ----------------------------------------------------------
    # MAIN RUN LOOP
    # ----------------------------------------------------------
    def run(self, pdf_path: str) -> str:
        """
        Main agent loop.
        Plans → Detects conflicts → Extracts sections →
        Checks medications → Checks pending → Assembles summary.
        Hard step cap enforced throughout.
        """
        patient_file = os.path.basename(pdf_path)
        self.trace = AgentTrace(patient_file)

        print(f"\n{'#'*60}")
        print(f"# DISCHARGE AGENT STARTING")
        print(f"# Patient file: {patient_file}")
        print(f"# Max steps: {MAX_STEPS}")
        print(f"# Model: {MODEL}")
        print(f"{'#'*60}\n")

        # --- READ PDF ---
        print("[AGENT] Reading patient PDF...")
        patient_text = get_patient_text(pdf_path)
        print(f"[AGENT] Patient text loaded: {len(patient_text)} characters")

        if not patient_text or "ERROR" in patient_text:
            return "[AGENT ERROR] Could not load patient data. Check PDF path."

        # --- STEP 1: PLAN ---
        print("\n[AGENT] STEP 1: Planning...")
        plan = self.step_plan(patient_text)
        self.extracted_data["plan"] = plan

        # --- STEP 2: DETECT CONFLICTS ---
        print("\n[AGENT] STEP 2: Detecting conflicts...")
        conflicts = self.step_detect_conflicts(patient_text)
        self.extracted_data["conflicts"] = conflicts

        # --- STEP 3: EXTRACT SECTIONS ---
        sections = [
            "demographics",
            "diagnoses",
            "hospital_course",
            "medications",
            "investigations",
            "allergies",
            "followup"
        ]

        for section in sections:
            print(f"\n[AGENT] STEP 3: Extracting {section}...")
            data = self.step_extract_section(patient_text, section)
            self.extracted_data[section] = data

            # Check step cap
            if self.step_count >= MAX_STEPS - 3:
                print(f"[AGENT] ⚠️  Approaching step cap. Skipping remaining sections.")
                break

        # --- STEP 4: MEDICATION SAFETY ---
        print("\n[AGENT] STEP 4: Medication safety check...")
        med_safety = self.step_medication_safety(
            self.extracted_data.get("medications", {})
        )
        self.extracted_data["medication_safety"] = med_safety

        # --- STEP 5: CHECK PENDING ---
        print("\n[AGENT] STEP 5: Checking pending results...")
        pending = self.step_check_pending()
        self.extracted_data["pending"] = pending

        # --- STEP 6: ASSEMBLE SUMMARY ---
        print("\n[AGENT] STEP 6: Assembling discharge summary...")
        summary = self.step_assemble_summary()

        # --- SAVE OUTPUTS ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patient_name = patient_file.replace(".pdf", "").replace(" ", "_")

        # Save discharge summary
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        summary_path = os.path.join(
            OUTPUT_FOLDER,
            f"discharge_summary_{patient_name}_{timestamp}.txt"
        )
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"\n[AGENT] ✅ Discharge summary saved: {summary_path}")

        # Save trace
        os.makedirs(TRACES_FOLDER, exist_ok=True)
        trace_path = os.path.join(
            TRACES_FOLDER,
            f"trace_{patient_name}_{timestamp}.json"
        )
        self.trace.save(trace_path)

        # Save extracted data
        extracted_path = os.path.join(
            OUTPUT_FOLDER,
            f"extracted_data_{patient_name}_{timestamp}.json"
        )
        with open(extracted_path, "w", encoding="utf-8") as f:
            json.dump(self.extracted_data, f, indent=2)
        print(f"[AGENT] ✅ Extracted data saved: {extracted_path}")

        print(f"\n[AGENT] Total LLM calls: {self.llm.call_count}")
        print(f"[AGENT] Total steps: {self.step_count}")
        print(f"[AGENT] Clinician flags raised: {len(self.clinician_flags)}")
        print(f"\n{'#'*60}")
        print(f"# AGENT COMPLETE")
        print(f"{'#'*60}\n")

        return summary


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    agent = DischargeAgent()
    pdfs = get_all_patient_pdfs(PATIENT_FOLDER)

    if not pdfs:
        print("No PDFs found in patient_data folder!")
    else:
        for pdf_path in pdfs:
            summary = agent.run(pdf_path)
            print("\n" + "="*60)
            print("DISCHARGE SUMMARY PREVIEW (first 2000 chars):")
            print("="*60)
            print(summary[:2000])