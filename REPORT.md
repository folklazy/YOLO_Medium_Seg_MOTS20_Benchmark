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


## 6. Key Findings

- Observation: YOLO26m-Seg มี Mask mAP50-95 สูงสุด 0.574222; ห่างอันดับถัดไป 0.055915 บนสเกล 0–1
- Observation: YOLO26m-Seg นำ AP75 และ YOLO26m-Seg นำ Recall
- Observation: forward เร็วสุดคือ YOLOv8m-Seg, pipeline เร็วสุดและ FPS สูงสุดคือ YOLO11m-Seg, VRAM ต่ำสุดคือ YOLO11m-Seg
- คู่ที่ใกล้ที่สุดด้าน Mask mAP50-95: YOLO11m-Seg / YOLOv8m-Seg ต่าง 0.011336; ไม่ได้ทดสอบ statistical significance
- Interpretation: การเลือกต้องแยก accuracy, forward, pipeline และ memory ไม่สรุปว่า parameters ต่ำกว่าจะเร็วหรือใช้ VRAM ต่ำกว่าเสมอ

## 7. Per-sequence Observations

- YOLO26m-Seg: strongest MOTS20-11 (0.633370); weakest MOTS20-02 (0.449210) by Mask mAP50-95.
- YOLO11m-Seg: strongest MOTS20-05 (0.579142); weakest MOTS20-02 (0.399526) by Mask mAP50-95.
- YOLOv8m-Seg: strongest MOTS20-05 (0.565443); weakest MOTS20-02 (0.385912) by Mask mAP50-95.
- Ranking changes relative to pooled AP: none across the four sequences.

## 8. Efficiency and Resource Observations

- คู่ที่ใกล้ที่สุดด้าน inference mean: YOLO26m-Seg / YOLO11m-Seg ต่าง 1.469 ms; ไม่ได้ทดสอบ statistical significance
- คู่ที่ใกล้ที่สุดด้าน pipeline mean: YOLO26m-Seg / YOLO11m-Seg ต่าง 0.338 ms — near-tied descriptively; ไม่ได้ทดสอบ statistical significance

YOLO11m-Seg has the lowest peak allocated VRAM. Loaded/fused parameters, GFLOPs and separate load times are retained in MODEL_COMPLEXITY.csv. Peak reserved VRAM is preserved in [source timing summary](timing/benchmark-20261002T075505Z/clean_repetition/summary.csv). Separate RLE preparation means: yolo26m-seg.pt: 261.591 ms; yolo11m-seg.pt: 278.867 ms; yolov8m-seg.pt: 312.879 ms.

## 9. Warnings and Anomalies

CPU NNPACK unsupported-hardware warnings occurred during checkpoint complexity inspection; pycocotools emitted a NumPy copy-keyword DeprecationWarning. Evaluator regression passed. No package versions were changed to suppress warnings. Primary timing contains only nine clean runs. Pipeline excludes RLE preparation and disk I/O; it is not end-to-end mask-saving/CCTV throughput.

## 10. Limitations

ผลนี้เป็น Person instance segmentation รายเฟรมบน MOTS20 ไม่ใช่ MOTS tracking; 26,894 GT instances เป็น annotation รายเฟรม ไม่ใช่จำนวนคนไม่ซ้ำ TP-only IoU/Dice พิจารณาเฉพาะคู่ที่ match ได้ ภาพต่อเนื่องสัมพันธ์กันและไม่มีการทดสอบ statistical significance ผลยังไม่ยืนยัน blur, low-light, มุมกล้อง, ระดับ occlusion หรือ deployment suitability จึงใช้เพื่อเลือก candidate for later CCTV robustness evaluation เท่านั้น

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
