# สรุปผล Medium (M) YOLO Instance Segmentation

## สรุปใน 1 นาที

- ทดสอบ YOLO26m-Seg, YOLO11m-Seg และ YOLOv8m-Seg สำหรับ Person instance segmentation
- MOTS20 2,862 frames และ 26,894 Person GT instances ใช้ pretrained / no fine-tuning ภายใต้ controlled benchmark เดียวกัน
- Accuracy สูงสุด: YOLO26m-Seg; AP75 สูงสุด: YOLO26m-Seg; Recall สูงสุด: YOLO26m-Seg
- Inference เร็วสุด: YOLOv8m-Seg; pipeline เร็วสุดและ FPS สูงสุด: YOLO11m-Seg
- Peak allocated VRAM ต่ำสุด: YOLO11m-Seg
- คู่ที่ใกล้ที่สุดด้าน Mask mAP50-95: YOLO11m-Seg / YOLOv8m-Seg ต่าง 0.011336; ไม่ได้ทดสอบ statistical significance
- สถานะ PASS WITH WARNINGS; pipeline FPS ไม่รวม RLE preparation และ disk I/O

## ผลหลัก

| Model | Mask mAP50-95 | Recall | F1 | Inference ms | Pipeline ms | FPS | Peak VRAM MiB |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26m-Seg | 0.574222 | 0.815312 | 0.863761 | 32.043 | 77.309 | 12.935 | 912.16 |
| YOLO11m-Seg | 0.518307 | 0.805049 | 0.856228 | 30.574 | 76.971 | 12.992 | 889.38 |
| YOLOv8m-Seg | 0.506971 | 0.793857 | 0.841578 | 27.232 | 78.112 | 12.802 | 1018.76 |


## แต่ละโมเดลเด่นด้านไหน

**YOLO26m-Seg**: จุดเด่น: Highest Mask mAP50-95 / Highest AP75 / Highest Recall จุดที่ด้อยกว่า: forward ช้ากว่าตัวที่เร็วที่สุด; ใช้ peak allocated VRAM มากกว่าตัวที่ต่ำสุด อันดับเชิงตัวเลขในสามโมเดลคือ accuracy 1, inference speed 3, pipeline speed 2 และ VRAM ต่ำ 2 เหมาะเริ่มพิจารณาเมื่อเน้น accuracy แล้วตรวจว่าค่า latency และ memory อยู่ในข้อจำกัดของงาน

**YOLO11m-Seg**: จุดเด่น: Fastest pipeline / Highest FPS / Lowest VRAM จุดที่ด้อยกว่า: Mask mAP50-95 ต่ำกว่าตัวนำ; forward ช้ากว่าตัวที่เร็วที่สุด อันดับเชิงตัวเลขในสามโมเดลคือ accuracy 2, inference speed 2, pipeline speed 1 และ VRAM ต่ำ 1 เหมาะพิจารณาเมื่อจำกัด memory โดยดู accuracy และ latency ประกอบ

**YOLOv8m-Seg**: จุดเด่น: Fastest inference จุดที่ด้อยกว่า: Mask mAP50-95 ต่ำกว่าตัวนำ; ใช้ peak allocated VRAM มากกว่าตัวที่ต่ำสุด อันดับเชิงตัวเลขในสามโมเดลคือ accuracy 3, inference speed 1, pipeline speed 3 และ VRAM ต่ำ 3 เหมาะพิจารณาเมื่อเวลา forward เป็นข้อจำกัด โดยยอมรับ accuracy ที่ลดลงจากตัวนำ

## สิ่งที่น่าสนใจจากรอบนี้

- Observation: YOLO26m-Seg มี Mask mAP50-95 สูงสุด 0.574222; ห่างอันดับถัดไป 0.055915 บนสเกล 0–1
- Observation: YOLO26m-Seg นำ AP75 และ YOLO26m-Seg นำ Recall
- Observation: forward เร็วสุดคือ YOLOv8m-Seg, pipeline เร็วสุดและ FPS สูงสุดคือ YOLO11m-Seg, VRAM ต่ำสุดคือ YOLO11m-Seg
- คู่ที่ใกล้ที่สุดด้าน Mask mAP50-95: YOLO11m-Seg / YOLOv8m-Seg ต่าง 0.011336; ไม่ได้ทดสอบ statistical significance
- Interpretation: การเลือกต้องแยก accuracy, forward, pipeline และ memory ไม่สรุปว่า parameters ต่ำกว่าจะเร็วหรือใช้ VRAM ต่ำกว่าเสมอ

## Trade-off ที่เห็น

### Accuracy

YOLO26m-Seg มี Mask mAP50-95 สูงสุด ต้องดู Recall และ AP75 ประกอบตามข้อจำกัด

### Speed

YOLOv8m-Seg มี inference mean ต่ำสุด ส่วน YOLO11m-Seg มี pipeline mean ต่ำสุด; คู่ที่ใกล้ที่สุดด้าน inference mean: YOLO26m-Seg / YOLO11m-Seg ต่าง 1.469 ms; ไม่ได้ทดสอบ statistical significance

### Memory / Resource

YOLO11m-Seg ใช้ peak allocated VRAM ต่ำสุด จำนวน parameters และ GFLOPs ไม่ใช่ข้อพิสูจน์เหตุเชิงสาเหตุของ latency

### ภาพรวม

เลือกตามข้อจำกัดจริงโดยแยก accuracy, forward, pipeline และ memory ไม่สร้าง weighted score และไม่สรุปความพร้อมใช้งาน CCTV จากชุดนี้เพียงชุดเดียว

## สิ่งที่ต้องระวังในการตีความ

ผลนี้เป็น Person instance segmentation รายเฟรมบน MOTS20 ไม่ใช่ MOTS tracking; 26,894 GT instances เป็น annotation รายเฟรม ไม่ใช่จำนวนคนไม่ซ้ำ TP-only IoU/Dice พิจารณาเฉพาะคู่ที่ match ได้ ภาพต่อเนื่องสัมพันธ์กันและไม่มีการทดสอบ statistical significance ผลยังไม่ยืนยัน blur, low-light, มุมกล้อง, ระดับ occlusion หรือ deployment suitability จึงใช้เพื่อเลือก candidate for later CCTV robustness evaluation เท่านั้น

คงคำเตือน NNPACK / pycocotools ตามหลักฐาน และแยก pipeline FPS ออกจากระบบที่บันทึก masks ครบวงจร

## ข้อมูลสำหรับนำไปรวมต่อ

[metrics/TIER_RESULTS.csv](metrics/TIER_RESULTS.csv) · [REPORT.md](REPORT.md) · [PRESENTATION_SUMMARY_TH.md](PRESENTATION_SUMMARY_TH.md) · [Master Study](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study)
