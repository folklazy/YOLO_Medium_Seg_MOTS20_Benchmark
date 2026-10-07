# Medium (M) YOLO Segmentation Benchmark — MOTS20

## 1. Experiment Status

PASS WITH WARNINGS

- Models completed: 3/3
- Frames: 2,862 per model; Person GT instances: 26,894
- Run ID: `benchmark-20261002T075505Z`

## 2. Models Tested

| Family | Model | Parameters | GFLOPs | Checkpoint MB |
| --- | --- | --- | --- | --- |
| YOLO26 | YOLO26m-Seg | 27,112,072 | 132.781 | 54.75 |
| YOLO11 | YOLO11m-Seg | 22,420,896 | 113.968 | 45.40 |
| YOLOv8 | YOLOv8m-Seg | 27,285,968 | 104.977 | 54.92 |


## 3. Protocol Compatibility

| Item | Status |
|---|---|
| Dataset | PASS |
| Evaluator | PASS |
| Preprocessing | PASS |
| Input size | PASS |
| Precision | PASS |
| Thresholds | PASS |
| maxDet | PASS |
| Timing protocol | PASS |
| Environment | PASS |

Dataset compatibility: PASS

Preprocessing compatibility: PASS

[Common methodology](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study/blob/main/METHODOLOGY_REFERENCE.md) · [Frozen protocol](EXPERIMENT_PROTOCOL.md)

## 4. Overall Results

| Model | Mask mAP50-95 | AP50 | AP75 | Precision | Recall | F1 | TP-only IoU | TP-only Dice | Inference ms | Pipeline ms | FPS | Peak VRAM MiB | Params | GFLOPs | Checkpoint MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26m-Seg | 0.574222 | 0.873522 | 0.629038 | 0.918331 | 0.815312 | 0.863761 | 0.825309 | 0.900655 | 32.043 | 77.309 | 12.935 | 912.16 | 27,112,072 | 132.781 | 54.75 |
| YOLO11m-Seg | 0.518307 | 0.855237 | 0.557205 | 0.914354 | 0.805049 | 0.856228 | 0.799402 | 0.884647 | 30.574 | 76.971 | 12.992 | 889.38 | 22,420,896 | 113.968 | 45.40 |
| YOLOv8m-Seg | 0.506971 | 0.843732 | 0.542131 | 0.895403 | 0.793857 | 0.841578 | 0.797128 | 0.883076 | 27.232 | 78.112 | 12.802 | 1018.76 | 27,285,968 | 104.977 | 54.92 |


## 5. Tier Winners

| Category | Model | Value |
|---|---|---|
| Highest Mask mAP50-95 | YOLO26m-Seg | 0.574222 |
| Highest AP75 | YOLO26m-Seg | 0.629038 |
| Highest Recall | YOLO26m-Seg | 0.815312 |
| Fastest inference | YOLOv8m-Seg | 27.232 |
| Fastest pipeline | YOLO11m-Seg | 76.971 |
| Highest FPS | YOLO11m-Seg | 12.992 |
| Lowest VRAM | YOLO11m-Seg | 889.38 |

Inference and pipeline latency are in ms/frame; FPS is derived from mean pipeline latency; VRAM is peak allocated MiB.

## 6. Key Findings

- Observation: YOLO26m-Seg has the highest Mask mAP50-95, 0.574222; the gap to the runner-up is 0.055915 on the 0–1 scale.
- Observation: YOLO26m-Seg leads both AP75 and Recall.
- Observation: the fastest forward pass is from YOLOv8m-Seg; the fastest pipeline and highest FPS are from YOLO11m-Seg; the lowest VRAM is from YOLO11m-Seg.
- Closest pair in Mask mAP50-95: YOLO11m-Seg / YOLOv8m-Seg differ by 0.011336; statistical significance was not tested.
- Interpretation: selection must distinguish accuracy, forward latency, pipeline latency and memory; fewer parameters do not necessarily mean lower latency or VRAM.

## 7. Per-sequence Observations

