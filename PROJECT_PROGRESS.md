# AirPredict — บันทึกแผนและความคืบหน้า

อัปเดต: 17 ตุลาคม 2026 (Asia/Bangkok)

## วิธีใช้บันทึก
เมื่อเริ่มแชตใหม่ ให้ผู้ช่วยอ่านไฟล์นี้ก่อนทำงานต่อ บันทึกนี้เป็นบริบทโครงการ ไม่ใช่ความจำอัตโนมัติข้ามแชต
อัปเดตสถานะตามผลที่ตรวจสอบได้จริง และไม่บันทึก API key หรือรหัสผ่าน

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
- [ ] ยืนยัน Python ที่ติดตั้ง รุ่น และ 64-bit
- [ ] ยืนยันการติดตั้งส่วนขยาย VS Code
- [ ] ยืนยันว่า clone repository และเปิดโฟลเดอร์ใน VS Code สำเร็จ
- [ ] สร้าง .venv และติดตั้งแพ็กเกจ
- [ ] เตรียม OpenAQ API key ในเครื่อง
- [ ] เลือกสถานี พิกัด และช่วงข้อมูลจริง
- [ ] เตรียม Dataset ฝึกโมเดล และพัฒนาเว็บ

หมายเหตุ: การตรวจครั้งแรกยังไม่พบคำสั่ง python หรือ py ใน PATH แต่ยังสรุปไม่ได้ว่าเครื่องไม่มี Python
ผู้ใช้พบว่า Git: Clone ไม่ปรากฏใน Command Palette จึงแนะนำ git clone ผ่าน Terminal ยังไม่มีผลยืนยันว่า clone สำเร็จ

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

## จุดที่ต้องทำต่อทันที
ให้ผู้ใช้เปิด Terminal ใน VS Code และตรวจ:

```powershell
py --version
py -3.12 --version
```

หาก py ใช้ไม่ได้ ให้ลอง python --version และใช้ผลจริงวินิจฉัยต่อ
หาก clone ไว้ก่อนมีบันทึกนี้ ให้ git pull หลังเข้าโฟลเดอร์ repository เพื่อรับไฟล์ล่าสุด

## แหล่งข้อมูล
- Repository: https://github.com/166405241035-st-cyber/Machine-Learning-Mini-Project
- OpenAQ API key: https://docs.openaq.org/using-the-api/quick-start
- NASA POWER Daily API: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
