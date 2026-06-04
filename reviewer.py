import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


class SimulatedDoctorReviewer:
    """
    A simulated clinician that applies a consistent editing policy
    to agent-generated discharge summary drafts.

    This produces (draft, edited) pairs for the learning loop.

    The doctor's editing policy (hidden from agent):
    1. Fill in [MISSING] fields with clinically reasonable values
    2. Resolve diagnosis conflicts by picking most clinically supported
    3. Make medication list more specific and complete
    4. Add specific follow-up dates and instructions
    5. Rewrite vague sentences to be more precise
    6. Add discharge vitals clearly
    7. Ensure drug interactions are prominently noted
    """

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.edit_history = []

    def review_and_edit(self, draft: str, patient_context: str = "") -> dict:
        """
        Takes an agent draft and returns an edited version.
        Also returns detailed edit annotations for learning signal.
        """
        print("\n[REVIEWER] Simulated doctor reviewing draft...")

        prompt = f"""You are an experienced hospital physician reviewing an AI-generated 
discharge summary draft. Apply your standard editing policy consistently.

YOUR EDITING POLICY (apply ALL of these):
1. Replace ALL [MISSING] fields with clinically appropriate values based on context
2. If diagnosis conflict exists, select the most clinically supported diagnosis as principal
3. Make medication list complete with doses, routes, frequencies, durations
4. Add specific follow-up: exact timeframes (e.g. "Review in 1 week" not just "follow up")
5. Rewrite vague clinical descriptions to be precise and professional
6. Ensure discharge condition includes specific vitals at time of discharge
7. Add drug interaction warnings prominently if present
8. Remove redundant or duplicate information
9. Ensure pending results section has clear action plan for each item
10. Add patient education points to follow-up section

PATIENT CONTEXT (use this to fill missing fields):
{patient_context}

DRAFT TO EDIT:
{draft}

Produce the edited discharge summary. Make it clinically precise and complete.
A real clinician should be able to use this directly without further editing.
Do not add fictional lab values — use [ESTIMATED] tag if you must estimate."""

        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an experienced physician editing clinical documents. Be precise, complete, and clinically accurate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=5000,
                temperature=0.2
            )

            edited = response.choices[0].message.content
            print(f"[REVIEWER] Edit complete. ({len(edited)} chars)")

            # Calculate edit metrics
            metrics = self._calculate_edit_metrics(draft, edited)

            result = {
                "original_draft": draft,
                "edited_version": edited,
                "metrics": metrics
            }

            self.edit_history.append(result)
            return result

        except Exception as e:
            print(f"[REVIEWER] Error: {e}")
            return {
                "original_draft": draft,
                "edited_version": draft,
                "metrics": {"error": str(e)},
                "error": str(e)
            }

    def _calculate_edit_metrics(self, original: str, edited: str) -> dict:
        """
        Calculates reward signal metrics between draft and edited version.
        Lower edit distance = better draft = higher reward.
        """
        # Normalized edit distance (Levenshtein approximation)
        orig_words = original.lower().split()
        edit_words = edited.lower().split()

        # Word-level diff
        orig_set = set(orig_words)
        edit_set = set(edit_words)

        words_removed = orig_set - edit_set
        words_added = edit_set - orig_set
        words_kept = orig_set & edit_set

        total_words = max(len(orig_set), len(edit_set))
        edit_distance = len(words_removed) + len(words_added)
        normalized_edit_distance = edit_distance / total_words if total_words > 0 else 0

        # Reward = 1 - normalized edit distance (higher = better draft)
        reward = max(0.0, 1.0 - normalized_edit_distance)

        # Count specific improvements
        missing_before = original.count("[MISSING")
        missing_after = edited.count("[MISSING")
        missing_filled = max(0, missing_before - missing_after)

        conflict_flags_before = original.count("CONFLICT")
        conflict_flags_after = edited.count("CONFLICT")

        pending_before = original.count("PENDING")
        pending_after = edited.count("PENDING")

        metrics = {
            "original_length": len(original),
            "edited_length": len(edited),
            "original_word_count": len(orig_words),
            "edited_word_count": len(edit_words),
            "words_removed": len(words_removed),
            "words_added": len(words_added),
            "words_kept": len(words_kept),
            "normalized_edit_distance": round(normalized_edit_distance, 4),
            "reward": round(reward, 4),
            "missing_fields_before": missing_before,
            "missing_fields_after": missing_after,
            "missing_fields_filled": missing_filled,
            "conflict_flags_before": conflict_flags_before,
            "conflict_flags_after": conflict_flags_after,
            "pending_items_before": pending_before,
            "pending_items_after": pending_after
        }

        print(f"[REVIEWER] Metrics:")
        print(f"  Edit distance (normalized): {normalized_edit_distance:.4f}")
        print(f"  Reward score: {reward:.4f}")
        print(f"  [MISSING] fields filled: {missing_filled}/{missing_before}")

        return metrics


if __name__ == "__main__":
    # Test with the latest discharge summary
    import glob

    summaries = glob.glob("output/discharge_summary_*.txt")
    if not summaries:
        print("No discharge summaries found. Run agent.py first.")
        exit()

    # Use most recent
    latest = sorted(summaries)[-1]
    print(f"Testing reviewer on: {latest}")

    with open(latest, "r", encoding="utf-8") as f:
        draft = f.read()

    # Patient context to help fill missing fields
    patient_context = """
    Patient: Male, approximately 45-55 years old (estimated from clinical context)
    Hospital: Sarji Super Speciality Hospital
    Admission: 26/02/2026, Discharge: 03/03/2026
    Primary issues: DKA, Uncontrolled T2DM (HbA1c 13.9%), AFI (Widal positive),
    B/L Pyelonephritis (CT confirmed), Cholelithiasis
    Discharge vitals: BP 170/80 mmHg, HR 110 bpm (still elevated at discharge)
    """

    reviewer = SimulatedDoctorReviewer()
    result = reviewer.review_and_edit(draft, patient_context)

    # Save edited version
    edited_path = latest.replace(
        "discharge_summary",
        "doctor_edited_summary"
    )
    with open(edited_path, "w", encoding="utf-8") as f:
        f.write(result["edited_version"])

    print(f"\n[REVIEWER] Edited summary saved: {edited_path}")
    print(f"\nMetrics: {json.dumps(result['metrics'], indent=2)}")
    print(f"\nPreview of edited summary (first 1000 chars):")
    print(result["edited_version"][:1000])