- YOLO26m-Seg: strongest MOTS20-11 (0.633370); weakest MOTS20-02 (0.449210) by Mask mAP50-95.
- YOLO11m-Seg: strongest MOTS20-05 (0.579142); weakest MOTS20-02 (0.399526) by Mask mAP50-95.
- YOLOv8m-Seg: strongest MOTS20-05 (0.565443); weakest MOTS20-02 (0.385912) by Mask mAP50-95.
- Ranking changes relative to pooled AP: none across the four sequences.

## 8. Efficiency and Resource Observations

- Closest pair in mean inference latency: YOLO26m-Seg / YOLO11m-Seg differ by 1.469 ms; statistical significance was not tested.
- Closest pair in mean pipeline latency: YOLO26m-Seg / YOLO11m-Seg differ by 0.338 ms — near-tied descriptively; statistical significance was not tested.

YOLO11m-Seg has the lowest peak allocated VRAM. Loaded/fused parameters, GFLOPs and separate load times are retained in MODEL_COMPLEXITY.csv. Peak reserved VRAM is preserved in [source timing summary](timing/benchmark-20261002T075505Z/clean_repetition/summary.csv). Separate RLE preparation means: yolo26m-seg.pt: 261.591 ms; yolo11m-seg.pt: 278.867 ms; yolov8m-seg.pt: 312.879 ms.

## 9. Warnings and Anomalies

CPU NNPACK unsupported-hardware warnings occurred during checkpoint complexity inspection; pycocotools emitted a NumPy copy-keyword DeprecationWarning. Evaluator regression passed. No package versions were changed to suppress warnings. Primary timing contains only nine clean runs. Pipeline excludes RLE preparation and disk I/O; it is not end-to-end mask-saving/CCTV throughput.

## 10. Limitations

This evaluates frame-level Person instance segmentation on MOTS20, rather than MOTS tracking. The 26,894 GT instances are frame-level annotations, not unique people. TP-only IoU/Dice are conditional on successful matching.

Consecutive video frames are correlated, and no statistical significance test was performed; small differences are descriptive. Selected qualitative cases do not replace dataset-level metrics.

These measurements do not establish robustness to blur, low light, camera angle or occlusion severity, or deployment suitability. They support candidate selection for later CCTV robustness evaluation only. No weighted score or architectural causal conclusion is used.

## 11. Reproducibility and Source Artifacts

- [TIER_RESULTS.csv](metrics/TIER_RESULTS.csv)
- [PER_SEQUENCE_RESULTS.csv](metrics/PER_SEQUENCE_RESULTS.csv)
- [TIMING_SUMMARY.csv](metrics/TIMING_SUMMARY.csv)
- [MODEL_COMPLEXITY.csv](metrics/MODEL_COMPLEXITY.csv)
- [PREFLIGHT_MAXDET.csv](metrics/PREFLIGHT_MAXDET.csv)

[Standardization provenance](manifests/STANDARDIZATION.json) · [Final integrity](manifests/final_integrity.json) · [Timing source](timing/benchmark-20261002T075505Z/clean_repetition/summary.csv) · [Plots](outputs/plots/INDEX.md)

Lossless per-frame RLE predictions and full telemetry remain local under predictions/benchmark-20261002T075505Z/ and timing/benchmark-20261002T075505Z/. Published manifests record hashes; no inference rerun is required to regenerate metrics.

## 12. Relation to Full Scaling Study

[Master Study](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study) — Medium only. Small, Nano and final Master synthesis were not run.

## Qualitative Analysis

Four same-frame diagnostic comparisons from saved lossless predictions are discussed in [PRESENTATION_SUMMARY_TH.md](PRESENTATION_SUMMARY_TH.md). See [current case selection](outputs/visualizations/qualitative/selection_v2/CASE_SELECTION.md) and [active selection](manifests/QUALITATIVE_SELECTION.json) for selection reasons, shared and tier-specific behaviors, and evidence limits. Comparisons use original MOTS20 frames. No inference or measured values were changed for this documentation update.
