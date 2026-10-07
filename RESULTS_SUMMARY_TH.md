# สรุปผล Medium YOLO Instance Segmentation

## สรุปใน 1 นาที

- โมเดล: YOLO26m-Seg, YOLO11m-Seg, YOLOv8m-Seg
- MOTS20 2,862 frames / 26,894 Person GT instances รายเฟรม
- Official pretrained checkpoints; ไม่มี training หรือ fine-tuning; สถานะ PASS WITH WARNINGS
- Accuracy สูงสุด: YOLO26m-Seg — Mask mAP50-95 0.574222
- Inference เร็วสุด: YOLOv8m-Seg — 27.232 ms
- Pipeline เร็วสุด: YOLO11m-Seg — 76.971 ms / 12.992 FPS
- Peak allocated VRAM ต่ำสุด: YOLO11m-Seg — 889.38 MiB
- Trade-off หลัก: ตัวนำ mAP สูงกว่ารองอันดับสอง 5.592 percentage points; ต้องแยก forward จาก pipeline

## ผลลัพธ์หลัก

| Model | Mask mAP50-95 | AP75 | Recall | Inference ms | Pipeline ms | FPS | Peak VRAM MiB |
|---|---|---|---|---|---|---|---|
| YOLO26m-Seg | 0.574222 | 0.629038 | 0.815312 | 32.043 | 77.309 | 12.935 | 912.16 |
| YOLO11m-Seg | 0.518307 | 0.557205 | 0.805049 | 30.574 | 76.971 | 12.992 | 889.38 |
| YOLOv8m-Seg | 0.506971 | 0.542131 | 0.793857 | 27.232 | 78.112 | 12.802 | 1018.76 |

AP/Recall เป็น fraction ช่วง 0–1; latency เป็น ms/frame และ FPS มาจาก mean pipeline

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

- YOLO26m-Seg นำ YOLO11m-Seg ด้าน mAP 5.592 percentage points
- YOLOv8m forward เร็วสุด แต่ pipeline ช้าสุด; อันดับ forward จึงกลับทิศเมื่อดูงานทั้ง pipeline
- YOLO11m pipeline ต่ำสุดตาม mean แต่ใกล้ YOLO26m; ไม่อ้างความเหนือกว่าที่แน่นอนจากช่องว่างเล็ก
- ไม่มีคู่ผ่าน descriptive mAP near-tie screen ≤0.001; ความใกล้ของ latency เป็นคนละประเด็น; near tie ไม่ใช่ equivalence หรือ statistical significance

## บทบาทของแต่ละโมเดล

| Model | จุดเด่น | สิ่งที่แลก | เหมาะพิจารณาเมื่อ |
|---|---|---|---|
| YOLO26m-Seg | นำ mAP/AP75/Recall และ TP-only quality | Forward ช้าสุด; VRAM สูงกว่า YOLO11m | Accuracy สำคัญกว่า forward latency |
| YOLO11m-Seg | Pipeline และ VRAM ต่ำสุดใน tier | mAP ต่ำกว่า YOLO26m; forward ช้ากว่า YOLOv8m | เปรียบเทียบ pipeline ที่ใกล้กันเชิงพรรณนา |
| YOLOv8m-Seg | Inference เร็วสุด | mAP ต่ำสุด; pipeline/VRAM สูงสุด | Forward latency เป็นข้อจำกัดหลัก |

## Trade-off หลัก

### Accuracy vs Speed

YOLO26m-Seg มี mAP 0.574222; ตัว forward เร็วสุด YOLOv8m-Seg มี mAP 0.506971 และ inference ต่ำกว่า 4.811 ms ส่วน pipeline ต้องดู YOLO11m-Seg แยก ไม่ถือว่า forward winner เป็น throughput winner

### Accuracy vs Memory

YOLO26m-Seg ใช้ VRAM มากกว่า YOLO11m-Seg 22.78 MiB เพื่อ mAP สูงกว่า 5.592 percentage points ไม่ใช้ชื่อขนาดหรือ parameters แทน memory measurement

## ข้อควรระวังในการตีความ

ไม่มี significance test; ภาพวิดีโอสัมพันธ์กัน TP-only quality วัดเฉพาะคู่ที่ match และ Recall เป็น mask matching ไม่ใช่ box Recall Pipeline ไม่รวม decode, RLE preparation และการเขียนผล; VRAM เป็น peak allocated ภายใต้ benchmark นี้ การแบ่ง tier ไม่ทำให้ capacity/pretraining เท่ากัน และยังไม่ยืนยัน CCTV robustness ไม่มี weighted score หรือผู้ชนะทุกข้อจำกัด

## รายละเอียดเพิ่มเติม

[REPORT.md](REPORT.md) · [รายงานวิจัยภาพเชิงคุณภาพ](PRESENTATION_SUMMARY_TH.md) · [TIER_RESULTS.csv](metrics/TIER_RESULTS.csv) · [Master Study](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study)
