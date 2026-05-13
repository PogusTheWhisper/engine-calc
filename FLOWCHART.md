# Engine Calculator — Flowchart

## 1. Flowchart รวม (Mermaid)

```mermaid
flowchart TD
    A([เริ่ม]) --> B[/รับค่า Bore, Stroke/]
    B --> C{Bore > 0<br>และ Stroke > 0?}
    C -- ไม่ --> E1[แสดง Error]
    E1 --> B
    C -- ใช่ --> D[คำนวณ STEP 1<br>CC, วาล์ว, B/S Ratio]
    D --> S1[/แสดงผล STEP 1/]
    S1 --> F[/เลือกน้ำมัน<br>95 / E20 / E85/]
    F --> G{เลือกแล้ว?}
    G -- ไม่ --> E2[แสดง Error]
    E2 --> F
    G -- ใช่ --> H[คำนวณ STEP 2<br>CR, ห้องเผาไหม้, หัวฉีด, AFR]
    H --> I[คำนวณ STEP 3<br>HP, แรงบิด, RPM, Cam, Lift]
    I --> J[/แสดงผล STEP 2 + STEP 3/]
    J --> K([จบ])
```

## 2. Flowchart รายฟังก์ชัน

### STEP 1 — ข้อมูลพื้นฐานเครื่องยนต์

```mermaid
flowchart TD
    A([Input: bore, stroke]) --> B["CC = π/4 × bore² × stroke / 1000"]
    B --> C["valve_intake = bore × 0.50"]
    C --> D["valve_exhaust = bore × 0.42"]
    D --> E["throttle = bore × 0.60"]
    E --> F["bs_ratio = bore / stroke"]
    F --> G{bs_ratio?}
    G -- "< 0.9" --> H1[Long Stroke<br>แรงบิดต่ำรอบ]
    G -- "0.9–1.1" --> H2[Square<br>สมดุล]
    G -- "> 1.1" --> H3[Over Square<br>รอบสูง]
    H1 --> Z([Output])
    H2 --> Z
    H3 --> Z
```

### STEP 2 — น้ำมันเชื้อเพลิง

```mermaid
flowchart TD
    A([Input: cc, fuel_type]) --> B{ชนิดน้ำมัน}
    B -- "Gasohol 95" --> C1["CR=10.5<br>inj_mult=1.0<br>AFR=14.7"]
    B -- "E20" --> C2["CR=11.5<br>inj_mult=1.2<br>AFR=13.8"]
    B -- "E85" --> C3["CR=13.0<br>inj_mult=1.3<br>AFR=9.8"]
    C1 --> D[chamber = cc / CR − 1]
    C2 --> D
    C3 --> D
    D --> E["injector = cc × inj_mult"]
    E --> Z([Output: CR, chamber, injector, AFR, ignition])
```

### STEP 3 — ประมาณกำลัง

```mermaid
flowchart TD
    A([Input: cc, bore, stroke, CR]) --> B{B/S ratio?}
    B -- "> 1.05" --> C1["RPM=11000<br>Cam 270–285°<br>Lift = bore × 0.28"]
    B -- "0.9–1.05" --> C2["RPM=9500<br>Cam 260–270°<br>Lift = bore × 0.26"]
    B -- "< 0.9" --> C3["RPM=8000<br>Cam 250–260°<br>Lift = bore × 0.24"]
    C1 --> D["BMEP = 900 + CR−10 × 30 kPa"]
    C2 --> D
    C3 --> D
    D --> E["kW = BMEP × cc × RPM / 120,000,000"]
    E --> F["HP = kW / 0.7457"]
    F --> G["Torque = 9549 × kW / RPM"]
    G --> Z([Output: HP, Torque, RPM, Cam, Lift])
```

## 3. ASCII Flowchart (เผื่อ Mermaid render ไม่ขึ้น)

```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Input: Bore, Stroke │
└──────┬──────────────┘
       │
       ▼
   ╱───────────╲
  ╱ ตรวจสอบค่า  ╲ ──── No ──▶ แจ้ง Error
   ╲ > 0 ?     ╱
    ╲─────────╱
       │ Yes
       ▼
┌─────────────────────────────────┐
│ STEP 1: คำนวณ                   │
│  • CC = π/4 × b² × s / 1000     │
│  • วาล์ว (×0.50, ×0.42, ×0.60)  │
│  • B/S Ratio → Long/Square/Over │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────┐
│ เลือกน้ำมัน          │
│  95 / E20 / E85     │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ STEP 2: คำนวณตามน้ำมัน           │
│  • CR (10.5 / 11.5 / 13.0)       │
│  • ห้องเผาไหม้ = cc / (CR − 1)    │
│  • หัวฉีด = cc × (1.0/1.2/1.3)   │
│  • AFR, จุดระเบิด                │
└──────┬───────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ STEP 3: ประมาณกำลัง                  │
│  • BMEP = 900 + (CR−10) × 30         │
│  • kW = BMEP × cc × RPM / 120,000,000│
│  • HP = kW / 0.7457                  │
│  • Torque = 9549 × kW / RPM          │
└──────┬───────────────────────────────┘
       │
       ▼
┌─────────────┐
│   แสดงผล    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    END      │
└─────────────┘
```

## 4. สูตรหลัก (Summary)

| รายการ | สูตร |
|--------|------|
| ความจุกระบอกสูบ | `CC = π/4 × bore² × stroke / 1000` |
| วาล์วไอดี | `bore × 0.50` |
| วาล์วไอเสีย | `bore × 0.42` |
| ลิ้นเร่ง | `bore × 0.60` |
| B/S Ratio | `bore / stroke` |
| ห้องเผาไหม้ | `cc / (CR − 1)` |
| หัวฉีด | `cc × inj_mult` |
| BMEP | `900 + (CR − 10) × 30  kPa` |
| Power | `kW = BMEP × cc × RPM / 120,000,000` |
| Horsepower | `HP = kW / 0.7457` |
| Torque | `Nm = 9549 × kW / RPM` |
