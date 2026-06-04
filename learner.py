import os
import json
import glob
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

from pdf_reader import get_patient_text, get_all_patient_pdfs
from tools import get_available_tools
from reviewer import SimulatedDoctorReviewer

load_dotenv()

MODEL = "llama-3.3-70b-versatile"
PATIENT_FOLDER = "patient_data"
PART2_FOLDER = "part2"
os.makedirs(PART2_FOLDER, exist_ok=True)

# ============================================================
# PROMPT VARIANTS — the bandit chooses between these
# Each variant has different level of detail/structure
# Agent cannot see which variant is "best" — it learns
# ============================================================
PROMPT_VARIANTS = {
    "variant_A": {
        "name": "Minimal Structure",
        "description": "Basic extraction with minimal guidance",
        "system_suffix": """Keep the summary concise. 
Use bullet points only for medications and investigations.
Aim for brevity while covering all required sections."""
    },
    "variant_B": {
        "name": "Detailed Clinical",
        "description": "Detailed clinical language with full context",
        "system_suffix": """Be extremely detailed and clinical.
Include all lab values with reference ranges.
Write in formal medical language.
Include timestamps for all key events.
Flag every abnormal value explicitly."""
    },
    "variant_C": {
        "name": "Structured Template",
        "description": "Rigid template format matching doctor preferences",
        "system_suffix": """Follow this exact structure for every section:
- Start each section with a one-line summary
- List specific values, not ranges
- End every section with ACTION REQUIRED or NO ACTION NEEDED
- Use SOAP-style notes for hospital course
- Medications: always include dose, route, frequency, duration"""
    },
    "variant_D": {
        "name": "Safety First",
        "description": "Extra emphasis on flags and safety",
        "system_suffix": """Prioritize safety flags above all.
Lead every section with safety concerns if any exist.
Use RED FLAG: prefix for critical items.
Include a dedicated SAFETY SUMMARY at the top.
Make pending results the most prominent section."""
    },
    "variant_E": {
        "name": "Clinician Friendly",
        "description": "Optimized for quick clinician review",
        "system_suffix": """Format for a busy clinician who has 2 minutes to review.
Start with a 3-line executive summary.
Use checkboxes format: [ ] for items needing action.
Bold all critical values.
Put discharge medications first after demographics.
Keep hospital course to 5 bullet points maximum."""
    }
}


# ============================================================
# CONTEXTUAL BANDIT
# Learns which prompt variant produces drafts
# closest to what the doctor wants (lowest edit distance)
# ============================================================
class ContextualBandit:
    def __init__(self, variants: dict, epsilon: float = 0.2):
        self.variants = list(variants.keys())
        self.epsilon = epsilon  # exploration rate
        self.rewards = {v: [] for v in self.variants}
        self.counts = {v: 0 for v in self.variants}
        self.avg_rewards = {v: 0.5 for v in self.variants}  # start optimistic

    def select_variant(self) -> str:
        """
        Epsilon-greedy selection:
        - With probability epsilon: explore (random variant)
        - With probability 1-epsilon: exploit (best known variant)
        """
        if random.random() < self.epsilon:
            # Explore
            chosen = random.choice(self.variants)
            print(f"  [BANDIT] Exploring: selected {chosen} randomly")
        else:
            # Exploit — pick highest average reward
            chosen = max(self.avg_rewards, key=self.avg_rewards.get)
            print(f"  [BANDIT] Exploiting: selected {chosen} (avg reward: {self.avg_rewards[chosen]:.4f})")

        return chosen

    def update(self, variant: str, reward: float):
        """Update reward estimate for variant using incremental mean."""
        self.rewards[variant].append(reward)
        self.counts[variant] += 1
        # Incremental mean update
        n = self.counts[variant]
        old_avg = self.avg_rewards[variant]
        self.avg_rewards[variant] = old_avg + (reward - old_avg) / n
        print(f"  [BANDIT] Updated {variant}: new avg reward = {self.avg_rewards[variant]:.4f}")

    def get_best_variant(self) -> str:
        return max(self.avg_rewards, key=self.avg_rewards.get)

    def get_state(self) -> dict:
        return {
            "avg_rewards": self.avg_rewards,
            "counts": self.counts,
            "best_variant": self.get_best_variant(),
            "total_iterations": sum(self.counts.values())
        }


