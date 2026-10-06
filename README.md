# Medium (M) — การทดสอบ YOLO Instance Segmentation บน MOTS20

## ภาพรวม

เปรียบเทียบการแยก Person เป็นราย instance บน MOTS20 ด้วยโมเดล pretrained โดยไม่ฝึกเพิ่มหรือปรับจูน ประเมินรายเฟรมไม่ใช่การติดตามคน เอกสารนี้ใช้แนะนำ repository และเชื่อมไปยังผลเชิงตัวเลขรายงานเทคนิคและการวิเคราะห์ภาพ

## โมเดลที่ทดสอบ

| ตระกูล | โมเดล | ขนาด |
| --- | --- | --- |
| YOLO26 | YOLO26m-Seg | Medium (M) |
| YOLO11 | YOLO11m-Seg | Medium (M) |
| YOLOv8 | YOLOv8m-Seg | Medium (M) |

## สถานะการทดลอง

COMPLETE / PASS WITH WARNINGS — ครบ 3/3 โมเดล โมเดลละ 2,862 เฟรมและ Person GT รายเฟรม 26,894 instances
รอบทดลอง: `benchmark-20261002T075505Z` ใช้ผลที่บันทึกไว้ ไม่มีการรัน inference ใหม่เพื่อปรับเอกสาร

## ผลลัพธ์หลัก

| โมเดล | Mask mAP50-95 | Recall | F1 | Inference (ms) | Pipeline (ms) | FPS | Peak allocated VRAM (MiB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YOLO26m-Seg | 0.574222 | 0.815312 | 0.863761 | 32.043 | 77.309 | 12.935 | 912.16 |
| YOLO11m-Seg | 0.518307 | 0.805049 | 0.856228 | 30.574 | 76.971 | 12.992 | 889.38 |
| YOLOv8m-Seg | 0.506971 | 0.793857 | 0.841578 | 27.232 | 78.112 | 12.802 | 1018.76 |

## เอกสารประกอบ

- [บทสรุปเชิงตัวเลข](RESULTS_SUMMARY_TH.md)
- [การวิเคราะห์ภาพและพฤติกรรมเชิงคุณภาพ](PRESENTATION_SUMMARY_TH.md)
- [รายงานเทคนิค](REPORT.md)
- [โพรโทคอลการทดลอง](EXPERIMENT_PROTOCOL.md)

## การนำทางในชุดการศึกษา

[Largest (X/E)](https://github.com/folklazy/YOLO_Large_Seg_MOTS20_Benchmark) | [Second-largest (L/C)](https://github.com/folklazy/YOLO_Second_Largest_Seg_MOTS20_Benchmark) | [Medium (M)](https://github.com/folklazy/YOLO_Medium_Seg_MOTS20_Benchmark) | [Small (S)](https://github.com/folklazy/YOLO_Small_Seg_MOTS20_Benchmark) | [Nano (N)](https://github.com/folklazy/YOLO_Nano_Seg_MOTS20_Benchmark) | [การศึกษาหลัก](https://github.com/folklazy/YOLO_Instance_Segmentation_MOTS20_Scaling_Study)

## หลักฐานสำหรับตรวจสอบซ้ำ

[ค่าตัวชี้วัด](metrics/) · [การตั้งค่า](configs/) · [หลักฐานและแหล่งที่มา](manifests/) · [ภาพและกราฟ](outputs/) · [บันทึกย้อนหลัง](reports/archive/)
