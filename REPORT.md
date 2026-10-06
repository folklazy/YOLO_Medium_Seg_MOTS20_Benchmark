# Medium (M) การทดสอบ YOLO Instance Segmentation — MOTS20

## 1. สถานะการทดลอง

PASS WITH WARNINGS

- โมเดลที่เสร็จแล้ว: 3/3
- จำนวนเฟรม: 2,862 ต่อโมเดล; Person GT รายเฟรม: 26,894 instances
- รหัสรอบทดลอง: `benchmark-20261002T075505Z`

## 2. โมเดลที่ทดสอบ

| ตระกูล | โมเดล | จำนวนพารามิเตอร์ | GFLOPs | Checkpoint (MB) |
| --- | --- | --- | --- | --- |
| YOLO26 | YOLO26m-Seg | 27,112,072 | 132.781 | 54.75 |
| YOLO11 | YOLO11m-Seg | 22,420,896 | 113.968 | 45.40 |
| YOLOv8 | YOLOv8m-Seg | 27,285,968 | 104.977 | 54.92 |

## 3. ความสอดคล้องกับโพรโทคอล

| รายการ | สถานะ |
|---|---|
| ข้อมูล | PASS |
| ตัวประเมิน | PASS |
| การเตรียมภาพ | PASS |
| ขนาดภาพเข้าโมเดล | PASS |
| ความละเอียดเชิงตัวเลข | PASS |
| ค่าเกณฑ์ | PASS |
| maxDet | PASS |
| วิธีวัดเวลา | PASS |
| สภาพแวดล้อม | PASS |

ความสอดคล้องของข้อมูล: PASS

ความสอดคล้องของการเตรียมภาพ: PASS

[วิธีทดลองร่วม](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study/blob/main/METHODOLOGY_REFERENCE.md) · [โพรโทคอลการทดลอง](EXPERIMENT_PROTOCOL.md) · [หลักฐานการกำหนดมาตรฐาน](manifests/STANDARDIZATION.json)

## 4. ผลลัพธ์รวม