# ============================================================
# MINI AGENT — uses selected prompt variant
# Lighter version of main agent for learning iterations
# ============================================================
class MiniAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_draft(self, patient_text: str, variant_key: str) -> str:
        """
        Generates a discharge summary draft using the selected prompt variant.
        """
        variant = PROMPT_VARIANTS[variant_key]
        print(f"  [MINI_AGENT] Generating draft with variant: {variant['name']}")

        system_prompt = f"""You are a clinical AI agent producing discharge summary DRAFTS.

CORE RULES (NEVER BREAK):
1. NEVER invent clinical facts — use [MISSING] for undocumented fields
2. NEVER resolve diagnosis conflicts — flag them with CONFLICT
3. NEVER fill in pending results — mark as PENDING
4. This is always a DRAFT for clinician review

{variant['system_suffix']}"""

        user_prompt = f"""Produce a complete discharge summary draft from these patient notes.
Include all required sections:
1. Patient Demographics
2. Admission & Discharge Dates  
3. Principal Diagnosis
4. Secondary Diagnoses
5. Allergies
6. Hospital Course
7. Procedures Performed
8. Investigations & Results
9. Discharge Medications
10. Medication Reconciliation
11. Pending Results
12. Follow-up Instructions
13. Discharge Condition
14. Clinician Flags

PATIENT NOTES:
{patient_text[:8000]}"""

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=4000,
                    temperature=0.1
                )
                draft = response.choices[0].message.content
                print(f"  [MINI_AGENT] Draft generated ({len(draft)} chars)")
                return draft

            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    wait = (attempt + 1) * 20
                    print(f"  [MINI_AGENT] Rate limit hit. Waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"  [MINI_AGENT] Error: {e}")
                    return f"[DRAFT GENERATION FAILED: {str(e)}]"

        return "[DRAFT GENERATION FAILED: Max retries exceeded]"


# ============================================================
# LEARNING LOOP
# ============================================================
class LearningLoop:
    def __init__(self, n_iterations: int = 10):
        self.n_iterations = n_iterations
        self.bandit = ContextualBandit(PROMPT_VARIANTS, epsilon=0.3)
        self.mini_agent = MiniAgent()
        self.reviewer = SimulatedDoctorReviewer()
        self.results = []
        self.patient_context = """
        Patient: Male, approximately 45-55 years old
        Hospital: Sarji Super Speciality Hospital
        Admission: 26/02/2026, Discharge: 03/03/2026
        Primary: DKA, Uncontrolled T2DM (HbA1c 13.9%), AFI, B/L Pyelonephritis
        Discharge vitals: BP 170/80 mmHg, HR 110 bpm
        """

    def run(self, patient_text: str) -> dict:
        """
        Main learning loop:
        For each iteration:
          1. Bandit selects prompt variant
          2. Mini agent generates draft with that variant
          3. Simulated doctor edits the draft
          4. Calculate reward (edit distance)
          5. Bandit updates variant weights
          6. Track improvement over iterations
        """
        print(f"\n{'='*60}")
        print(f"LEARNING LOOP STARTING")
        print(f"Iterations: {self.n_iterations}")
        print(f"Variants: {list(PROMPT_VARIANTS.keys())}")
        print(f"{'='*60}\n")

        rewards_over_time = []

        for iteration in range(1, self.n_iterations + 1):
            print(f"\n--- ITERATION {iteration}/{self.n_iterations} ---")

            # Step 1: Select variant
            variant_key = self.bandit.select_variant()

            # Step 2: Generate draft
            draft = self.mini_agent.generate_draft(patient_text, variant_key)

            if "FAILED" in draft:
                print(f"  Skipping iteration {iteration} — draft generation failed")
                time.sleep(10)
                continue

            # Step 3: Doctor edits
            time.sleep(3)  # avoid rate limits
            edit_result = self.reviewer.review_and_edit(
                draft, self.patient_context
            )

            if "error" in edit_result:
                print(f"  Skipping iteration {iteration} — reviewer failed")
                time.sleep(10)
                continue

            # Step 4: Get reward
            reward = edit_result["metrics"].get("reward", 0.0)
            missing_filled = edit_result["metrics"].get("missing_fields_filled", 0)
            missing_before = edit_result["metrics"].get("missing_fields_before", 1)

            # Adjusted reward — penalize if many fields still missing
            # This prevents gaming by being vague
            if missing_before > 0:
                fill_rate = missing_filled / missing_before
                adjusted_reward = reward * 0.7 + fill_rate * 0.3
            else:
                adjusted_reward = reward

            print(f"  Raw reward: {reward:.4f}")
            print(f"  Fill rate: {missing_filled}/{missing_before}")
            print(f"  Adjusted reward: {adjusted_reward:.4f}")

            # Step 5: Update bandit
            self.bandit.update(variant_key, adjusted_reward)

            # Step 6: Record results
            iteration_result = {
                "iteration": iteration,
                "variant_key": variant_key,
                "variant_name": PROMPT_VARIANTS[variant_key]["name"],
                "reward": reward,
                "adjusted_reward": adjusted_reward,
                "missing_filled": missing_filled,
                "missing_before": missing_before,
                "edit_distance": edit_result["metrics"].get(
                    "normalized_edit_distance", 0
                ),
                "draft_length": len(draft),
                "bandit_state": self.bandit.get_state()
            }
            self.results.append(iteration_result)
            rewards_over_time.append(adjusted_reward)

            # Save draft and edit pair
            pair_path = os.path.join(
                PART2_FOLDER,
                f"pair_iter_{iteration}_{variant_key}.json"
            )
            with open(pair_path, "w", encoding="utf-8") as f:
                json.dump({
                    "iteration": iteration,
                    "variant": variant_key,
                    "draft": draft[:2000],  # truncate for storage
                    "edited": edit_result["edited_version"][:2000],
                    "metrics": edit_result["metrics"]
                }, f, indent=2)

            print(f"\n  Bandit state: {self.bandit.get_state()}")

            # Rate limit protection
            if iteration < self.n_iterations:
                print(f"  Waiting 5s before next iteration...")
                time.sleep(5)

        # Final results
        final_results = {
            "total_iterations": len(self.results),
            "results": self.results,
            "rewards_over_time": rewards_over_time,
            "final_bandit_state": self.bandit.get_state(),
            "best_variant": self.bandit.get_best_variant(),
            "improvement": self._calculate_improvement(rewards_over_time)
        }

        # Save results
        results_path = os.path.join(PART2_FOLDER, "learning_results.json")
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump(final_results, f, indent=2)

        print(f"\n[LEARNING] Results saved: {results_path}")
        print(f"\n{'='*60}")
        print(f"LEARNING COMPLETE")
        print(f"Best variant: {self.bandit.get_best_variant()}")
        print(f"Best variant name: {PROMPT_VARIANTS[self.bandit.get_best_variant()]['name']}")
        print(f"Improvement: {self._calculate_improvement(rewards_over_time)}")
        print(f"{'='*60}")

        return final_results

    def _calculate_improvement(self, rewards: list) -> dict:
        """Calculate before/after improvement metrics."""
        if len(rewards) < 2:
            return {"insufficient_data": True}

        first_half = rewards[:len(rewards)//2]
        second_half = rewards[len(rewards)//2:]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)
        improvement_pct = ((avg_second - avg_first) / avg_first * 100
                           if avg_first > 0 else 0)

        return {
            "avg_reward_first_half": round(avg_first, 4),
            "avg_reward_second_half": round(avg_second, 4),
            "absolute_improvement": round(avg_second - avg_first, 4),
            "percentage_improvement": round(improvement_pct, 2),
            "improved": avg_second > avg_first
        }


if __name__ == "__main__":
    print("Loading patient data...")
    pdfs = get_all_patient_pdfs(PATIENT_FOLDER)

    if not pdfs:
        print("No PDFs found!")
        exit()

    patient_text = get_patient_text(pdfs[0])
    print(f"Patient text loaded: {len(patient_text)} chars")

    # Run learning loop — 10 iterations
    loop = LearningLoop(n_iterations=10)
    results = loop.run(patient_text)

    print(f"\nFinal improvement curve:")
    for i, r in enumerate(results["rewards_over_time"]):
        bar = "█" * int(r * 20)
        print(f"  Iter {i+1:2d}: {bar} {r:.4f}")