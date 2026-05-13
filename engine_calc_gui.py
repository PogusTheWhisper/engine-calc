"""
Engine Calculator — Tkinter GUI
================================
เครื่องคำนวณสเปคเครื่องยนต์สูบเดี่ยว สำหรับงานแต่ง
- STEP 1: คำนวณ CC, วาล์ว, ลิ้นเร่ง, B/S Ratio
- STEP 2: เลือกน้ำมัน → กำลังอัด, ห้องเผาไหม้, หัวฉีด, AFR
- STEP 3: ประมาณ HP, แรงบิด, RPM, Cam, Valve Lift
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox


# ─── ฟังก์ชันคำนวณ (Pure functions) ───────────────────────────────────────────

def calc_displacement(bore_mm, stroke_mm):
    """ความจุกระบอกสูบ (cc) = π/4 × bore² × stroke / 1000"""
    return (math.pi / 4) * (bore_mm ** 2) * stroke_mm / 1000


def calc_valves(bore_mm):
    """ขนาดวาล์ว/ลิ้นเร่ง ตามสูตรช่างแต่ง"""
    return {
        "intake":   bore_mm * 0.50,   # วาล์วไอดี
        "exhaust":  bore_mm * 0.42,   # วาล์วไอเสีย
        "throttle": bore_mm * 0.60,   # ลิ้นเร่ง
    }


def classify_bs_ratio(bore_mm, stroke_mm):
    """จัดประเภทเครื่องตามค่า B/S Ratio"""
    r = bore_mm / stroke_mm
    if r < 0.9:
        return r, "Long Stroke", "แรงบิดต่ำรอบ เหมาะสายบ้าน"
    if r > 1.1:
        return r, "Over Square", "รอบสูงได้ดี เหมาะสายซิ่ง"
    return r, "Square", "สมดุล ใช้ได้ทั่วไป"


# ตารางคุณสมบัติน้ำมัน — รถซิ่งใช้ 3 ตัวนี้
FUEL_SPECS = {
    "Gasohol 95": {"cr": 10.5, "afr": 14.7, "inj_mult": 1.0, "ign": 34},
    "E20":        {"cr": 11.5, "afr": 13.8, "inj_mult": 1.2, "ign": 35},
    "E85":        {"cr": 13.0, "afr":  9.8, "inj_mult": 1.3, "ign": 38},
}


def calc_fuel(cc, fuel_name):
    """กำลังอัด, ห้องเผาไหม้, หัวฉีด, AFR"""
    s = FUEL_SPECS[fuel_name]
    return {
        "cr":       s["cr"],
        "chamber":  cc / (s["cr"] - 1),
        "injector": cc * s["inj_mult"],
        "afr":      s["afr"],
        "ignition": s["ign"],
    }


def calc_performance(cc, bore_mm, stroke_mm, cr):
    """
    ประมาณกำลัง 4-stroke
    P(kW) = BMEP_kPa × cc × RPM / 120,000,000
    HP    = P(kW) / 0.7457
    T(Nm) = 9549 × P(kW) / RPM
    """
    bs = bore_mm / stroke_mm
    if bs > 1.05:
        rpm, cam, lift_mult = 11000, "270-285°", 0.28
    elif bs < 0.90:
        rpm, cam, lift_mult =  8000, "250-260°", 0.24
    else:
        rpm, cam, lift_mult =  9500, "260-270°", 0.26

    bmep_kpa = 900 + (cr - 10) * 30
    kw = (bmep_kpa * cc * rpm) / 120_000_000
    hp = kw / 0.7457
    torque = (9549 * kw) / rpm

    return {
        "hp": hp,
        "torque": torque,
        "rpm": rpm,
        "cam": cam,
        "lift": bore_mm * lift_mult,
    }


# ─── GUI ──────────────────────────────────────────────────────────────────────

class EngineCalcApp:
    BG     = "#0a0c0f"
    CARD   = "#111418"
    BORDER = "#1e2530"
    ORANGE = "#ff6b00"
    TEXT   = "#e0e0e0"
    MUTED  = "#5a6a7a"

    def __init__(self, root):
        self.root = root
        self.root.title("Engine Calculator — Advanced Tuning")
        self.root.configure(bg=self.BG)
        self.root.geometry("780x780")

        self.cc = None             # เก็บผล Step 1 ไว้ให้ Step 2 ใช้
        self.bore = None
        self.stroke = None

        self._build_header()
        self._build_step1()
        self._build_step2()
        self._build_step3()
        self._build_footer()

    # ── helpers ──
    def _label(self, parent, text, **kw):
        return tk.Label(parent, text=text, bg=self.CARD, fg=self.TEXT, **kw)

    def _card(self, title, step_no):
        frame = tk.Frame(self.root, bg=self.CARD, bd=1, relief="solid",
                         highlightbackground=self.BORDER, highlightthickness=1)
        frame.pack(fill="x", padx=20, pady=8)
        header = tk.Frame(frame, bg=self.CARD)
        header.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(header, text=title, bg=self.CARD, fg=self.ORANGE,
                 font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(header, text=f"STEP 0{step_no}", bg=self.CARD,
                 fg=self.MUTED, font=("Courier", 9)).pack(side="right")
        return frame

    # ── Header ──
    def _build_header(self):
        h = tk.Frame(self.root, bg=self.BG)
        h.pack(pady=(16, 8))
        tk.Label(h, text="ENGINE CALC", bg=self.BG, fg=self.TEXT,
                 font=("Arial", 18, "bold")).pack()
        tk.Label(h, text="Advanced Tuning Calculator · Single Cylinder",
                 bg=self.BG, fg=self.MUTED, font=("Arial", 9)).pack()

    # ── STEP 1 ──
    def _build_step1(self):
        f = self._card("⬤ ข้อมูลเครื่องยนต์", 1)

        body = tk.Frame(f, bg=self.CARD)
        body.pack(fill="x", padx=12, pady=6)

        tk.Label(body, text="ลูกสูบ (Bore) mm:", bg=self.CARD, fg=self.MUTED).grid(row=0, column=0, sticky="w", pady=4)
        self.entry_bore = tk.Entry(body, width=12, bg="#000", fg="#fff", insertbackground="#fff")
        self.entry_bore.grid(row=0, column=1, padx=8)

        tk.Label(body, text="ช่วงชัก (Stroke) mm:", bg=self.CARD, fg=self.MUTED).grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.entry_stroke = tk.Entry(body, width=12, bg="#000", fg="#fff", insertbackground="#fff")
        self.entry_stroke.grid(row=0, column=3, padx=8)

        tk.Button(f, text="คำนวณ STEP 1", bg=self.ORANGE, fg="#fff",
                  font=("Arial", 10, "bold"), relief="flat",
                  command=self.run_step1).pack(fill="x", padx=12, pady=(4, 8))

        self.label_step1 = tk.Label(f, text="", bg=self.CARD, fg=self.TEXT,
                                    font=("Courier", 10), justify="left", anchor="w")
        self.label_step1.pack(fill="x", padx=12, pady=(0, 10))

    # ── STEP 2 ──
    def _build_step2(self):
        f = self._card("☁ เลือกน้ำมันเชื้อเพลิง", 2)

        row = tk.Frame(f, bg=self.CARD)
        row.pack(fill="x", padx=12, pady=6)
        tk.Label(row, text="ชนิดน้ำมัน:", bg=self.CARD, fg=self.MUTED).pack(side="left")

        self.fuel_var = tk.StringVar()
        self.fuel_dropdown = ttk.Combobox(row, textvariable=self.fuel_var,
                                          values=list(FUEL_SPECS.keys()),
                                          state="readonly", width=18)
        self.fuel_dropdown.pack(side="left", padx=10)

        tk.Button(f, text="คำนวณ STEP 2", bg=self.ORANGE, fg="#fff",
                  font=("Arial", 10, "bold"), relief="flat",
                  command=self.run_step2).pack(fill="x", padx=12, pady=(4, 8))

        self.label_step2 = tk.Label(f, text="", bg=self.CARD, fg=self.TEXT,
                                    font=("Courier", 10), justify="left", anchor="w")
        self.label_step2.pack(fill="x", padx=12, pady=(0, 10))

    # ── STEP 3 ──
    def _build_step3(self):
        f = self._card("⚡ ประมาณกำลัง & จุดระเบิด", 3)
        self.label_step3 = tk.Label(f, text="(คำนวณ Step 1 และ 2 ก่อน)",
                                    bg=self.CARD, fg=self.MUTED,
                                    font=("Courier", 10), justify="left", anchor="w")
        self.label_step3.pack(fill="x", padx=12, pady=10)

    # ── Footer ──
    def _build_footer(self):
        tk.Label(self.root,
                 text="⚙ ค่าที่แสดงเป็นค่าประมาณ · ใช้เป็นแนวทาง · ปรึกษาช่างก่อนแต่งจริง",
                 bg=self.BG, fg=self.MUTED, font=("Arial", 8)).pack(pady=8)

    # ── Actions ──
    def run_step1(self):
        try:
            bore = float(self.entry_bore.get())
            stroke = float(self.entry_stroke.get())
            if bore <= 0 or stroke <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "กรุณากรอกตัวเลข Bore/Stroke ให้ถูกต้อง")
            return

        self.bore, self.stroke = bore, stroke
        self.cc = calc_displacement(bore, stroke)
        v = calc_valves(bore)
        r, name, note = classify_bs_ratio(bore, stroke)

        self.label_step1.config(text=(
            f"ความจุกระบอกสูบ : {self.cc:>8.2f} cc\n"
            f"วาล์วไอดี        : {v['intake']:>8.1f} mm\n"
            f"วาล์วไอเสีย      : {v['exhaust']:>8.1f} mm\n"
            f"ลิ้นเร่ง          : {v['throttle']:>8.1f} mm\n"
            f"B/S Ratio        : {r:>8.3f}  ({name})\n"
            f"  → {note}"
        ))
        self.label_step2.config(text="")
        self.label_step3.config(text="(เลือกน้ำมัน แล้วกด STEP 2)", fg=self.MUTED)

    def run_step2(self):
        if self.cc is None:
            messagebox.showerror("Error", "กรุณาคำนวณ STEP 1 ก่อน")
            return
        fuel = self.fuel_var.get()
        if not fuel:
            messagebox.showerror("Error", "กรุณาเลือกชนิดน้ำมัน")
            return

        f = calc_fuel(self.cc, fuel)
        self.label_step2.config(text=(
            f"น้ำมัน          : {fuel}\n"
            f"กำลังอัด        : {f['cr']}:1\n"
            f"ห้องเผาไหม้     : {f['chamber']:>8.2f} cc\n"
            f"หัวฉีด          : {f['injector']:>8.0f} cc/min\n"
            f"AFR (Stoich)    : {f['afr']}:1\n"
            f"จุดระเบิด       : {f['ignition']}° BTDC"
        ))

        # Step 3 ต่อทันที
        p = calc_performance(self.cc, self.bore, self.stroke, f["cr"])
        self.label_step3.config(text=(
            f"กำลัง (HP)      : {p['hp']:>8.2f} HP\n"
            f"แรงบิด          : {p['torque']:>8.2f} Nm\n"
            f"รอบพลัง         : {p['rpm']:>8,} RPM\n"
            f"Cam Duration    : {p['cam']}\n"
            f"Valve Lift แนะนำ: {p['lift']:>8.1f} mm"
        ), fg=self.TEXT)


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = EngineCalcApp(root)
    root.mainloop()