# Pre-extracted clinical text from Patient 2 PDF (image-based scanned document)
# Extracted by Claude vision reading of all 71 pages
# This is the ground truth data the agent will reason over

PATIENT_2_TEXT = """
=== PATIENT 2 CLINICAL RECORDS ===
Source: Sarji Super Speciality Hospital
Total Pages: 71 (image-based scanned document)

--- ADMISSION DETAILS ---
Date of Admission: 26/02/2026
Time of Admission: 6:14 PM (ER arrival)
Date of Discharge: 03/03/2026
Department: Internal Medicine (HDU/SDICU/Ward)
Weight: 71 kg
Patient Gender: Male (referred to as 'he' in notes)
Patient Name: [NOT DOCUMENTED IN RECORDS]
Age: [NOT DOCUMENTED IN RECORDS]
IP Number: [NOT DOCUMENTED IN RECORDS]
Blood Group: [NOT DOCUMENTED IN RECORDS]

--- ALLERGIES ---
Known Drug Allergies: NOT KNOWN (consistent across all pages)

--- CHIEF COMPLAINTS (Admission Record) ---
- Fever
- Generalized weakness since 3 days
- Myalgia (+)

--- HISTORY OF PRESENT ILLNESS ---
Patient on regular medication (Ayurvedic medication for T2DM).
Gradually complaints of fever, myalgia, generalized weakness.
Came to hospital for further management.
Past History: Known case of T2DM (on Ayurvedic medication)
HbA1c: 13.9% (outside report) — very poorly controlled diabetes

--- ER OBSERVATION (26/02/2026 @ 6:14 PM) ---
Triage Category: Yellow
ER Diagnosis: DKA (Diabetic Ketoacidosis)
Vital Signs on Arrival:
  - Pulse: 116 b/min
  - BP: 87/50 mmHg (HYPOTENSION - CRITICAL)
  - RR: 22 b/min
  - Temperature: 98°F
  - SaO2 on air: 96%
  - GCS: 15/15
  - Blood Glucose: 443 mg/dL (CRITICAL - very high)
  - Pain Score: 4/10
Procedure in ER: IV Cannulation done in left hand 20G

--- ER INVESTIGATIONS ORDERED ---
CBC, Creatinine, Serum Electrolytes, ABG, Urine Routine, ECG

--- ER MEDICATIONS GIVEN ---
- Inj. PAN 40mg IV @ 6:14 PM
- Inj. EMESET 4mg IV @ 6:14 PM
- Inf. NS 2 Bolus (6:14 PM to 9:00 PM)
- Inj. Sodium Bicarbonate 25ml in NS x 2 cycles (as per advice)

--- NURSING ASSESSMENT ON ADMISSION ---
Date: 26/02/2026 @ 6:14 PM
Complaints: Fever, generalized weakness since 3 days
Oriented: Yes
Level of Consciousness: Conscious
Speech: Clear
Visual Impairment: None
Extremity Strength: Equal
Pupils: Equal, Reactive
Hearing Impairment: None
Pain: Yes — Location: Body
Pain Scale: Mild pain (2/10)
Airway: Clear
Dyspnea: Absent
Wheezing: No
Cough: Yes
Sputum: Yes
Edema: Absent
Skin Perfusion: Warm
Skin Color: Fresh/Normal
Mucous Membrane: Intact
Moisture: Dry/Clammy
Gastrointestinal: Loss of Appetite Yes, Nausea/Vomiting/Diarrhoea present
Abdomen: Soft
Swallowing difficulty: No
Genitourinary: Dysuria Yes, Hematuria No, Incontinence No
Any Drug Allergy: NOT KNOWN

--- ADMISSION RECORD (Case Record 1, 2, 3) ---
Provisional Diagnosis: TAFE (Typhoid and Febrile Episode) + Uncontrolled T2DM
Final Diagnosis (Admission Record):
  - ? Synovitis
  - Cholelithiasis without cholecystitis

Examination on Admission:
  - O/E: Conscious, oriented
  - General Physical: Well built
  - PR: 116 b/min
  - BP: 87/50 mmHg
  - RR: 16 b/min
  - SPO2: 99%
  - GRBS: 443 mg/dL
  - Temp: 98.3°F
  - CNS: GCS M6/V5/E4 = 15/15, Pupils bilateral equal
  - CVS: S1S2 heard, no murmurs
  - RS: Normal effort, bilateral air entry equal
  - PA: Soft, no distension

Investigations ordered: CBC, Sr. Creatinine, Electrolytes, ABG, Urine Routine

--- CONSULTATION SHEETS ---

Consultation 1 — 27/02/2026 @ 11:30 AM (CSIB Dr.)
  Diagnosis: Uncontrolled T2DM, AKI
  Condition: Fair
  O/E: BP 110/70 mmHg, PR 117 bpm, SPO2 94%
  CNS: Conscious, oriented; CVS: S1S2+; RS: B/L AE+; PA: Soft
  Advice:
    - USG Abdomen & Pelvis STAT
    - GRBS 2nd hourly
    - CBC, S.Creat, Urine Routine @ 3PM
    - S.Na+
    - Shift to ward by evening

Consultation 2 — 27/02/2026 @ 6:00 PM (CSIB Dr.)
  Echo done:
    - Sinus tachycardia @ HR 149 bpm
    - Normal LV systolic function
    - No definite RWMA
    - LVEF: 60%
    - AR-Trivial, No AS
    - MR-Trivial
    - TR-Mild (gradient 28 mmHg)
    - No PAH
    - IVC 12/6 mm, Normal Collapsing
    - No clot/pericardial effusion

Consultation 3 — 27/02/2026 @ 6:20 PM (CSIB Dr.)
  Diagnosis: USG s/o pyelonephritis
  O/E: BP 96/60 mmHg, HR 116 bpm, SPO2 99% on O2, CNS: Conscious
  CVS: S1S2+; RS: B/L NVBS+; PA: Soft, diffuse tenderness
  Advice:
    - CT KUB
    - Urologist opinion
    - CBC, Sr. Creat TIM
    - Rx as per chart

Consultation 4 — 28/02/2026 @ 11:40 AM (CSIB Dr.)
  Condition: Fair
  O/E: BP 110/70, PR 114 bpm, SPO2 96.7%
  Advice:
    - Urologist opinion
    - CBC, S.Creat TIM
    - Shift to ward
    - Rx as per chart

Consultation 5 — 28/02/2026 @ 11:45 AM (S/B Dr. — Urologist)
  Thanks for referral. History noted. Reports noted.
  CT-KUB films noted.
  Assessment: Reassured. Continue same treatment.

Consultation 6 — 28/02/2026 @ 5:34 PM (CSIB Dr.)
  Case reviewed.
  Case of AFI, DKA, Uncontrolled T2DM, B/L Pyelonephritis
  C/o Dryness of mouth. Febrile @ 4PM — 102.2°F
  O/E: BP 130/60 mmHg, HR 135 bpm, SPO2 91% @ RA
  CNS: Conscious, oriented; CVS: S1S2+; RS: B/L AE+; PA: Soft
  Advice:
    - CBC, Sr. Creat GRBS 297 TIM
    - FC remove STAT
    - 8th hourly GRBS monitoring

Consultation 7 — 01/03/2026 @ 11:30 AM (CSIB Dr. — Physician)
  Care reviewed. Patient stable.
  1 episode of chills yesterday night.
  No fever spike currently.
  Symptomatically better now.
  BP 110/30mmHg, PR 80bpm, SPO2 58.6% @RA
  Advice: CST (Continue Same Treatment)

Consultation 8 — 02/03/2026 @ 11:25 AM (CSIB Dr.)
  Case of AFI, DKA, Uncontrolled T2DM, B/L Polynephritis
  O/E: BP 170/80 mmHg, SPO2 97%, HR 110 b/m
  CNS: Conscious, oriented; CVS: S1S2+
  Advice: Ortho Opinion, Discharge on Request (Evening), Diet Counselling

Consultation 9 — 02/03/2026 @ 11:56 AM (S/B Dr. — Orthopaedics)
  Thanks for reference. History noted.
  C/o pain (+) hip region
  O/E: Tenderness (+), Range of movement painful and restricted
  H/o R tibia operated 3 years back
  Advice:
    - X-ray pelvis bilateral hips AP view
    - Xray done — fracture united well
    - Rx: ? Synovitis
    - Tab. Ultracet 1-0-1 x 5 days
    - Tab. Etoshine — Continue current medication

Consultation 10 — 02/03/2026 @ 1:00 PM (Dietician — CSIB)
  Case of AFI, DKA, B/L Pyelonephritis, Uncontrolled T2DM on Ayurvedic medication
  Diet counselling done and diet chart issued
  Advice:
    - Strict diet modification
    - Allow low GI foods
    - Include fiber rich foods

Consultation 11 — 03/03/2026 @ 11:25 AM (CSIB Dr.)
  Case of AFI, DKA, Uncontrolled T2DM, B/L Polynephritis
  O/E: BP 170/80mmHg, SPO2 97+%, HR 110 b/m
  Advice: Ortho Opinion, Discharge on Request (Evening), Diet Counselling

--- DIAGNOSES ACROSS DOCUMENTS (CONFLICTS FLAGGED) ---
CONFLICT FLAG: Multiple diagnoses found across documents:
  1. ER Chart: DKA (Diabetic Ketoacidosis)
  2. Admission Record Provisional: TAFE + Uncontrolled T2DM
  3. Admission Record Final: ? Synovitis + Cholelithiasis without cholecystitis
  4. Consultation Sheets (28/02 onwards): AFI + DKA + Uncontrolled T2DM + B/L Pyelonephritis
  5. Latest Consultation (03/03): AFI + DKA + Uncontrolled T2DM + B/L Polynephritis
  NOTE: Clinician must confirm final diagnosis — agent cannot resolve this conflict.

--- LABORATORY RESULTS ---

BLOOD GLUCOSE MONITORING (Diabetic Chart):
  28/02/2026:
    - Before Lunch (BL): 267 mg/dL
    - After Dinner (AD): 380 mg/dL
    - Insulin: 16U (BL), 30U (AD)
  01/03/2026:
    - BBF: 265 mg/dL, BL: 178 mg/dL, AD: 270 mg/dL
    - Insulin: 22U H.A (BBF), 12-14U Bi-Lantus (BL), 12-8U (AD)
  02/03/2026:
    - BBF: 217 mg/dL, BL: 167 mg/dL
    - Insulin: 18U H.A (BBF), 12EU Tus Lantus (BL)

CBC RESULTS:
  Date 28/02/2026:
    - Hb: 10.4 gm/dL (LOW — ref 13.5-17.5)
    - TLC: 7820 cells/cumm (normal)
    - Platelet: 1.38 Lakhs (LOW — ref 1.5-4.5)

  Date 13/03/2026 (note: likely 01/03/2026):
    - Hb: 10.7 gm/dL (LOW)
    - TLC: 11560 cells/cumm (HIGH — leukocytosis)
    - Neutrophils: 83.9% (HIGH — neutrophilia)
    - Lymphocytes: 9.2%
    - Platelet: 1.60 Lakhs
    - PCV: 32.4% (LOW)
    - MCV: 78.5 fL (LOW — microcytosis)

  CBC (Another report):
    - Hb: 12.0 gm/dL
    - TLC: 6680 cells/cumm
    - Neutrophils: 79.1% (HIGH)
    - Platelet: 1.80 Lakhs
    - PCV: 35.9% (LOW)
    - MCV: 78.6 fL (LOW)

  CBC (Another report — 13/03/2026):
    - Hb: 11.4 gm/dL
    - TLC: 7160 cells/cumm
    - Neutrophils: 78% (HIGH)
    - Platelet: 2.56 Lakhs

BIOCHEMISTRY:
  Serum Creatinine:
    - 28/02/2026: 1.02 mg/dL (normal range 0.7-1.4)
    - 01/03/2026: 1.04 mg/dL (normal)
    - Another report: 0.85 mg/dL (normal)
    - Another report: 1.07 mg/dL (normal)

  Random Blood Sugar (RBS): 496 mg/dL (CRITICAL HIGH)
  Serum Sodium: 127 mmol/L (CRITICALLY LOW — ref 135-150) — HYPONATREMIA
  Serum Potassium: 3.84 mmol/L (normal)
  Serum Chloride: 84.90 mmol/L (LOW — ref 90-108)

ABG (Arterial Blood Gas):
  pH: 7.39 (low normal — ref 7.35-7.45)
  pCO2: 32 mmHg (LOW — compensatory hyperventilation)
  pO2: 72 mmHg (LOW)
  Sodium [Na+]: 114 mmol/L (CRITICALLY LOW)
  Potassium [K+]: 2.65 mmol/L (LOW — hypokalemia)
  Chloride [Cl-]: 83 mmol/L (LOW)
  cCALCIUM: 0.71 mmol/L (LOW — ref 1.15-1.33)
  HCT: 36%
  Haemoglobin: 11.60 g/dL (LOW)
  SO2(C): 94.20%
  HCO3: 19.20 mmol/L (LOW — ref 20-28, metabolic acidosis)
  Base Excess: -5.80 mmol/L (negative — metabolic acidosis)
  Lactate: 0.80 mmol/L (normal)

SEROLOGY:
  CRP (C-Reactive Protein): 80.23 mg/L (MARKEDLY ELEVATED — Adults ref <5.0 mg/L)
  Mean Blood Glucose: 352.2 mg/dL (CRITICAL)
  Widal Test:
    - Salmonella typhi "O": POSITIVE 1:160 (SIGNIFICANT)
    - Salmonella typhi "H": POSITIVE 1:80 (SIGNIFICANT)
    - Salmonella paratyphi "AH": Negative
    - Salmonella paratyphi "BH": Negative
  NOTE: Widal positive confirms typhoid fever (AFI)

HbA1c: 13.9% (outside report — ref <7% for controlled DM) — SEVERELY UNCONTROLLED

URINE ROUTINE (Multiple reports):
  Report 1:
    - pH: 5.5, Color: Pale Yellow, Appearance: Slightly Turbid
    - Albumin: Present+, Sugar: Present 1.5%, Ketones: Present+
    - Pus Cells: 4-5/hpf, Epithelial Cells: 1-2/hpf, RBCs: 2-3/hpf
    - Bacteria: Absent, Nitrite: Absent
    - Impression: Amorphous Urates Present

  Report 2 (later):
    - pH: 5.5, Color: Yellow, Appearance: TURBID
    - Albumin: Present++, Sugar: Present 1.0%, Ketones: Present+++
    - Bile Salt: Present, Bile Pigment: Present
    - Pus Cells: 3-4/hpf, Epithelial Cells: 2-3/hpf, RBCs: 2-3/hpf
    - Bacteria: Absent, Nitrite: Absent
    - Impression: GRANULAR CAST PRESENT

URINE CULTURE AND SENSITIVITY:
  Result: NO SIGNIFICANT BACTERIURIA
  Colony count: Less than 10,000 CFU/ML
  CONFLICT FLAG: Clinical diagnosis of B/L Pyelonephritis made on CT findings,
  but urine culture is NEGATIVE. Clinician must review this discrepancy.

--- IMAGING RESULTS ---

USG ABDOMEN & PELVIS (Bedside):
  - Liver (17cm): Enlarged, diffuse Grade I fatty infiltration. No focal lesion.
    No IHBR/EHBR dilatation. CBD not dilated.
  - Gall Bladder: Well distended, normal wall thickness.
    Conglomerated calculus measuring 13mm. No pericholecystic fat stranding.
  - Spleen (11cm): Normal size and echotexture.
  - Pancreas: Normal.
  - Both Kidneys: Mildly bulky. Normal shape, position, echotexture.
    Corticomedullary differentiation maintained.
    Right kidney: 12.0cm. No hydronephrosis. No calculi.
    Left kidney: 12.3cm. No hydronephrosis. No calculi.
  - HRUSG: No significant mass/collection.
  - Urinary Bladder: Empty. Foley's bulb in situ.
  - Prostate: Suboptimal.
  - Minimal ascites.
  - Minimal right pleural effusion with underlying subsegmental lung consolidation.
  USG IMPRESSION:
    1. Mild hepatomegaly with Grade I fatty infiltration
    2. Cholelithiasis without cholecystitis
    3. Mildly bulky bilateral kidneys — suggested RFT correlation towards pyelonephritis
    4. Minimal ascites
    5. Minimal right pleural effusion with underlying subsegmental lung consolidation

CT KUB (PLAIN) — Clinical data: Uncontrolled T2DM:
  Kidneys:
    - Bilateral perinephric fat plane stranding noted
    - Both kidneys mildly bulky
    - Right kidney: 12.3 x 6.4 x 6.5 cm. No hydroureteronephrosis. No calculus.
    - Left kidney: 12.0 x 6.0 x 6.1 cm. No hydroureteronephrosis.
      Tiny 1-2mm calculus in lower pole (496 HU)
    - Mild bilateral anterior pararenal (Gerota's), posterior pararenal (Zuckerkandl's)
      and lateral conal fascial thickening
    - No demonstrable calculus in ureters bilaterally
  - Urinary Bladder: Partially distended. Foley's bulb in situ.
  - Spleen: Normal.
  - Liver: Enlarged (20.0cm)
  - Gall Bladder: Conglomerated calculus ~1.4cm in neck
  - Pancreas: Grossly unremarkable
  - Minimal ascites
  - Bilateral mild pleural effusion with underlying subsegmental lung consolidation
  CT KUB IMPRESSION:
    1. Both kidneys mildly bulky with perinephric fat plane stranding —
       FEATURES LIKELY SUGGESTIVE OF ACUTE PYELONEPHRITIS
       Suggested contrast study for further evaluation
    2. Tiny left renal calyceal calculus
    3. Hepatomegaly
    4. Cholelithiasis without cholecystitis
    5. Minimal ascites
    6. Bilateral mild pleural effusion with underlying subsegmental lung consolidation

ECHO (Trans-Thoracic — 27/02/2026):
  - Left Atrium: Normal
  - Right Atrium: Normal
  - Mitral Valve: Normal (MR-Trivial)
  - Tricuspid Valve: Normal (TR-Mild, gradient 28 mmHg)
  - Aortic Valve: Normal (AR-Trivial)
  - Pulmonary Valve: Normal
  - Left Ventricle: Normal (LVEF 60%)
  - Right Ventricle: Normal
  - Interatrial Septum: Intact
  - Interventricular Septum: Intact
  - Pericardium: No Pericardial Effusion
  - Thrombus/Vegetation: Nil
  - Other: Sinus Tachycardia (HR-149bpm), IVC 12/6mm Normal Collapsing
  ECHO FINAL DIAGNOSIS:
    - No definite RWMA
    - Normal LV Systolic Function
    - LVEF 60%
    - AR/MR Trivial
    - TR Mild
    - No clot/vegetation

ECG: Done (26/02/2026) — report not separately documented

--- PROCEDURES PERFORMED ---
  1. IV Cannulation: 26/02, 27/02, 28/02, 01/03, 02/03 (multiple sites, 18-20G)
  2. Foley's Catheterisation: Inserted 26/02/2026, Removed 02/03/2026 (F/C 16 number)
  3. ECG: Done 26/02/2026
  4. USG Abdomen & Pelvis: Done 27/02/2026
  5. CT KUB (Plain): Done 28/02/2026 (bill paid, scan done)
  6. ECHO (Trans-Thoracic): Done 27/02/2026
  7. Blood Culture & Sensitivity: Sent (27/02/2026 due to fever spike)
  8. Urine Culture & Sensitivity: Sent, Result: No significant bacteriuria
  9. Urine Routine: Multiple times
  10. Widal Test: Done — Positive
  11. CRP: Done — Elevated 80.23 mg/L
  12. ABG: Done
  13. X-ray Pelvis B/L Hips AP View: Done (02/03/2026) — Fracture united well
  14. PD Sets & Vein O Line: Done multiple days
  15. Oxygen therapy: Given on 26/02/2026
  16. CAUTI monitoring: Active (Foley inserted 26/02 @ 8:58 PM)
  17. Bed sores assessment: No bed sores (26/02, 27/02, 28/02)
  18. Phototherapy: Done 27/02/2026

--- INPATIENT MEDICATIONS (Drug Charts) ---

ICU/HDU MEDICATIONS:
  1. Inj. MEROPENEM 1g IV TDS (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  2. Inj. PAN (Pantoprazole) 40mg IV OD (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  3. Inj. EMESET (Ondansetron) 4mg IV TDS (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  4. Inj. SUMOL (Paracetamol) 1g IV SOS (started 28/02/2026)
  5. Inj. HAPPYNERVE PLUS 1 amp IV OD (started 28/02/2026)
     - Given: 28/02, 01/03 only
  6. Inj. LANTUS (Insulin Glargine) 10U SC OD (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  7. Inj. H.ACTRAPID (Regular Insulin) S/C TDS sliding scale (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  8. Tab. DOLO (Paracetamol) 650mg PO TDS (started 28/02/2026)
     - Given: 28/02, 01/03, 02/03
  9. B80 SEP GEL (topical) EIA (started 01/03/2026) — Orthopaedic
  10. Inj. Gallium Noradrenaline 25mg IV (STAT — given for hypotension episode)
  11. Inj. Human Actrapid (sliding scale insulin) — given multiple times
  12. Inf. NS/RL @ 150ml/hr (IV fluids)
  13. Inf. DNS @ 150ml/hr (when GRBS < 200 mg/dL)
  14. Inj. Tramadol 2ml + 3ml NS = 5ml, 3ml IV (given for chills episode 27/02 night)
  15. Inj. PCT (Paracetamol) 1gm IV (given for fever spike 102°F, 12PM 27/02)
  16. Inj. Noradrenaline infusion (for septic shock/hypotension)

--- NURSING DOCUMENTATION SUMMARY ---

26/02/2026 (ER to HDU):
  - Patient received from casualty to HDU
  - Vital signs connected and monitored
  - IV cannulation done 20G right hand
  - IV medications given
  - Blood investigations sent to lab
  - ECG done
  - Patient provisioned to bed
  - Patient case and blood reports informed to Dr. Shunya Campael
  - Patient admission to HDU, handed to 3rd floor HDU evening staff
  - Episode of hypotension — NS 200ml bolus given as per advice
  - Episode of chills — Tramadol 2ml+3ml NS IV given
  - Sudden desaturation — O2 mask connected
  - Foley's catheterisation done @ 2AM as per advice

27/02/2026:
  - Patient charge handover from night to morning duty staff
  - Vitals: BP 108/64, SpO2 96%, HR 114 b/m, RR 28 b/m
  - Patient seen by Dr., Sir advised:
    * CBC, Sr. Creat TIM
    * USG Abdomen & Pelvis (done @ 3:55 PM — report awaited)
    * Urine Routine, Blood C/S sent
  - CT KUB cancelled at 11PM due to night duty time and patient's condition
  - Patient fever spike 103°F at 12PM — PCT 1gm given
  - 1 episode of chills and tachycardia — Tramadol given
  - GRBS checked and recorded
  - At 6AM: Inj. Emeset 4mg, Inj. PAN 40mg, Inj. Meropenem 1gm, Inj. HappyNerve Plus given

28/02/2026:
  - Patient received to SDICU 1st floor
  - CT KUB done, Jelly done (report awaited)
  - Patient shifted to ward — urine opening
  - Patient seen by Dr. Sir Adv: CBC/Sr. Creatinine TIM, CST
  - Patient all reports given from ICU to ward staff
  - GRBS checked every 2 hours
  - Patient charge handover given to SRICU staff to ward staff
  - Patient oral medication advised as per drug chart
  - Patient seen by Dr. Sir — Adv: discharge
  - On request of ortho opinion — patient seen by ortho Dr.
  - 12PM: Advice X-ray after review, inform report

01/03/2026 (13/03 in some notes):
  - Patient sleep sounds done, no fresh complaints
  - Patient IV medications given as per drug chart
  - GRBS checked and recorded
  - Patient CBC, S.Creat sent to lab, report due
  - Patient change handover to morning duty staff
  - Temp 100°F — informed duty doctor, Sir to advise CST

02/03/2026:
  - Patient change handover from night to morning duty staff
  - Vitals checked and recorded — monitoring chart
  - Oral medications advised as per drug chart
  - Patient seen by Dr. Sir — discharge advised
  - On request of ortho opinion
  - Patient seen by Dr. — advice X-ray after review inform report
  - 12PM: Patient sent to discharge summary & billing
  - Advice medications explained, health education given
  - OPD file, original summary, all original reports sent to patient attendants
  - IV cannula NOT removed at discharge (noted in discharge checklist)
  - Billing cleared, patient got discharge @ 4PM

--- DISCHARGE CHECK LIST ---
1. Patient Details: [NOT FILLED IN DISCHARGE CHECKLIST]
2. Discharge Summary: Given
3. Discharge Medication: Advised by Dr.
4. Blood Reports: Given
5. Radiology Reports CT/X-Ray: Given
6. USG Reports: Given
7. MRI Reports: N/A
8. ECG: Given
9. ECHO: Given
10. Patient IP Bands: Removed
11. IV Cannula: NOT REMOVED at discharge — FLAG FOR REVIEW
12. CVP: N/A
13. Oxygen: N/A
14. Other Reports or Forms: Given
15. OPD File and Old Reports: Given
16. Billing Clearance: Cleared
17. ICU Chart: Attached

--- DISCHARGE MEDICATIONS ---
CRITICAL FLAG: No formal discharge prescription sheet found in the records.
Discharge medications were "advised by Dr." per checklist but not documented
in a separate prescription format.

The following medications were being given at time of discharge and
may constitute discharge medications — CLINICIAN MUST VERIFY AND CONFIRM:
  From Drug Charts (last entries 02/03/2026):
  1. Tab. DOLO (Paracetamol) 650mg PO TDS — ongoing
  2. Inj. LANTUS (Glargine) 10U SC OD — ongoing (insulin — requires discharge plan)
  3. Inj. H.ACTRAPID sliding scale — ongoing (insulin — requires discharge plan)
  4. B80 SEP GEL (topical) — ongoing (ortho)

  From Ortho Consultation (02/03/2026):
  5. Tab. ULTRACET 1-0-1 x 5 days (new — added by ortho)
  6. Tab. ETOSHINE — continue (new — added by ortho)

  MEDICATION RECONCILIATION FLAGS:
  a. Inj. MEROPENEM: Was being given IV in hospital — oral antibiotic at discharge NOT documented
  b. Inj. LANTUS/H.ACTRAPID: Insulin management at home not documented
  c. Patient was on Ayurvedic medication for T2DM before admission — 
     no documentation of whether this should continue or stop
  d. Inj. HAPPYNERVE PLUS: Given only 2 days, stopped without documented reason
  e. Tab. ULTRACET and Tab. ETOSHINE: Added by Ortho — interaction check needed

--- FOLLOW-UP INSTRUCTIONS ---
  - Diet counselling done (low GI diet, fiber rich foods)
  - Ortho follow-up implied (hip pain, ? synovitis)
  - No specific follow-up date documented
  - Blood culture result pending at discharge (sent 27/02 due to fever spike)
  - Contrast CT KUB recommended but not done — pending
  - HbA1c needs repeat monitoring
  - Urology follow-up implied (CT findings of pyelonephritis)

--- CONDITION AT DISCHARGE ---
  - Patient symptomatically better
  - No fever spike on morning of 02/03 and 03/03
  - Hemodynamically stable by 02/03
  - Discharged on request (attenders not willing to stay)
  - BP at discharge: 170/80 mmHg (HIGH — hypertension at discharge)
  - HR at discharge: 110 b/m (still tachycardic)
  NOTE: Patient discharged with BP 170/80 and HR 110 — not fully normalized.
  This is a clinical concern and should be flagged for clinician review.

--- PENDING RESULTS AT DISCHARGE ---
  1. Blood Culture & Sensitivity (sent 27/02/2026) — RESULT PENDING
  2. Contrast CT KUB — RECOMMENDED but NOT DONE (only plain CT done)
  3. HbA1c monitoring (last known: 13.9% from outside report)
  4. Repeat blood glucose monitoring post-discharge
  5. Urology follow-up for bilateral pyelonephritis

--- BED SORES ASSESSMENT ---
  26/02/2026 (8PM-8AM): No bed sores
  27/02/2026 (8AM-2PM): No bed sores
  27/02/2026 (2PM-8PM): No pressure sores
  28/02/2026 (8AM-2PM): No bed sores

--- INTAKE/OUTPUT SUMMARY ---
  28/02/2026: Intake ~13350ml, Output ~1325ml (positive balance — fluid resuscitation)
  01/03/2026: Intake ~750ml, Output ~1250ml
  02/03/2026: Intake recorded (oral fluids H2O), Output ~200-250ml per entry

--- MONITORING CHART VITALS TREND ---
  28/02/2026:
    4PM:  Temp 102.2°F, HR 135, RR 26, SPO2 87%, BP 130/70
    7PM:  Temp 98.6°F, HR 130, RR 21, SPO2 86.7%, BP 130/80
    9PM:  Temp 98.0°F, HR 110, RR 20, SPO2 90%, BP 120/20
    11PM: Temp 102°F, HR 120, RR 21, SPO2 89.7%, BP 130/80
  01/03/2026:
    12AM: Temp 98.6°F, HR 110, RR 20, SPO2 89.7%, BP 120/80
    3AM:  Temp 98.0°F, HR 112, RR 21, SPO2 90%, BP 110/70
    7AM:  Temp 98.6°F, HR 110, RR 20, SPO2 89.7%, BP 120/80
    9AM:  Temp 97.2°F, HR 104, RR 24, SPO2 93%, BP 110/70
    12PM: Temp 97.4°F, HR 98, RR 24, SPO2 95.4%, BP 100/60
    2PM:  Temp 97.2°F, HR 101, RR 22, SPO2 96%, BP 110/70
    4PM:  Temp 98.2°F, HR 100, RR 20, SPO2 97%, BP 120/80
  02/03/2026:
    12PM: Temp 98.6°F, HR 116, RR 20, SPO2 94%, BP 120/80
    3AM:  Temp 103°F, HR 100, RR 21, SPO2 93.7%, BP 110/70
    7AM:  Temp 98.6°F, HR 110, RR 20, SPO2 92.5%, BP 120/80
    10AM: Temp 97.6°F, HR 100, RR 20, SPO2 94%, BP 110/80
    12PM: Temp 98.2°F, HR 105, RR 20, SPO2 96%, BP 120/60
    2PM:  Temp 97.2°F, HR 100, RR 20, SPO2 97%, BP 110/70

=== END OF PATIENT 2 EXTRACTED RECORDS ===
"""