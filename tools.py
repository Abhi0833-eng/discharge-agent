import json
import time
import random

# ============================================================
# MOCK TOOLS — the agent decides when to call these
# In production these would call real APIs
# ============================================================

def check_drug_interactions(medications: list) -> dict:
    """
    Mock drug interaction checker.
    Agent calls this when it sees multiple medications.
    Returns interaction warnings if any found.
    """
    print(f"  [TOOL: drug_interaction_checker] Checking {len(medications)} medications...")
    time.sleep(0.3)  # simulate API call

    # Known interaction rules (mock database)
    interaction_rules = {
        ("meropenem", "valproate"): {
            "severity": "MAJOR",
            "description": "Meropenem significantly reduces valproate levels — may cause seizures"
        },
        ("tramadol", "ondansetron"): {
            "severity": "MODERATE",
            "description": "Tramadol + Ondansetron may increase risk of serotonin syndrome and QT prolongation"
        },
        ("tramadol", "emeset"): {
            "severity": "MODERATE",
            "description": "Tramadol + Ondansetron (Emeset) — QT prolongation risk"
        },
        ("ultracet", "tramadol"): {
            "severity": "MAJOR",
            "description": "Ultracet contains tramadol — duplication if both prescribed"
        },
        ("noradrenaline", "tramadol"): {
            "severity": "MODERATE",
            "description": "Noradrenaline + Tramadol — increased risk of serotonin syndrome"
        },
        ("lantus", "dolo"): {
            "severity": "LOW",
            "description": "No significant interaction. Monitor blood glucose."
        },
        ("etoshine", "ultracet"): {
            "severity": "MODERATE",
            "description": "Both are analgesics — monitor for additive effects and GI side effects"
        }
    }

    found_interactions = []
    meds_lower = [m.lower().strip() for m in medications]

    # Check all pairs
    for i in range(len(meds_lower)):
        for j in range(i + 1, len(meds_lower)):
            pair1 = (meds_lower[i], meds_lower[j])
            pair2 = (meds_lower[j], meds_lower[i])

            if pair1 in interaction_rules:
                interaction = interaction_rules[pair1].copy()
                interaction["drug1"] = medications[i]
                interaction["drug2"] = medications[j]
                found_interactions.append(interaction)
            elif pair2 in interaction_rules:
                interaction = interaction_rules[pair2].copy()
                interaction["drug1"] = medications[j]
                interaction["drug2"] = medications[i]
                found_interactions.append(interaction)

    result = {
        "tool": "drug_interaction_checker",
        "medications_checked": medications,
        "interactions_found": len(found_interactions),
        "interactions": found_interactions,
        "status": "completed"
    }

    if found_interactions:
        print(f"  [TOOL: drug_interaction_checker] ⚠️  {len(found_interactions)} interaction(s) found!")
    else:
        print(f"  [TOOL: drug_interaction_checker] ✅ No major interactions found.")

    return result


def flag_for_clinician_review(issue_type: str, details: str, severity: str = "HIGH") -> dict:
    """
    Escalation tool — agent calls this when it finds something
    that requires clinician attention before finalization.
    severity: HIGH, MEDIUM, LOW
    """
    print(f"  [TOOL: escalation] 🚨 Flagging: {issue_type} [{severity}]")
    time.sleep(0.1)

    valid_severities = ["HIGH", "MEDIUM", "LOW"]
    if severity not in valid_severities:
        severity = "HIGH"

    result = {
        "tool": "clinician_escalation",
        "issue_type": issue_type,
        "severity": severity,
        "details": details,
        "action": "FLAGGED_FOR_CLINICIAN_REVIEW",
        "status": "escalated"
    }

    return result


def reconcile_medications(admission_meds: list, discharge_meds: list) -> dict:
    """
    Compares admission vs discharge medications.
    Flags additions, discontinuations, and changes.
    """
    print(f"  [TOOL: med_reconciliation] Comparing admission vs discharge medications...")
    time.sleep(0.2)

    admission_lower = {m.lower().strip(): m for m in admission_meds}
    discharge_lower = {m.lower().strip(): m for m in discharge_meds}

    added = []
    stopped = []
    continued = []

    for med in discharge_lower:
        if med not in admission_lower:
            added.append(discharge_lower[med])
        else:
            continued.append(discharge_lower[med])

    for med in admission_lower:
        if med not in discharge_lower:
            stopped.append(admission_lower[med])

    result = {
        "tool": "medication_reconciliation",
        "added_at_discharge": added,
        "stopped_at_discharge": stopped,
        "continued": continued,
        "reconciliation_flags": [],
        "status": "completed"
    }

    # Flag stops without documented reason
    for med in stopped:
        result["reconciliation_flags"].append({
            "medication": med,
            "flag": "STOPPED — no documented reason found. Clinician must verify.",
            "severity": "MEDIUM"
        })

    # Flag new additions
    for med in added:
        result["reconciliation_flags"].append({
            "medication": med,
            "flag": "NEW at discharge — verify indication and patient education given.",
            "severity": "LOW"
        })

    print(f"  [TOOL: med_reconciliation] Added: {len(added)}, Stopped: {len(stopped)}, Continued: {len(continued)}")
    return result


