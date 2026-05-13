"""Engine Calculator — Tkinter GUI (สูบเดี่ยว)"""

import math
import tkinter as tk
from tkinter import ttk, messagebox

# ─── ตารางน้ำมัน ─────────────────────────────────────────────
FUEL = {
    "Gasohol 95": {"cr": 10.5, "afr": 14.7, "inj": 1.0, "ign": 34},
    "E20":        {"cr": 11.5, "afr": 13.8, "inj": 1.2, "ign": 35},
    "E85":        {"cr": 13.0, "afr":  9.8, "inj": 1.3, "ign": 38},
}

# ─── ฟังก์ชันคำนวณ ───────────────────────────────────────────
def cc_of(bore, stroke):
    return math.pi / 4 * bore**2 * stroke / 1000

def bs_char(bore, stroke):
    r = bore / stroke
    if r < 0.9:  return r, "Long Stroke"
    if r > 1.1:  return r, "Over Square"
    return r, "Square"

def performance(cc, bore, stroke, cr):
    r = bore / stroke
    rpm  = 11000 if r > 1.05 else 8000 if r < 0.9 else 9500
    lift = bore * (0.28 if r > 1.05 else 0.24 if r < 0.9 else 0.26)
    bmep = 900 + (cr - 10) * 30
    kw   = bmep * cc * rpm / 120_000_000
    return {
        "hp":     kw / 0.7457,
        "torque": 9549 * kw / rpm,
        "rpm":    rpm,
        "lift":   lift,
    }

# ─── GUI ─────────────────────────────────────────────────────
def calculate():
    try:
        bore   = float(e_bore.get())
        stroke = float(e_stroke.get())
        fuel   = fuel_var.get()
        if bore <= 0 or stroke <= 0 or fuel not in FUEL:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "กรอกข้อมูลให้ครบและถูกต้อง")
        return

    cc = cc_of(bore, stroke)
    r, name = bs_char(bore, stroke)
    f = FUEL[fuel]
    chamber  = cc / (f["cr"] - 1)
    injector = cc * f["inj"]
    p = performance(cc, bore, stroke, f["cr"])

    result.config(text=(
        f"━━ STEP 1 — เครื่องยนต์ ━━\n"
        f"CC                : {cc:8.2f} cc\n"
        f"วาล์วไอดี          : {bore*0.50:8.1f} mm\n"
        f"วาล์วไอเสีย        : {bore*0.42:8.1f} mm\n"
        f"ลิ้นเร่ง            : {bore*0.60:8.1f} mm\n"
        f"B/S Ratio          : {r:8.3f}  ({name})\n\n"
        f"━━ STEP 2 — น้ำมัน {fuel} ━━\n"
        f"กำลังอัด           : {f['cr']}:1\n"
        f"ห้องเผาไหม้        : {chamber:8.2f} cc\n"
        f"หัวฉีด             : {injector:8.0f} cc/min\n"
        f"AFR                : {f['afr']}:1\n"
        f"จุดระเบิด          : {f['ign']}° BTDC\n\n"
        f"━━ STEP 3 — กำลัง (ประมาณ) ━━\n"
        f"HP                 : {p['hp']:8.2f} HP\n"
        f"แรงบิด             : {p['torque']:8.2f} Nm\n"
        f"รอบพลัง            : {p['rpm']:>8,} RPM\n"
        f"Valve Lift แนะนำ   : {p['lift']:8.1f} mm"
    ))

root = tk.Tk()
root.title("Engine Calculator")
root.configure(bg="#0a0c0f")

tk.Label(root, text="ENGINE CALC", bg="#0a0c0f", fg="#ff6b00",
         font=("Arial", 16, "bold")).pack(pady=(12, 8))

form = tk.Frame(root, bg="#0a0c0f")
form.pack(padx=20, pady=4)

tk.Label(form, text="Bore (mm):",   bg="#0a0c0f", fg="#fff").grid(row=0, column=0, sticky="e", pady=4)
e_bore = tk.Entry(form, width=14); e_bore.grid(row=0, column=1, padx=8)

tk.Label(form, text="Stroke (mm):", bg="#0a0c0f", fg="#fff").grid(row=1, column=0, sticky="e", pady=4)
e_stroke = tk.Entry(form, width=14); e_stroke.grid(row=1, column=1, padx=8)

tk.Label(form, text="น้ำมัน:",       bg="#0a0c0f", fg="#fff").grid(row=2, column=0, sticky="e", pady=4)
fuel_var = tk.StringVar()
ttk.Combobox(form, textvariable=fuel_var, values=list(FUEL.keys()),
             state="readonly", width=12).grid(row=2, column=1, padx=8)

tk.Button(root, text="คำนวณ", bg="#ff6b00", fg="#fff", relief="flat",
          font=("Arial", 11, "bold"), command=calculate).pack(fill="x", padx=20, pady=10)

result = tk.Label(root, text="", bg="#111418", fg="#e0e0e0",
                  font=("Courier", 10), justify="left", anchor="w", padx=12, pady=10)
result.pack(fill="both", expand=True, padx=20, pady=(0, 16))

root.mainloop()
