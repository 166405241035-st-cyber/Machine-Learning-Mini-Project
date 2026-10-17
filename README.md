# AirPredict

เว็บไซต์ประมาณ PM2.5 จากอุณหภูมิ ความชื้น และความเร็วลมเฉลี่ยรายวัน ด้วย Linear Regression 1 โมเดล ใช้ข้อมูลพื้นที่โรงพยาบาลจุฬาลงกรณ์ กรุงเทพฯ

## รันใน VS Code บน Windows

เปิด Terminal ในโฟลเดอร์โปรเจ็กต์ หากเตรียมเครื่องตามบันทึกไว้แล้วและมี models/linear_regression.joblib ให้รัน:

```powershell
.\.venv\Scripts\python.exe app.py
```

เปิด http://127.0.0.1:5000 แล้วกรอกค่าหรือทดลอง 30 °C, ความชื้น 70%, ลม 2 m/s กดประมาณค่า PM2.5 หน้าเว็บจะแสดงผลและกราฟประเมินโมเดล

หากเริ่มจากเครื่องใหม่:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

เปิด .env ใส่ OPENAQ_API_KEY ของตนเอง แล้วเตรียมข้อมูลและฝึกโมเดล:

```powershell
.\.venv\Scripts\python.exe scripts\find_stations.py
.\.venv\Scripts\python.exe scripts\check_coverage.py
.\.venv\Scripts\python.exe scripts\prepare_dataset.py
.\.venv\Scripts\python.exe scripts\train_model.py
.\.venv\Scripts\python.exe app.py
```

API key และ .venv ไม่ถูก commit ห้ามนำ key ไปวางในโค้ด โมเดลและ dataset สร้างในเครื่องจากสคริปต์ ไม่ต้องดาวน์โหลดไฟล์ joblib จากบุคคลอื่น

## ข้อมูลและการทดลอง

- OpenAQ location 5545, sensor 1304222: PM2.5 หน่วย µg/m³
- NASA POWER: พิกัด 13.729852, 100.536501; T2M (°C), RH2M (%), WS10M (m/s ที่ 10 เมตร)
- ช่วงปี 2024–2025 รวมข้อมูลที่ผ่านเกณฑ์ 490 วัน
- ค่าฝุ่นต้องไม่ติดลบ มี coverage อย่างน้อย 75% และไม่มี quality flag
- ดึงอากาศรายชั่วโมง UTC และเฉลี่ยภายใน [เวลาเริ่ม, เวลาสิ้นสุด) ของค่าฝุ่นแต่ละวัน ต้องมีครบ 24 ชั่วโมง ไม่เติมค่าขาด
- ฝึก 392 วันแรก ทดสอบ 98 วันท้ายตามลำดับเวลา ไม่สุ่มและไม่ฝึกซ้ำด้วยชุดทดสอบ
- ทดสอบ 2025-06-13 ถึง 2025-12-31: MAE 5.14 µg/m³, RMSE 6.20 µg/m³, R² 0.529
- Baseline ใช้ค่าเฉลี่ยจากชุดฝึก: MAE 8.88 µg/m³
- ผลจาก snapshot ที่ตรวจครั้งนี้ API อาจมีการแก้ไขข้อมูลย้อนหลัง

ผลเต็มอยู่ reports/metrics.json, reports/test_predictions.csv และ reports/evaluation.png หลังฝึก

## ข้อจำกัด

เป็นการประมาณค่าจากอากาศเฉลี่ยในช่วงวันเดียวกัน ไม่ใช่การพยากรณ์ล่วงหน้าหรือค่าตรวจวัดสด ข้อมูลฝุ่นขาดมากในบางเดือน โดยเฉพาะปลายปี 2024 ทำให้ฤดูกาลในชุดข้อมูลไม่สมดุล อากาศ NASA POWER เป็นข้อมูลกริด ผลทดสอบนี้ไม่รับรองผลในพื้นที่อื่น

เว็บเตือนเมื่อกรอกค่านอกช่วงชุดฝึก หาก Linear Regression ให้ค่าติดลบจะแสดงว่าผลไม่สมเหตุสมผลแทนการปรับเป็นศูนย์เงียบ ๆ MAE เป็นค่าความผิดพลาดเฉลี่ยของชุดทดสอบ ไม่ใช่ช่วงรับประกันผลรายครั้ง

## ทดสอบ

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## โครงสร้าง

- app.py — Flask และ API /api/predict
- templates/, static/ — หน้าเว็บภาษาไทย
- scripts/ — ค้นสถานี ตรวจ coverage รวมข้อมูล และฝึกโมเดล
- data/ — ข้อมูลในเครื่อง ไม่เผยแพร่ raw data โดยอัตโนมัติ
- models/ — โมเดลที่สร้างในเครื่อง
- reports/ — ผลประเมิน
- PROJECT_PROGRESS.md — บันทึกสถานะและงานต่อ

## แหล่งอ้างอิง

- [OpenAQ API และแหล่งข้อมูลต้นทาง](https://docs.openaq.org/) ต้องตรวจผู้ให้บริการและ license ของสถานีก่อนเผยแพร่ dataset ต่อ
- [NASA POWER Hourly API](https://power.larc.nasa.gov/docs/services/api/temporal/hourly/)
- [Scikit-learn LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Flask](https://flask.palletsprojects.com/)
