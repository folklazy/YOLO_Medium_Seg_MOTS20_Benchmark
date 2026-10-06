# สรุปผล Medium (M) YOLO Instance Segmentation

## สรุปใน 1 นาที

- โมเดล: YOLO26m-Seg, YOLO11m-Seg, YOLOv8m-Seg
- MOTS20 2,862 เฟรม / 26,894 Person GT รายเฟรม (annotation รายเฟรม)
- Official pretrained checkpoints / ไม่ปรับจูน; สถานะเดิม PASS WITH WARNINGS
- ความแม่นยำสูงสุด: YOLO26m-Seg — Mask mAP50-95 0.574222
- เร็วสุด: inference YOLOv8m-Seg (27.232 ms); pipeline YOLO11m-Seg (76.971 ms)
- Peak allocated VRAM ต่ำสุด: YOLO11m-Seg — 889.38 MiB
- Trade-off หลัก: YOLO26m-Seg นำรองอันดับสอง 5.591500 percentage points ของ mAP; เวลา inference มากกว่าตัวเร็วสุด 4.811 ms

## ผลลัพธ์หลัก

| โมเดล | Mask mAP50-95 | AP75 | Recall | Inference (ms) | Pipeline (ms) | FPS | Peak allocated VRAM (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26m-Seg | 0.574222 | 0.629038 | 0.815312 | 32.043 | 77.309 | 12.935 | 912.16 |
| YOLO11m-Seg | 0.518307 | 0.557205 | 0.805049 | 30.574 | 76.971 | 12.992 | 889.38 |
| YOLOv8m-Seg | 0.506971 | 0.542131 | 0.793857 | 27.232 | 78.112 | 12.802 | 1018.76 |

## สรุปผลจากตาราง

อ่านร่วมกับตารางหลักด้านบน; AP50 และ TP-only IoU/Dice อ้างอิง [CSV มาตรฐาน](metrics/TIER_RESULTS.csv) และ [REPORT.md](REPORT.md) ตัวเลข TP-only วัดเฉพาะคู่ที่ จับคู่ ได้ จึงไม่แทนความครอบคลุม GT หรือคุณภาพทุก instance

### YOLO26m-Seg

นำทั้ง AP50, AP75, mAP50-95, Recall และ TP-only IoU/Dice; Recall 81.53% สนับสนุนความครอบคลุม GT ที่สูงกว่า แต่ยังมีคนพลาดหรือจับคู่ไม่ผ่านและคุณภาพของ mask เฉลี่ยนี้พิจารณาเฉพาะ TP ซึ่งอาจเป็นคนละชุด GT ระหว่างโมเดล

สิ่งที่แลกคือ inference 32.043 ms ช้าที่สุดและ VRAM 912.16 MiB สูงกว่า YOLO11m แต่ต่ำกว่า YOLOv8m ส่วน pipeline 77.309 ms ใกล้ YOLO11m (76.971 ms) หากรับทรัพยากรเพิ่มได้ รุ่นนี้เป็นตัวเลือกด้าน accuracy โดยไม่อ้างว่า pipeline ต่างกันอย่างมีนัยสำคัญ

### YOLO11m-Seg

mAP/AP75/Recall และ TP-only quality อยู่ระหว่าง YOLO26m กับ YOLOv8m แต่มี pipeline 76.971 ms เร็วสุดและ VRAM 889.38 MiB ต่ำสุด จึงเป็นตัวเลือกที่มีเหตุผลเมื่อ pipeline/หน่วยความจำเป็นข้อจำกัด มากกว่าตัดสินจากขนาดหรือชื่อรุ่น

เมื่อเลือกแทน YOLO26m จะได้ inference เร็วกว่าและ VRAM ต่ำกว่า แต่ลด mAP/AP75/Recall ตามค่าที่วัด ความต่าง pipeline เล็กจึงไม่เพียงพอจะเรียกว่า “สมดุลดีที่สุด”; ต้องตัดสินว่ายอมลด accuracy เพื่อประหยัดทรัพยากรได้หรือไม่

### YOLOv8m-Seg

มี inference 27.232 ms เร็วสุด แต่ pipeline 78.112 ms ช้าที่สุดและ VRAM 1018.76 MiB สูงสุด อีกทั้ง mAP/AP75/Recall และ TP-only quality ต่ำสุด จึงเป็นตัวอย่างว่าการลดเวลา forward ไม่ได้ทำให้ pipeline ทั้งชุดเร็วขึ้นตามกัน

ควรเก็บเป็นตัวเลือกเฉพาะเมื่อ forward เวลาแฝงเป็นข้อจำกัดสำคัญ หรือใช้เป็น baseline; ถ้าเน้น pipeline/VRAM รุ่น YOLO11m มีค่าที่วัดดีกว่าพร้อม accuracy สูงกว่า ข้อสรุปนี้จำกัดเฉพาะ checkpoint และ protocol รอบนี้ ไม่ใช่การพิสูจน์โครงสร้างโมเดลหรือความพร้อมใช้งาน CCTV

## ผู้ชนะในแต่ละด้าน

| ด้าน | โมเดล | ผลลัพธ์ |
| --- | --- | --- |
| Mask mAP50-95 | YOLO26m-Seg | 0.574222 |
| AP75 | YOLO26m-Seg | 0.629038 |
| Recall | YOLO26m-Seg | 0.815312 |
| Inference เร็วสุด | YOLOv8m-Seg | 27.232 ms |
| Pipeline เร็วสุด | YOLO11m-Seg | 76.971 ms |
| VRAM | YOLO11m-Seg | 889.38 MiB |

## สิ่งที่ตัวเลขบอกเรา

- mAP ของ YOLO26m-Seg สูงกว่า YOLO11m-Seg 5.591500 percentage points
- Pipeline ของ YOLO11m กับ YOLO26m ต่างเพียง 0.338 ms (ประมาณ 0.44%); ไม่ใช่ accuracy คะแนนใกล้กัน
- YOLOv8m inference เร็วสุด แต่ pipeline ช้าที่สุดและ VRAM สูงสุดในขนาด
- ความแม่นยำ winner ใช้ VRAM มากกว่าตัวต่ำสุด 22.78 MiB; การจัดอันดับ inference และ pipeline ต้องแยกกัน

## ข้อแลกเปลี่ยนหลัก

### ความแม่นยำกับความเร็ว

YOLO26m-Seg มี mAP 0.574222; YOLOv8m-Seg มี mAP 0.506971
และ inference 27.232 ms เทียบกับ 32.043 ms ของโมเดลนำด้านความแม่นยำ
Pipeline winner คือ YOLO11m-Seg (76.971 ms); ไม่ใช้เวลา forward แทน throughput ของ pipeline

### ความแม่นยำกับหน่วยความจำ

YOLO26m-Seg ใช้ 912.16 MiB; YOLO11m-Seg ใช้ 889.38 MiB
และมี mAP 0.518307

## ข้อควรระวังในการตีความ

ไม่มีการทดสอบนัยสำคัญทางสถิติ; คะแนนใกล้กันเป็นคำบรรยาย ค่า AP/Recall อยู่ช่วง 0–1
Pipeline ไม่รวม RLE preparation และการอ่านเขียนดิสก์; VRAM เป็น peak allocated
MOTS20 ไม่ใช่ผลทดสอบความทนทานต่อ CCTV ขั้นสุดท้าย

## ข้อมูลสำหรับนำไปรวมต่อ

นำ YOLO26m สำหรับ accuracy, YOLOv8m สำหรับ inference และ YOLO11m สำหรับ pipeline/VRAM ไปเทียบข้ามขนาดโดยคง protocol และแหล่ง canonical เดิม ยังไม่สรุปครบ 17 โมเดล

[TIER_RESULTS.csv](metrics/TIER_RESULTS.csv) · [REPORT.md](REPORT.md) ·
[การวิเคราะห์ภาพ](PRESENTATION_SUMMARY_TH.md) ·
[การศึกษาหลัก](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study)
