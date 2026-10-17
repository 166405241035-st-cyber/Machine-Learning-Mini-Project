# AirPredict — บันทึกแผนและความคืบหน้า

อัปเดต: 17 ตุลาคม 2026 (Asia/Bangkok)

## วิธีใช้บันทึก
เมื่อเริ่มแชตใหม่ ให้ผู้ช่วยอ่านไฟล์นี้ก่อนทำงานต่อ บันทึกนี้เป็นบริบทโครงการ ไม่ใช่ความจำอัตโนมัติข้ามแชต
อัปเดตสถานะตามผลที่ตรวจสอบได้จริง และไม่บันทึก API key หรือรหัสผ่าน
ผู้ใช้ขอให้อัปเดตไฟล์นี้เมื่อมีความคืบหน้าของงาน โดยไม่ต้องรอให้เตือนซ้ำ

## เป้าหมายและขอบเขตที่ตกลง
- ทำงานใน VS Code และเก็บโค้ดใน GitHub repository นี้
- ผู้ใช้ขอวางแผนก่อนเริ่มพัฒนา ปัจจุบันยังอยู่ขั้นเตรียมเครื่อง
- อ้างอิงเอกสาร Prediction Website Using Weather Data.docx
- ไฟล์ใน Downloads และ Downloads/mv มี SHA-256 ตรงกัน เป็นไฟล์เดียวกัน
- เว็บไซต์ AirPredict ประมาณ PM2.5 จากอุณหภูมิ ความชื้น และความเร็วลม
- ข้อมูลย้อนหลัง 2 ชุด: PM2.5 จาก OpenAQ และสภาพอากาศจาก NASA POWER
- เลือกพื้นที่หนึ่งในกรุงเทพฯ และช่วงเวลาที่ข้อมูลทั้งสองแหล่งตรงกัน
- ใช้ Linear Regression 1 โมเดล
- HTML, CSS, JavaScript สำหรับหน้าเว็บ; Python และ Flask สำหรับ backend
- ผู้ใช้กรอกข้อมูลเอง ผลลัพธ์หน่วย µg/m³ ไม่รวมการดึงสภาพอากาศเรียลไทม์

## สถานะที่ยืนยันแล้ว
- [x] อ่านเอกสารและสรุปขอบเขต
- [x] ตรวจพบ VS Code และ Git ผ่านคำสั่งในเครื่อง
- [x] ตรวจ repository ก่อนสร้างบันทึก: ยังว่าง และเชื่อมต่อ GitHub ได้
- [x] สร้างบันทึกความคืบหน้าฉบับแรก
- [x] ยืนยัน Python ที่ติดตั้ง รุ่น และ 64-bit (ผู้ใช้แจ้งว่าทำครบแล้ว ยังไม่ได้ตรวจผลคำสั่งโดยผู้ช่วย)
- [x] ยืนยันการติดตั้งส่วนขยาย VS Code (ผู้ใช้แจ้งว่าทำครบแล้ว ยังไม่ได้ตรวจผลคำสั่งโดยผู้ช่วย)
- [x] ยืนยันว่า clone repository และเปิดโฟลเดอร์ใน VS Code สำเร็จ (ผู้ใช้แจ้งว่าทำครบแล้ว ยังไม่ได้ตรวจผลคำสั่งโดยผู้ช่วย)
- [x] สร้าง .venv และติดตั้งแพ็กเกจ (ผู้ใช้แจ้งว่าทำครบแล้ว ยังไม่ได้ตรวจผลคำสั่งโดยผู้ช่วย)
- [x] เตรียม OpenAQ API key ในเครื่อง (ผู้ใช้แจ้งว่าทำครบแล้ว ยังไม่ได้ตรวจผลคำสั่งโดยผู้ช่วย)
- [ ] เลือกสถานี พิกัด และช่วงข้อมูลจริง
- [ ] เตรียม Dataset ฝึกโมเดล และพัฒนาเว็บ

