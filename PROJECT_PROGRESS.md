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
