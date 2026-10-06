# Medium — qualitative case selection v2

คัดจาก 12 frozen visualization frames โดยตรวจ per-frame metrics, original/GT และ saved RLE ที่ confidence ≥0.25 / mask matching IoU ≥0.50 ตาม evaluator/ignore policy เดิม ไม่รัน inference

1 shared anchor + 3 cases ตามพฤติกรรมของ tier ไม่บังคับภาพทั้งหมดตรงกันระหว่าง tier; ภายใน case ใช้เฟรมเต็มเดียวกันทุกโมเดล ROI เป็นภาพเสริม ไม่ซ่อน full-frame errors

| Case | Sequence / frame | Why selected / decision use | Source comparison |
|---|---|---|---|
| 1 | MOTS20-05 / 000419 | tier diagnostic: small GT and extra output; ช่วยเทียบเมื่อให้ความสำคัญกับ instance เล็ก: YOLO26m match 2002 แต่ YOLO11m/YOLOv8m ไม่ผ่าน; YOLO11m ยังมี FP ริมขวา | reuse existing image |
| 2 | MOTS20-09 / 000263 | shared anchor: common failure; ใช้ตรวจ error ในกลุ่มคน และเห็นว่า FN ของ YOLOv8m ที่ GT 2018 มี mask อยู่แล้วแต่ IoU ต่ำกว่าเกณฑ์เล็กน้อย | reuse existing image |
| 3 | MOTS20-02 / 000001 | counterexample: more TP with extra outputs; ช่วยเห็นว่า YOLOv8m มี TP สูงกว่า accuracy leader ในเฟรมนี้ ขณะที่ YOLO11m ไม่มี FP แต่ FN มากกว่า | reuse existing image |
| 4 | MOTS20-11 / 000450 | control plus error: equal valid GT coverage, different FP; ใช้ตรวจภาระ extra-instance output เมื่อ coverage เท่ากัน: ทุกโมเดล TP 9 / FN 0 แต่ YOLO26m/YOLO11m/YOLOv8m มี FP 1/0/2 ในเฟรมนี้ | new composite from saved predictions |

## ทำไมบางภาพยังตรงกับ tier อื่น

Case 2 (09/263) ใช้ร่วมเพื่อเทียบ FN/FP บน GT ชุดเดียวกัน กรณีอื่นซ้ำได้เมื่อ error เดียวกันช่วยตรวจคนละโมเดล: 05/419 ใช้ L/M ตรวจ GT 2002; 02/1 ใช้ L/M ตรวจ equal counts และ GT ต่างชุด; 02/600 ใช้ Largest/Small ตรวจกรณีสวนอันดับ; 02/300 ใช้ Small/Nano ตรวจ TP–FP trade-off; 11/1 ใช้ L/N แต่ L ตรวจ GT 2016 ส่วน N ตรวจ GT 2028 และ extra mask; 11/450 ใช้ Largest/Medium ตรวจ coverage เท่ากันกับ extra output ของคนละชุดโมเดล ไม่ใช้จำนวนภาพซ้ำเป็นหลักฐานอิสระเพิ่ม

## การแทน case เดิม

เดิม Case 4 (09/1) TP 6 / FP 0 / FN 0 ทุกโมเดล; 11/450 คง coverage เท่ากันแต่แสดง FP ต่างกัน ภาพ/หลักฐานเก่ายังคงเดิมเพื่อ audit; presentation เก่าเก็บใน reports/archive

## ขอบเขต

ทั้งห้า tier มี 20 case slots แต่ใช้ original frames ต่างกัน 10 เฟรม (เดิม 6) ชุดใหม่มี MOTS20-11 และยังมี common failure / counterexample ไม่เลือกเฉพาะ frame ที่ accuracy leader ชนะ ทั้งนี้ pool 12 เฟรมไม่แทน dataset; ไม่อ้างว่าเป็นเฟรมที่ต่างที่สุดใน 2,862 เฟรม ไม่ใช้ภาพวัด latency/VRAM หรือ statistical significance

[Candidate pool](CANDIDATE_POOL.json) · [Case evidence](CASE_EVIDENCE.json) · [Focus evidence](FOCUS_EVIDENCE.json) · [Decision audit](CASE_DECISION_AUDIT.json) · [Active selection](../../../../manifests/QUALITATIVE_SELECTION.json)
