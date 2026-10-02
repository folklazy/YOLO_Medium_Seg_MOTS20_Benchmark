# สรุปผล Medium (M) YOLO Instance Segmentation

## สรุปใน 1 นาที

- โมเดล: YOLO26m-Seg, YOLO11m-Seg, YOLOv8m-Seg
- MOTS20 2,862 frames / 26,894 Person GT instances (annotation รายเฟรม)
- Official pretrained checkpoints / no fine-tuning; สถานะเดิม PASS WITH WARNINGS
- Accuracy สูงสุด: YOLO26m-Seg — Mask mAP50-95 0.574222
- เร็วสุด: inference YOLOv8m-Seg (27.232 ms); pipeline YOLO11m-Seg (76.971 ms)
- Peak allocated VRAM ต่ำสุด: YOLO11m-Seg — 889.38 MiB
- Trade-off หลัก: YOLO26m-Seg นำรองอันดับสอง 5.591500 percentage points ของ mAP; เวลา inference มากกว่าตัวเร็วสุด 4.811 ms

## ผลลัพธ์หลัก

| Model | Mask mAP50-95 | AP75 | Recall | Inference ms | Pipeline ms | FPS | Peak VRAM MiB |
|---|---|---|---|---|---|---|---|
| YOLO26m-Seg | 0.574222 | 0.629038 | 0.815312 | 32.043 | 77.309 | 12.935 | 912.16 |
| YOLO11m-Seg | 0.518307 | 0.557205 | 0.805049 | 30.574 | 76.971 | 12.992 | 889.38 |
| YOLOv8m-Seg | 0.506971 | 0.542131 | 0.793857 | 27.232 | 78.112 | 12.802 | 1018.76 |

## Winner ของแต่ละด้าน

| ด้าน | Model | Result |
|---|---|---|
| Mask mAP50-95 | YOLO26m-Seg | 0.574222 |
| AP75 | YOLO26m-Seg | 0.629038 |
| Recall | YOLO26m-Seg | 0.815312 |
| Inference speed | YOLOv8m-Seg | 27.232 ms |
| Pipeline speed | YOLO11m-Seg | 76.971 ms |
| VRAM | YOLO11m-Seg | 889.38 MiB |

## สิ่งที่ตัวเลขบอกเรา

- mAP ของ YOLO26m-Seg สูงกว่า YOLO11m-Seg 5.591500 percentage points
- Pipeline ของ YOLO11m กับ YOLO26m ต่างเพียง 0.338 ms (ประมาณ 0.44%); ไม่ใช่ accuracy near tie
- YOLOv8m inference เร็วสุด แต่ pipeline ช้าที่สุดและ VRAM สูงสุดใน tier
- Accuracy winner ใช้ VRAM มากกว่าตัวต่ำสุด 22.78 MiB; การจัดอันดับ inference และ pipeline ต้องแยกกัน

## Trade-off หลัก

### Accuracy vs Speed

YOLO26m-Seg มี mAP 0.574222; YOLOv8m-Seg มี mAP 0.506971
และ inference 27.232 ms เทียบกับ 32.043 ms ของ accuracy winner
Pipeline winner คือ YOLO11m-Seg (76.971 ms); ไม่ใช้เวลา forward แทน throughput ของ pipeline

### Accuracy vs Memory

YOLO26m-Seg ใช้ 912.16 MiB; YOLO11m-Seg ใช้ 889.38 MiB
และมี mAP 0.518307

## ข้อควรระวังในการตีความ

ไม่มีการทดสอบ statistical significance; near tie เป็นคำบรรยาย ค่า AP/Recall อยู่ช่วง 0–1
Pipeline ไม่รวม RLE preparation และ disk I/O; VRAM เป็น peak allocated
MOTS20 ไม่ใช่ผลทดสอบ CCTV robustness ขั้นสุดท้าย

## ข้อมูลสำหรับนำไปรวมต่อ

นำ YOLO26m สำหรับ accuracy, YOLOv8m สำหรับ inference และ YOLO11m สำหรับ pipeline/VRAM ไปเทียบข้าม tier โดยคง protocol และแหล่ง canonical เดิม ยังไม่สรุปครบ 17 โมเดล

[TIER_RESULTS.csv](metrics/TIER_RESULTS.csv) · [REPORT.md](REPORT.md) ·
[Visual analysis](PRESENTATION_SUMMARY_TH.md) ·
[Master Study](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study)
