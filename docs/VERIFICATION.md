# ผลตรวจความพร้อม AirPredict จากโฟลเดอร์ใหม่

ตรวจวันที่ 17 ตุลาคม 2026 บน Windows ใน C:/Users/dY470g3/Downloads/minipro/AirPredict-verification โดย clone จาก GitHub commit ae2d34a ก่อนแก้ข้อบกพร่องที่พบ

## ผลสรุป

ติดตั้ง environment ใหม่ ดาวน์โหลดข้อมูลใหม่ ฝึกโมเดล สร้างกราฟ และเปิดเว็บสำเร็จ ไม่ได้คัดลอก .venv, dataset, โมเดล หรือ reports จากโฟลเดอร์งานเดิม ใช้เฉพาะ API key ที่ผู้ใช้ตั้งไว้ โดยคัดลอก .env ในเครื่องและไม่เปิดเผยค่า

| ขั้นตรวจ | ผล |
|---|---|
| Clone repository | ผ่าน โดยใช้ OpenSSL เฉพาะคำสั่ง clone |
| Python | 3.12.14 แบบ 64-bit จาก runtime Codex |
| Environment ใหม่ | .venv แบบ include-system-site-packages=false |
| pip install -r requirements.txt | ผ่าน ครบ 32 แพ็กเกจที่ระบุ |
| pip check / imports | ผ่าน |
| ค้นหาสถานี | ผ่านหลังแก้ UTF-8 output |
| ดาวน์โหลด PM2.5 | ผ่าน |
| ดาวน์โหลด NASA POWER และรวมข้อมูล | ผ่าน ได้ 490 วัน |
| ฝึกโมเดล | ผ่าน ฝึก 392 วัน ทดสอบ 98 วัน |
| สร้างกราฟวิเคราะห์ | ผ่าน 6 ชุด |
| ทดสอบอัตโนมัติหลังแก้ไข | ผ่าน 10 กรณี พร้อมเปิด ResourceWarning เป็น error |
| สร้าง SVG ซ้ำ | ผ่าน ภาพทั้ง 6 ตรงกันทุกไบต์ |
| HTTP หน้าทำนายและหน้าวิเคราะห์ | 200 ทั้งสองหน้า |
| HTTP กราฟ SVG | 200 ครบ 6 รูป |
| POST /api/predict | 200; 30°C,70%,2m/s ให้ 32.30 µg/m³ |
| Browser | เปิดหน้าทำนายจาก server ในโฟลเดอร์ใหม่และตรวจเนื้อหาได้ |

## ผลโมเดลที่สร้างใหม่

- MAE 5.1445413559 µg/m³
- RMSE 6.1950544033 µg/m³
- R² 0.5293613632
- Baseline MAE 8.8791873178 µg/m³
- ผลตรงกับการทดลองก่อนหน้าในระดับตัวเลขที่รายงาน

## ข้อบกพร่องที่พบและแก้ไข

1. find_stations.py หยุดเมื่อเจอชื่อสถานีที่มีอีโมจิบน console encoding cp874: ตั้ง stdout เป็น UTF-8 และเพิ่ม regression test จำลอง console แบบเดิม
2. SVG มีเวลาและรหัสสุ่ม ทำให้ Git แสดงความเปลี่ยนแปลงทุกครั้งที่สร้างใหม่: กำหนด svg.hashsalt และตัด metadata Date แล้วทดสอบสร้างซ้ำได้ไฟล์เดิม
3. README ชุดคำสั่งเริ่มต้นยังไม่รวม analyze_results.py: เพิ่มให้ทำครบก่อนเปิดเว็บ
4. tests เปิด response ไฟล์โดยไม่ปิด: ใช้ context manager และรันใหม่โดยให้ ResourceWarning เป็น error
5. PNG ที่สร้างจากการวิเคราะห์ปรากฏเป็น untracked: ignore PNG exports และเก็บ SVG เป็นภาพใน GitHub

## ข้อจำกัดของการตรวจ

การรันจากเครื่องมือใช้ Python runtime Codex 3.12.14 ไม่ใช่ Python 3.12.10 ของผู้ใช้ เพราะเครื่องมือเปิด executable ตัวนั้นไม่ได้ การตรวจนี้ยืนยัน clean environment บนเครื่อง Windows นี้ ยังไม่ใช่การตรวจข้ามเครื่องหรือทุกเวอร์ชัน Python

Git ผ่านเครื่องมือมีข้อผิดพลาด Schannel SEC_E_NO_CREDENTIALS จึงใช้ git -c http.sslBackend=openssl clone เฉพาะครั้งนี้ ไม่ปิด TLS certificate verification และไม่เปลี่ยน global Git config

เปิด server ทดสอบที่ http://127.0.0.1:5002 เพื่อไม่ชน server เดิมที่ 5000/5001 ข้อมูลดิบ โมเดล reports และ .env อยู่เฉพาะในเครื่อง ไม่ได้อัปโหลด GitHub

## ใช้งานต่อ

โฟลเดอร์ AirPredict-verification เป็น checkout ใหม่ที่ทดสอบแล้ว พร้อม environment ข้อมูล โมเดล และกราฟ ผู้ใช้สามารถเปิดโฟลเดอร์นี้ใน VS Code เพื่อทำงานต่อ เก็บโฟลเดอร์เดิมไว้ ไม่ลบหรือรีเซ็ตประวัติ Git เดิม

```powershell
cd C:\Users\dY470g3\Downloads\minipro\AirPredict-verification
.\.venv\Scripts\python.exe -m flask --app app run --port 5002
```

หาก server 5002 เปิดอยู่แล้ว ให้ใช้หน้าเว็บที่เปิดไว้ ไม่ต้องรัน server ซ้ำ
