import csv
import os

LOG_FILE = r"C:\Users\gwert\_itmo\электротехника\лабы\lab3\2_9.log"
OUT_FILE = "results.csv"

vals = {}

with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if line.startswith("i_rms:"):
            # i_rms: RMS(-I(V1))=0.600931285769 FROM 0 TO 0.02
            part = line.split("=", 1)[1].split()[0]
            vals["i_rms"] = round(float(part), 3)
        elif line.startswith("i1_rms:"):
            part = line.split("=", 1)[1].split()[0]
            vals["i1_rms"] = round(float(part), 3)
        elif line.startswith("i2_rms:"):
            part = line.split("=", 1)[1].split()[0]
            vals["i2_rms"] = round(float(part), 3)

required = ["i_rms", "i1_rms", "i2_rms"]
if not all(k in vals for k in required):
    print("❌ В логе нет всех трёх RMS (i_rms, i1_rms, i2_rms)")
    print("Нашёл:", vals)
    raise SystemExit

row = [vals[k] for k in required]

# Собираем уже существующие строки, чтобы избежать дублей
existing_rows = set()
if os.path.exists(OUT_FILE):
    with open(OUT_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for r in reader:
            existing_rows.add(tuple(r))

row_str = tuple(map(str, row))

if row_str in existing_rows:
    print("⚠ Такие значения уже есть, запись пропущена:", row)
else:
    write_header = not os.path.exists(OUT_FILE)
    with open(OUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        if write_header:
            writer.writerow(["I", "I1", "I2"])
        writer.writerow(row)
    print("✅ Добавлено в results.csv:", row)
