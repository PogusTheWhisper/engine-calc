"""สร้างภาพ flowchart ของ Engine Calculator (graphviz)"""
from graphviz import Digraph

g = Digraph("engine_calc", format="png")
g.attr(rankdir="TB", bgcolor="white", fontname="Arial", splines="ortho")
g.attr("node", fontname="Arial", fontsize="11")

# ─── โหนด ──────────────────────────────────────────────
g.node("start", "START", shape="oval",
       style="filled", fillcolor="#ff6b00", fontcolor="white", fontsize="13")

g.node("in1", "Input:\nBore, Stroke (mm)", shape="parallelogram",
       style="filled", fillcolor="#e3f2fd")

g.node("chk1", "Bore > 0 และ\nStroke > 0 ?", shape="diamond",
       style="filled", fillcolor="#fff8e1")
g.node("err1", "แจ้ง Error", shape="box",
       style="filled", fillcolor="#ffcdd2")

# STEP 1
g.node("s1", "STEP 1 — ข้อมูลเครื่องยนต์\l"
             "• CC = π/4 × bore² × stroke / 1000\l"
             "• วาล์วไอดี   = bore × 0.50\l"
             "• วาล์วไอเสีย = bore × 0.42\l"
             "• ลิ้นเร่ง     = bore × 0.60\l"
             "• B/S Ratio = bore / stroke\l",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")

g.node("bs", "ประเภทเครื่อง", shape="diamond",
       style="filled", fillcolor="#fff8e1")
g.node("bs_long",   "Long Stroke\n(B/S < 0.9)",  shape="box", style="filled", fillcolor="#bbdefb")
g.node("bs_sq",     "Square\n(0.9 ≤ B/S ≤ 1.1)", shape="box", style="filled", fillcolor="#c8e6c9")
g.node("bs_over",   "Over Square\n(B/S > 1.1)",  shape="box", style="filled", fillcolor="#ffe0b2")

# STEP 2 — fuel
g.node("in2", "เลือกน้ำมัน\n(95 / E20 / E85)", shape="parallelogram",
       style="filled", fillcolor="#e3f2fd")
g.node("chk2", "เลือกแล้ว ?", shape="diamond",
       style="filled", fillcolor="#fff8e1")
g.node("err2", "แจ้ง Error", shape="box",
       style="filled", fillcolor="#ffcdd2")

g.node("s2", "STEP 2 — น้ำมัน\l"
             "• 95  → CR 10.5, inj × 1.0\l"
             "• E20 → CR 11.5, inj × 1.2\l"
             "• E85 → CR 13.0, inj × 1.3\l"
             "• ห้องเผาไหม้ = cc / (CR − 1)\l"
             "• หัวฉีด = cc × inj_mult\l",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")

# STEP 3 — power
g.node("s3", "STEP 3 — ประมาณกำลัง\l"
             "• BMEP = 900 + (CR − 10) × 30\l"
             "• kW = BMEP × cc × RPM / 120,000,000\l"
             "• HP = kW / 0.7457\l"
             "• Torque = 9549 × kW / RPM\l",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")

g.node("out", "แสดงผล\nHP, Torque, RPM,\nCam, Valve Lift",
       shape="parallelogram", style="filled", fillcolor="#e8f5e9")
g.node("end", "END", shape="oval",
       style="filled", fillcolor="#424242", fontcolor="white", fontsize="13")

# ─── เส้น ─────────────────────────────────────────────
g.edge("start", "in1")
g.edge("in1", "chk1")
g.edge("chk1", "err1", label="No")
g.edge("err1", "in1")
g.edge("chk1", "s1", label="Yes")
g.edge("s1", "bs")
g.edge("bs", "bs_long",  label="< 0.9")
g.edge("bs", "bs_sq",    label="0.9–1.1")
g.edge("bs", "bs_over",  label="> 1.1")
g.edge("bs_long", "in2")
g.edge("bs_sq",   "in2")
g.edge("bs_over", "in2")
g.edge("in2", "chk2")
g.edge("chk2", "err2", label="No")
g.edge("err2", "in2")
g.edge("chk2", "s2", label="Yes")
g.edge("s2", "s3")
g.edge("s3", "out")
g.edge("out", "end")

out = g.render("flowchart", cleanup=True)
print("Saved:", out)