| โมเดล | Mask mAP50-95 | AP50 | AP75 | Precision | Recall | F1 | TP-only IoU | TP-only Dice | Inference (ms) | Pipeline (ms) | FPS | Peak allocated VRAM (MiB) | จำนวนพารามิเตอร์ | GFLOPs | Checkpoint (MB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26m-Seg | 0.574222 | 0.873522 | 0.629038 | 0.918331 | 0.815312 | 0.863761 | 0.825309 | 0.900655 | 32.043 | 77.309 | 12.935 | 912.16 | 27,112,072 | 132.781 | 54.75 |
| YOLO11m-Seg | 0.518307 | 0.855237 | 0.557205 | 0.914354 | 0.805049 | 0.856228 | 0.799402 | 0.884647 | 30.574 | 76.971 | 12.992 | 889.38 | 22,420,896 | 113.968 | 45.40 |
| YOLOv8m-Seg | 0.506971 | 0.843732 | 0.542131 | 0.895403 | 0.793857 | 0.841578 | 0.797128 | 0.883076 | 27.232 | 78.112 | 12.802 | 1018.76 | 27,285,968 | 104.977 | 54.92 |

## 5. ผู้ชนะในแต่ละด้าน

| ด้าน | โมเดล | ผลลัพธ์ |
| --- | --- | --- |
| Mask mAP50-95 สูงสุด | YOLO26m-Seg | 0.574222 |
| AP75 สูงสุด | YOLO26m-Seg | 0.629038 |
| Recall สูงสุด | YOLO26m-Seg | 0.815312 |
| Inference เร็วสุด | YOLOv8m-Seg | 27.232 |
| Pipeline เร็วสุด | YOLO11m-Seg | 76.971 |
| FPS สูงสุด | YOLO11m-Seg | 12.992 |
| VRAM ต่ำสุด | YOLO11m-Seg | 889.38 |

## 6. ข้อค้นพบสำคัญ

- ข้อสังเกต: YOLO26m-Seg มี Mask mAP50-95 สูงสุด 0.574222; ห่างอันดับถัดไป 0.055915 บนสเกล 0–1
- ข้อสังเกต: YOLO26m-Seg นำ AP75; YOLO26m-Seg นำ Recall
- ข้อสังเกต: YOLOv8m-Seg มี inference เร็วสุด; YOLO11m-Seg มี pipeline เร็วสุดและ FPS สูงสุด; YOLO11m-Seg มี VRAM ต่ำสุด
- คู่ mAP ใกล้ที่สุด: YOLO11m-Seg / YOLOv8m-Seg ต่าง 0.011336; เป็นความใกล้เชิงพรรณนา ไม่ใช่ผลทดสอบนัยสำคัญทางสถิติ
- การตีความ: แยกความแม่นยำความครบถ้วนเวลา forward เวลา pipeline และหน่วยความจำไม่มีคะแนนรวมถ่วงน้ำหนักจำนวนพารามิเตอร์หรือ GFLOPs ไม่กำหนดอันดับเวลา/VRAM โดยตรง

## 7. ข้อสังเกตรายลำดับภาพ

- YOLO26m-Seg: Mask mAP50-95 สูงสุดที่ MOTS20-11 (0.633370); ต่ำสุดที่ MOTS20-02 (0.449210)
- YOLO11m-Seg: Mask mAP50-95 สูงสุดที่ MOTS20-05 (0.579142); ต่ำสุดที่ MOTS20-02 (0.399526)
- YOLOv8m-Seg: Mask mAP50-95 สูงสุดที่ MOTS20-05 (0.565443); ต่ำสุดที่ MOTS20-02 (0.385912)
- ลำดับ mAP ที่ต่างจากผลรวม: ไม่มีในทั้งสี่ลำดับภาพ

AP รวมคำนวณจากข้อมูลทั้งหมด ไม่ใช่ค่าเฉลี่ย AP รายลำดับภาพ ดูค่าครบใน [PER_SEQUENCE_RESULTS.csv](metrics/PER_SEQUENCE_RESULTS.csv)

## 8. ประสิทธิภาพและการใช้ทรัพยากร

- คู่ที่ใกล้ที่สุดด้านค่าเฉลี่ย inference: YOLO26m-Seg / YOLO11m-Seg ต่าง 1.469 ms; ไม่ได้ทดสอบนัยสำคัญทางสถิติ
- คู่ที่ใกล้ที่สุดด้านค่าเฉลี่ย pipeline: YOLO26m-Seg / YOLO11m-Seg ต่าง 0.338 ms; ไม่ได้ทดสอบนัยสำคัญทางสถิติ

YOLO11m-Seg ใช้ peak allocated VRAM ต่ำสุดจำนวนพารามิเตอร์ก่อน/หลัง fusion, GFLOPs และเวลาโหลดแยกเก็บใน [MODEL_COMPLEXITY.csv](metrics/MODEL_COMPLEXITY.csv) ส่วน peak reserved VRAM อยู่ใน [แหล่งวัดเวลา](timing/benchmark-20261002T075505Z/clean_repetition/summary.csv) เวลาเตรียม RLE แยก: yolo26m-seg.pt: 261.591 ms; yolo11m-seg.pt: 278.867 ms; yolov8m-seg.pt: 312.879 ms.

ใช้ 3 รอบที่ไม่ถูกรบกวนต่อโมเดล รอบละ 100 เฟรมหลัง 10 warmups และ synchronize CUDA ตามขอบเขต stage ค่า pipeline รวม preprocessing, inference และ postprocessing ไม่รวมการเตรียม RLE และการอ่านเขียนดิสก์ FPS จึงไม่ใช่อัตราการบันทึก mask ครบกระบวนการและไม่บวก Ultralytics-inclusive diagnostic ซ้ำ

ค่าเฉลี่ย postprocessing: YOLO26m-Seg: 43.560 ms; YOLO11m-Seg: 44.664 ms; YOLOv8m-Seg: 49.148 ms

## 9. คำเตือนและข้อสังเกตผิดปกติ

พบคำเตือน CPU NNPACK ระหว่างตรวจความซับซ้อน checkpoint และ NumPy copy-keyword DeprecationWarning จาก pycocotools การตรวจ regression ของตัวประเมินผ่าน ไม่เปลี่ยน package เพื่อซ่อนคำเตือน ผลเวลาหลักมี 9 รอบที่ไม่ถูกรบกวน

Pipeline ไม่รวมการเตรียม RLE และการอ่านเขียนดิสก์จึงไม่ใช่เวลา/อัตราประมวลผลครบกระบวนการสำหรับการบันทึก mask หรือระบบ CCTV การปรับเอกสารครั้งนี้ไม่รัน inference ใหม่และไม่เปลี่ยนค่าที่วัด

## 10. ข้อจำกัด

ผลนี้เป็น Person instance segmentation รายเฟรมบน MOTS20 ไม่ใช่ MOTS tracking; 26,894 GT instances เป็น annotation รายเฟรมไม่ใช่จำนวนคนไม่ซ้ำ TP-only IoU/Dice พิจารณาเฉพาะคู่ที่ จับคู่ ได้ ภาพต่อเนื่องสัมพันธ์กันและไม่มีการทดสอบนัยสำคัญทางสถิติผลยังไม่ยืนยันภาพพร่า, แสงน้อย, มุมกล้อง, ระดับ occlusion หรือความเหมาะสมต่อการนำไปใช้งานจึงใช้เพื่อเลือกตัวเลือกสำหรับการทดสอบต่อการประเมินความทนทานต่อ CCTV เท่านั้น

## 11. หลักฐานสำหรับตรวจสอบซ้ำ

- [TIER_RESULTS.csv](metrics/TIER_RESULTS.csv)
- [PER_SEQUENCE_RESULTS.csv](metrics/PER_SEQUENCE_RESULTS.csv)
- [TIMING_SUMMARY.csv](metrics/TIMING_SUMMARY.csv)
- [MODEL_COMPLEXITY.csv](metrics/MODEL_COMPLEXITY.csv)
- [PREFLIGHT_MAXDET.csv](metrics/PREFLIGHT_MAXDET.csv)

[แหล่งที่มาและค่า hash](manifests/STANDARDIZATION.json) · [โพรโทคอล](EXPERIMENT_PROTOCOL.md) · [รายการกราฟ](outputs/plots/INDEX.md) · [บันทึกย้อนหลัง](reports/archive/)

prediction แบบ RLE ที่ไม่สูญเสียข้อมูลและบันทึกการวัดเวลาละเอียดเก็บในเครื่องตามรหัสรอบทดลอง หลักฐานต้นทางคงเดิม; การปรับภาษานี้ไม่คำนวณค่าตัวชี้วัดใหม่และไม่รัน inference

## 12. ความเชื่อมโยงกับการศึกษาทุกขนาด

[การศึกษาหลัก](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study) — รายงานนี้กล่าวถึงขนาด Medium (M) เท่านั้นผลรวม 17 โมเดลยังรอคำสั่งจากผู้ใช้ แม้การทดลองทั้งห้าขนาดเสร็จแล้ว การปรับเอกสารไม่เริ่ม benchmark หรือการสังเคราะห์ผลใหม่

## การวิเคราะห์เชิงคุณภาพ

ภาพเปรียบเทียบเฟรมเดียวกัน 4 กรณีจาก prediction ที่บันทึกไว้ พร้อมข้อผิดพลาดที่พบและการตีความ อยู่ใน [PRESENTATION_SUMMARY_TH.md](PRESENTATION_SUMMARY_TH.md) ดู [เหตุผลเลือกกรณีปัจจุบัน](outputs/visualizations/qualitative/selection_v2/CASE_SELECTION.md) และ [ตัวชี้ชุดหลักฐาน](manifests/QUALITATIVE_SELECTION.json) รายงานเทคนิคนี้เชื่อมไปยังการวิเคราะห์ภาพเพื่อไม่เล่าเนื้อหาซ้ำ