def check_pending_results(investigations: list) -> dict:
    """
    Checks which investigations are still pending.
    Agent calls this before finalizing discharge summary.
    """
    print(f"  [TOOL: pending_results_checker] Checking {len(investigations)} investigations...")
    time.sleep(0.1)

    # Simulate some pending, some resulted
    pending = []
    resulted = []

    for inv in investigations:
        inv_lower = inv.lower()
        # Known pending from records
        if any(keyword in inv_lower for keyword in [
            "blood culture", "contrast ct", "hba1c repeat",
            "urology follow", "blood c/s"
        ]):
            pending.append({
                "investigation": inv,
                "status": "PENDING",
                "action_required": "Follow up result and review with clinician"
            })
        else:
            resulted.append({
                "investigation": inv,
                "status": "RESULTED"
            })

    result = {
        "tool": "pending_results_checker",
        "total_checked": len(investigations),
        "pending_count": len(pending),
        "resulted_count": len(resulted),
        "pending_items": pending,
        "resulted_items": resulted,
        "status": "completed"
    }

    if pending:
        print(f"  [TOOL: pending_results_checker] ⚠️  {len(pending)} result(s) still PENDING!")
    else:
        print(f"  [TOOL: pending_results_checker] ✅ All results available.")

    return result


def get_available_tools() -> list:
    """
    Returns list of tools available to the agent.
    Agent reads this at start to know what it can use.
    """
    return [
        {
            "name": "check_drug_interactions",
            "description": "Check for drug-drug interactions between medications",
            "when_to_use": "Always call when multiple discharge medications identified",
            "parameters": ["medications (list of medication names)"]
        },
        {
            "name": "flag_for_clinician_review",
            "description": "Escalate a clinical concern for mandatory clinician review",
            "when_to_use": "Call when: missing data, conflicts found, safety concerns, abnormal values",
            "parameters": ["issue_type (string)", "details (string)", "severity (HIGH/MEDIUM/LOW)"]
        },
        {
            "name": "reconcile_medications",
            "description": "Compare admission vs discharge medications and surface changes",
            "when_to_use": "Always call to identify medication changes during hospitalization",
            "parameters": ["admission_meds (list)", "discharge_meds (list)"]
        },
        {
            "name": "check_pending_results",
            "description": "Identify which investigations are still pending at discharge",
            "when_to_use": "Always call before finalizing discharge summary",
            "parameters": ["investigations (list of investigation names)"]
        }
    ]


if __name__ == "__main__":
    print("=== Testing Tools ===\n")

    # Test 1: Drug interactions
    print("Test 1: Drug Interaction Check")
    result = check_drug_interactions([
        "Meropenem", "Tramadol", "Emeset",
        "Lantus", "Dolo", "Ultracet", "Etoshine"
    ])
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Test 2: Escalation
    print("Test 2: Escalation Tool")
    result = flag_for_clinician_review(
        issue_type="DIAGNOSIS_CONFLICT",
        details="Multiple conflicting diagnoses found across documents",
        severity="HIGH"
    )
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Test 3: Medication Reconciliation
    print("Test 3: Medication Reconciliation")
    result = reconcile_medications(
        admission_meds=["Ayurvedic DM medication"],
        discharge_meds=["Tab. Dolo 650mg", "Tab. Ultracet", "Tab. Etoshine", "Inj. Lantus 10U"]
    )
    print(f"Result: {json.dumps(result, indent=2)}\n")

    # Test 4: Pending Results
    print("Test 4: Pending Results Check")
    result = check_pending_results([
        "Blood Culture & Sensitivity",
        "Contrast CT KUB",
        "CBC",
        "Serum Creatinine",
        "Urine Routine"
    ])
    print(f"Result: {json.dumps(result, indent=2)}\n")