หมายเหตุ: การตรวจครั้งแรกยังไม่พบคำสั่ง python หรือ py ใน PATH แต่ยังสรุปไม่ได้ว่าเครื่องไม่มี Python
ผู้ใช้พบว่า Git: Clone ไม่ปรากฏใน Command Palette จึงแนะนำ git clone ผ่าน Terminal
ล่าสุดผู้ใช้ส่งผล PowerShell จาก C:\Users\dY470g3\Downloads\minipro\Machine-Learning-Mini-Project ยืนยันว่าอยู่ในโฟลเดอร์ชื่อนี้แล้ว แต่ยังไม่ได้ตรวจ git remote เพื่อยืนยันการ clone

## การเตรียมเครื่องที่เสนอ
1. Python 3.12 แบบ 64-bit และเปิด Add python.exe to PATH ขณะติดตั้ง
2. VS Code extensions ของ Microsoft: Python, Pylance, Python Debugger
3. Clone repository และเปิดโฟลเดอร์
4. สร้าง environment:

```powershell
py -3.12 -m venv .venv
```

เลือก Python: Select Interpreter เป็น .venv แล้วติดตั้ง:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install flask pandas scikit-learn joblib matplotlib requests python-dotenv
```

แพ็กเกจที่เสนอข้างต้นยังไม่ได้ติดตั้งหรือทดสอบในโครงการ
จะจัด requirements.txt พร้อมรุ่นที่ทดสอบแล้วระหว่าง setup
เก็บ secret ใน .env และเพิ่ม .env กับ .venv/ ลง .gitignore ก่อน commit

## แผนพัฒนา
1. ตรวจ setup และการรัน Python
2. ตรวจความพร้อมข้อมูล OpenAQ ก่อนยืนยันสถานีและช่วงเวลา
3. ดึงข้อมูลสภาพอากาศ NASA POWER จากพิกัดที่สอดคล้องกัน
4. ตรวจหน่วย ค่าขาดหาย ข้อมูลซ้ำ และวัน/เขตเวลาของทั้งสองแหล่งก่อนรวม
5. เสนอข้อมูลรายวันประมาณ 1–2 ปี หากมีข้อมูลเพียงพอ ยังไม่ได้ยืนยันช่วงจริง
6. แบ่งข้อมูลตามเวลา: ข้อมูลเก่าสำหรับฝึก ข้อมูลใหม่สำหรับทดสอบ
7. ฝึก Linear Regression และรายงาน MAE, RMSE, R² เทียบ baseline แบบง่าย
8. บันทึกโมเดลและเชื่อม Flask กับแบบฟอร์มรับค่า 3 ตัว
9. ทดสอบ input ผิดพลาด การโหลดโมเดล และผลการทำนาย
10. เขียน README วิธีติดตั้ง รัน ฝึกโมเดล และข้อจำกัดจากผลจริง

## ความคืบหน้าล่าสุด
- ผู้ใช้ยืนยันว่าทำ setup ครบทั้ง 6 ขั้นแล้ว: Python, extensions, clone, .venv, แพ็กเกจ และบัญชี/API key OpenAQ
- สถานะสำเร็จอ้างอิงคำยืนยันของผู้ใช้ ยังไม่ได้ตรวจเวอร์ชันจริงหรือทดสอบ import โดยผู้ช่วย
- ปัญหา Python เรียกไม่ได้ที่บันทึกก่อนหน้านี้เป็นประวัติก่อนผู้ใช้แจ้ง setup สำเร็จ
- เพิ่ม .gitignore บน GitHub เพื่อกัน .venv/, .env และไฟล์ cache แล้ว ผู้ใช้ต้อง git pull เพื่อรับลงเครื่อง
- ไม่ขอให้ผู้ใช้ส่ง API key ในแชตหรือ commit ขึ้น GitHub

## จุดที่ต้องทำต่อทันที
1. ตรวจ import แพ็กเกจผ่าน Python ของ .venv แบบสั้น
2. เตรียม .gitignore และ .env.example โดยไม่มี secret
3. ตรวจสถานี OpenAQ ในกรุงเทพฯ และช่วงข้อมูล PM2.5 ย้อนหลังที่มีจริง
4. เลือกสถานีเดียวและช่วงเวลาที่สอดคล้องกับ NASA POWER ก่อนดาวน์โหลดข้อมูล
5. ยังไม่ฝึกโมเดลจนกว่าจะตรวจคุณภาพและรวมข้อมูลจริง

คำสั่งตรวจแพ็กเกจในโฟลเดอร์โปรเจ็กต์:

```powershell
.\.venv\Scripts\python.exe -c "import flask, pandas, sklearn, joblib, matplotlib, requests, dotenv; print('Setup OK')"
```

หากต้องการรับบันทึกที่อัปเดตจาก GitHub ลงเครื่อง ใช้ git pull ในโฟลเดอร์ repository

## แหล่งข้อมูล
- Repository: https://github.com/166405241035-st-cyber/Machine-Learning-Mini-Project
- OpenAQ API key: https://docs.openaq.org/using-the-api/quick-start
- NASA POWER Daily API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/

## ผลตรวจ setup ที่ยืนยันจาก Terminal
- ผู้ใช้ส่งผลทดสอบ import flask, pandas, sklearn, joblib, matplotlib, requests, dotenv ผ่าน Python ของ .venv: Setup OK
- git pull สำเร็จ และ git status แสดง main ตรงกับ origin/main ณ commit 807c4bd
- .venv/ ปรากฏเป็น untracked จึงยังไม่ได้ถูกติดตามใน working tree ตามผลที่ส่งมา
- เพิ่ม .gitignore บน GitHub แล้ว ขั้นต่อไปให้ git pull และ git status อีกครั้ง .venv/ ควรไม่ปรากฏใน untracked
- ยังไม่ได้บันทึกรุ่นแพ็กเกจจริงลง requirements.txt

## เริ่มขั้นค้นหาข้อมูลจริง
- ตรวจ GitHub พบ requirements.txt แล้ว
- เพิ่ม .env.example และ scripts/find_stations.py ใช้ OpenAQ API v3 พร้อม pagination, timeout และไม่แสดง key
- ค้นกรอบพิกัดกรุงเทพฯ และบริเวณใกล้เคียง ต้องตรวจว่าอยู่กรุงเทพฯ จริงก่อนเลือก
- ผลเขียน data/station_candidates.csv มี station/sensor IDs พิกัด และช่วงวันที่ระดับสถานี ซึ่งยังไม่รับรองความครบของ PM2.5 ระดับ sensor
- ยังไม่ได้รัน API จริง เนื่องจาก key อยู่ในเครื่องผู้ใช้
- ขั้นต่อไป: git pull, ตั้ง .env เฉพาะเครื่อง, รันสคริปต์ และตรวจรายชื่อสถานี

## ผลรันค้นหาสถานีจากผู้ใช้
- รัน scripts/find_stations.py สำเร็จ พบ 267 PM2.5 sensors และสร้าง data/station_candidates.csv ในเครื่องผู้ใช้
- จำนวน 267 เป็นจำนวน sensor ไม่ใช่จำนวนสถานีไม่ซ้ำ บางสถานีมีหลาย sensor
- ผู้ใช้เคยพิมพ์ OPENAQ_API_KEY=your_key_here ลง PowerShell จึงเกิด CommandNotFoundException บรรทัดนี้ต้องอยู่ใน .env แต่การรันสคริปต์ภายหลังสำเร็จ แสดงว่ามี key ใช้งานได้ใน environment หรือ .env โดยไม่ต้องเปิดเผยค่า
- ยังไม่ได้เลือกสถานีหรือยืนยันช่วงข้อมูล ต้องอ่าน CSV และตรวจ sensor-level coverage ต่อ

## การเข้าถึงไฟล์ในเครื่อง
- ผู้ใช้อนุญาตให้อ่านข้อมูลโครงการในเครื่องโดยตรง แทนให้แนบ CSV ซ้ำ
- อ่าน data/station_candidates.csv จาก C:/Users/dY470g3/Downloads/minipro/Machine-Learning-Mini-Project สำเร็จ ยืนยัน 267 แถว
- ตัวเลือกตรวจต่อ: Chulalongkorn Hospital location 5545, sensor 1304222, พิกัด 13.729852,100.536501 หน่วย µg/m³
- CSV ระบุช่วงสถานี 2016-08-18 ถึง 2026-10-17 แต่เป็น metadata ระดับ location ยังไม่ยืนยันความครบของ sensor หรือข้อมูลรายวัน
- ยังไม่เลือกสถานีถาวร ต้องตรวจ coverage จริงก่อน เสนอพิจารณาช่วงปีเต็ม 2024–2025 ถ้าข้อมูลเพียงพอ

## ผลตรวจรายวันจริง สถานีจุฬาลงกรณ์
- เพิ่ม scripts/check_coverage.py และรัน API จริงแล้ว เก็บ raw JSON, CSV, coverage_report.json ใน data/coverage/ เฉพาะเครื่อง ยังไม่อัปโหลดข้อมูลดิบ
- sensor 1304222: 2024 คืน 366 วัน ผ่านเกณฑ์ 275/366 (75.14%); 2025 คืน 259 วัน ผ่านเกณฑ์ 215/365 (58.90%)
- เกณฑ์เบื้องต้น: ค่า finite ไม่ติดลบ หน่วย µg/m³ coverage >=75% และ hasFlags=false ไม่เติมค่าฝุ่นวันที่ขาด
- ยังไม่เลือกสถานีถาวร เนื่องจากปี 2025 ขาดข้อมูลมาก ควรตรวจสถานีอื่น เช่น Thai Meteorological Department sensor 1304072 ก่อน
- ต้องพิจารณา missingness รายเดือนและกรอบวัน OpenAQ ก่อนรวม NASA POWER
- .venv launcher เปิดโปรเซสจาก tool ไม่ได้ จึงใช้ Python runtime ของ Codex กับ pure-Python packages requests/dotenv ใน .venv รันตรวจสำเร็จ ไม่ได้แก้ .venv ของผู้ใช้

## เตรียม Dataset จริงแล้ว
- ตรวจสถานีเพิ่ม: กรมอุตุฯ sensor 1304072 ผ่าน 249/366 วันในปี 2024 และ 47/365 วันในปี 2025; ม.เกษตรฯ sensor 1304409 ผ่าน 202 และ 233 วัน; สวนลุมพินี sensor 2076227 ผ่าน 164 และ 213 วัน
- เลือกจุฬาฯ sensor 1304222 สำหรับชุดข้อมูลต้นแบบจาก 4 สถานีที่ตรวจ ไม่อ้างว่าดีที่สุดของทุกสถานี
- ปี 2024 จุฬาฯ ผ่าน 275 วัน ปี 2025 ผ่าน 215 วัน รวม 490 วัน มีช่องว่างตามฤดูกาล (พ.ย.–ธ.ค. 2024 และบางเดือน 2025)
- ดาวน์โหลด NASA POWER hourly T2M (°C), RH2M (%), WS10M (m/s, ลมที่ความสูง 10m) พิกัด 13.729852,100.536501 แบบ UTC
- รวมอากาศตามขอบเขตเวลา UTC ของ OpenAQ จริง [start,end) 24 ชั่วโมง ไม่ใช้ LST แทนเวลาไทย และไม่เติมค่าที่ขาด
- data/processed/airpredict_daily.csv ในเครื่องมี 490 แถว ไม่มีวันที่ซ้ำ ช่วง 2024-01-01 ถึง 2025-12-31 อากาศครบทุกวันที่ฝุ่นผ่านเกณฑ์
- scripts/prepare_dataset.py รันสำเร็จจริง พร้อมตรวจหน่วย ค่า missing และจำนวนชั่วโมง เก็บ raw JSON และ dataset_summary.json ในเครื่อง
- ข้อมูลอากาศเป็นข้อมูลกริด ไม่ใช่การวัด ณ สถานีเดียวกัน; ตัวอย่างไม่ครอบคลุมทุกฤดูเท่ากัน
- ยังไม่ฝึกโมเดล ขั้นถัดไป Linear Regression 1 โมเดล แบ่งตามเวลา ประเมินเทียบค่าเฉลี่ยจากชุดฝึกด้วย MAE/RMSE/R²
- ฝั่ง tool ไม่สามารถเขียน .git/FETCH_HEAD ได้ จึงอัปเดต GitHub ผ่าน connector; สคริปต์ใน working tree ยัง untracked ต้องจัด sync อย่างระมัดระวัง (ไม่ลบไฟล์ของผู้ใช้)
- ข้อมูลดิบและ CSV ยังอยู่เฉพาะเครื่อง ไม่ได้เผยแพร่ dataset บน GitHub ต้องตรวจ attribution/licensing ก่อน

## เว็บ AirPredict รุ่นทดลองพร้อมใช้งาน
- เพิ่ม app.py, templates/index.html, static/style.css, static/app.js และ scripts/train_model.py พร้อม README และ tests/test_app.py
- ฝึก LinearRegression 1 โมเดลจาก 392 วันแรก และทดสอบ 98 วันท้าย (2025-06-13 ถึง 2025-12-31) ไม่สุ่มและไม่ใช้ชุดทดสอบฝึก
- MAE 5.1445, RMSE 6.1951 µg/m³, R² 0.52936; baseline ค่าเฉลี่ยจากชุดฝึก MAE 8.8792
- โมเดลบันทึก models/linear_regression.joblib; reports/metrics.json, test_predictions.csv, evaluation.png สร้างจริงในเครื่อง
- เว็บภาษาไทยรองรับหน้าจอแคบ มีแบบฟอร์ม 3 ตัวแปร ผลประมาณ กราฟและตัวเลขประเมิน พร้อมข้อจำกัดข้อมูล
- API ตรวจค่าผิดรูปแบบ, boolean, NaN/Infinity, ขอบเขต, missing model และเตือนค่านอกชุดฝึก ค่าทำนายติดลบแสดงเป็นไม่สามารถประมาณทางกายภาพ ไม่ clamp เงียบ
- unittest ผ่าน 6 กรณี ทดสอบ assets และหน้าเว็บ 200; ทดสอบ browser จริงกดทำนาย 30°C,70%,2m/s ได้ 32.30 µg/m³
- เปิด local Flask server http://127.0.0.1:5000 ผ่าน bundled Python 3.12.14 โดยใช้แพ็กเกจใน .venv; Python ของผู้ใช้เคยรันได้เอง แต่ tool ยังเรียก executable ของผู้ใช้ไม่ได้
- ผู้ใช้รันปกติด้วย .\.venv\Scripts\python.exe app.py; ถ้าพอร์ตถูกใช้อยู่ ใช้ server ที่เปิดไว้ก่อน
- .gitignore กัน data/, models/, reports/, .mplconfig/; ไม่เผยแพร่ API key หรือ raw data
- โค้ด GitHub อัปเดตผ่าน connector เพราะเครื่องมือยังเขียน .git/FETCH_HEAD ไม่ได้; working tree มีไฟล์เดียวกับที่สร้างไว้ แต่ metadata Git ในเครื่องอาจยังตามหลัง ก่อน pull ต้องตรวจ untracked files เพื่อไม่ชนไฟล์
- ยังไม่ได้ deploy ออนไลน์ สถานะคือเว็บทดลองบนเครื่องและผลประเมินย้อนหลัง งานถัดไปให้ผู้ใช้ทดลอง UI และตรวจความเหมาะสมสำหรับรายงาน
