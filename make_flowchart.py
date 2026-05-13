"""สร้างภาพ flowchart ของ Engine Calculator (ใช้ graphviz)"""
from graphviz import Digraph

g = Digraph("engine_calc", format="png")
g.attr(rankdir="TB", bgcolor="white", fontname="Arial")
g.attr("node", fontname="Arial", fontsize="11")

g.node("start", "START", shape="oval", style="filled", fillcolor="#ff6b00", fontcolor="white")
g.node("input", "Input:\nBore, Stroke, Fuel", shape="parallelogram", style="filled", fillcolor="#e3f2fd")
g.node("check", "Bore > 0 และ\nStroke > 0 ?", shape="diamond", style="filled", fillcolor="#fff3e0")
g.node("err", "แจ้ง Error", shape="box", style="filled", fillcolor="#ffcdd2")

g.node("s1", "STEP 1\nCC = π/4 × b² × s / 1000\nวาล์ว, ลิ้นเร่ง, B/S",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")
g.node("s2", "STEP 2\nเลือก CR, ห้องเผาไหม้,\nหัวฉีด, AFR",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")
g.node("s3", "STEP 3\nHP, Torque, RPM,\nValve Lift",
       shape="box", style="filled,rounded", fillcolor="#fff3e0")

g.node("out", "แสดงผล", shape="parallelogram", style="filled", fillcolor="#e8f5e9")
g.node("end", "END", shape="oval", style="filled", fillcolor="#424242", fontcolor="white")

g.edge("start", "input")
g.edge("input", "check")
g.edge("check", "err", label="No")
g.edge("err", "input")
g.edge("check", "s1", label="Yes")
g.edge("s1", "s2")
g.edge("s2", "s3")
g.edge("s3", "out")
g.edge("out", "end")

out = g.render("flowchart", cleanup=True)
print("Saved:", out)
