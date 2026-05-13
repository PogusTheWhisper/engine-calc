# Engine Calc

เครื่องคำนวณสเปคเครื่องยนต์สูบเดี่ยวสำหรับงานแต่ง — ใส่ค่า Bore, Stroke และชนิดน้ำมัน แล้วระบบจะคำนวณ:

- ความจุกระบอกสูบ (cc)
- ขนาดวาล์วไอดี / ไอเสีย / ลิ้นเร่ง
- ลักษณะเครื่อง (Long Stroke / Square / Over Square) จาก B/S Ratio
- กำลังอัด, ขนาดห้องเผาไหม้, หัวฉีด, AFR
- ประมาณ HP, แรงบิด, รอบพลัง, Cam Duration, Valve Lift

Deploy บน Vercel แล้ว — เว็บหน้าเดียวเรียก API Python ฝั่ง serverless ไม่มี dependency เพิ่ม (ใช้ stdlib อย่างเดียว)

🔗 **Live**: https://engine-calc-ashen.vercel.app/

## โครงสร้าง

```
api/
  index.py     # ฟังก์ชันคำนวณ (Python ล้วน) + WSGI wrapper
  index.html   # หน้าเว็บ (HTML/CSS/JS รวมไฟล์เดียว)
vercel.json    # config Vercel
```

- `api/index.py` — ฟังก์ชันคำนวณแยกเป็นชิ้นเล็ก ๆ อ่านง่าย (`calc_displacement`, `calc_valve_sizes`, `calc_fuel_specs` ฯลฯ) ตามด้วย `app(environ, start_response)` WSGI สั้น ๆ ห่อให้ Vercel เรียกได้
- `api/index.html` — UI ภาษาไทย ธีมเข้ม-ส้ม 3 ขั้นตอน ใช้ `fetch` ดึงข้อมูลจาก `/api/calculate`

## API

```
GET /api/calculate?bore=57&stroke=58.7&fuel=95
```

พารามิเตอร์:

| ชื่อ | จำเป็น | คำอธิบาย |
|------|-------|----------|
| `bore`   | ใช่ | ขนาดลูกสูบ (mm) > 0 |
| `stroke` | ใช่ | ช่วงชัก (mm) > 0 |
| `fuel`   | ไม่ | `91`, `95`, `E20`, `E85` |

ถ้าไม่ส่ง `fuel` จะคืนแค่ค่าความจุ + วาล์ว + B/S character

## รันบนเครื่อง

ต้องมี Vercel CLI:

```bash
npm i -g vercel
vercel dev
```

เปิด `http://localhost:3000`

## Deploy

```bash
vercel          # preview
vercel --prod   # production
```

ครั้งแรกจะถาม link โปรเจ็กต์ — กด yes ตามค่า default ได้

## หมายเหตุ

ค่ากำลังและแรงบิดที่ระบบประมาณ ใช้สูตร BMEP อย่างง่าย ไม่ใช่ค่าจริงจาก dyno — ใช้เป็น **แนวทาง** เท่านั้น ของจริงควรปรึกษาช่างผู้เชี่ยวชาญก่อนแต่งเครื่อง

## License

ดู `LICENSE`
