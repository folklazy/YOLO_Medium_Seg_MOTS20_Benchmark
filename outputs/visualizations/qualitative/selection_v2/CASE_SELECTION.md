# Medium — qualitative case selection v2

Selected from 12 frozen visualization frames using per-frame metrics, original/GT images and saved RLE masks at confidence ≥0.25 and mask matching IoU ≥0.50, with the original evaluator and ignore policy. No inference was run.

One shared anchor plus three cases selected for tier-specific behavior. Tiers need not share every frame; within each case, all models use the same full frame. ROI views supplement the full comparison and do not hide errors elsewhere.

| Case | Sequence / frame | Why selected / decision use | Source comparison |
|---|---|---|---|
| 1 | MOTS20-05 / 000419 | Tier diagnostic: small GT and an extra output. YOLO26m matches GT 2002, whereas YOLO11m and YOLOv8m fail matching; YOLO11m also has an FP at the right edge. | reuse existing image |
| 2 | MOTS20-09 / 000263 | Shared anchor: common failure. Examine errors among overlapping people; YOLOv8m produces a mask for GT 2018, but its IoU is slightly below the matching threshold, so the instance is an FN. | reuse existing image |
| 3 | MOTS20-02 / 000001 | Counterexample: more TP with extra outputs. YOLOv8m has more TP than the accuracy leader in this frame; YOLO11m has no FP but more FN. | reuse existing image |
| 4 | MOTS20-11 / 000450 | Coverage control with errors: equal valid GT coverage, different FP. All models have TP 9 / FN 0, while YOLO26m/YOLO11m/YOLOv8m have FP 1/0/2 in this frame. | new composite from saved predictions |

## Why some frames are shared across tiers

Case 2 (09/263) compares FN/FP against the same GT. Other frames may repeat when the same error region helps compare different models: 05/419 examines GT 2002 in Second-largest/Medium; 02/1 examines equal counts and different GT sets in Second-largest/Medium; 02/600 provides a counterexample in Largest/Small; 02/300 examines TP–FP trade-offs in Small/Nano; 11/1 examines GT 2016 in Second-largest and GT 2028 with extra masks in Nano; 11/450 compares equal coverage with extra outputs in Largest/Medium. Reused frames are not additional independent evidence.

## Replacement of previous cases

Previous Case 4 (09/1) had TP 6 / FP 0 / FN 0 for every model. Its replacement (11/450) retains equal coverage while showing different FP. Previous images and evidence remain unchanged for audit; the previous presentation is retained under reports/archive.

## Scope

Across five tiers, 20 case slots use 10 distinct original frames (previously 6). The selection includes MOTS20-11, common failures and counterexamples, rather than only frames where the accuracy leader wins. The 12-frame pool does not represent the dataset, and these are not claimed to be the most divergent frames among all 2,862. Images do not measure latency, VRAM or statistical significance.

[Candidate pool](CANDIDATE_POOL.json) · [Case evidence](CASE_EVIDENCE.json) · [Focus evidence](FOCUS_EVIDENCE.json) · [Decision audit](CASE_DECISION_AUDIT.json) · [Active selection](../../../../manifests/QUALITATIVE_SELECTION.json)
