import csv
import sys
import os
import tkinter as tk
from tkinter import font, PhotoImage

# ---------- EXE kompatibilis elérési út ----------
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# ---------- CSV betöltés ----------
csv_path = os.path.join(application_path, "szamlatukor_adatok.csv")
osztalyok = []

with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        osztalyok.append({
            row["szamlaszam"]: [row["szamlanev_ro"], row["szamlanev_hu"]]
        })

# ---------- GUI ----------
root = tk.Tk()
root.title("Számlanév kereső (Dark Mode)")
root.geometry("550x400")
root.resizable(False, False)
root.configure(bg="#2e2e2e")

# ---------- Ikon betöltése ----------
ikon_path = os.path.join(application_path, "ikon.ico")
try:
    root.iconbitmap(ikon_path)
except Exception as e:
    print("Nem sikerült betölteni az ikont:", e)

# ---------- Betűtípusok ----------
bold_font = font.Font(family="Segoe UI", size=10, weight="bold")
normal_font = font.Font(family="Segoe UI", size=10)

# ---------- Kereső típus választó ----------
search_type = tk.StringVar(value="szam")
frame_radio = tk.Frame(root, bg="#2e2e2e")
frame_radio.pack(pady=5)

tk.Radiobutton(frame_radio, text="Számlaszám (teljes egyezés)", variable=search_type, value="szam",
               bg="#2e2e2e", fg="white", selectcolor="#444444", activebackground="#2e2e2e", activeforeground="white",
               font=normal_font).pack(side=tk.LEFT, padx=5)
tk.Radiobutton(frame_radio, text="Számlanév_RO (részleges egyezés)", variable=search_type, value="nev",
               bg="#2e2e2e", fg="white", selectcolor="#444444", activebackground="#2e2e2e", activeforeground="white",
               font=normal_font).pack(side=tk.LEFT, padx=5)

# ---------- Input és gomb ----------
tk.Label(root, text="Keresett érték:", bg="#2e2e2e", fg="white", font=normal_font).pack(pady=5)
entry = tk.Entry(root, bg="#3c3c3c", fg="white", insertbackground="white", font=normal_font)
entry.pack(pady=5)
tk.Button(root, text="Keresés", command=lambda: keres(), bg="#444444", fg="white",
          activebackground="#555555", activeforeground="white", font=normal_font).pack(pady=5)

# ---------- Frame a Text + Scrollbar-hoz ----------
frame_text = tk.Frame(root, bg="#2e2e2e")
frame_text.pack(pady=10)

text_result = tk.Text(frame_text, height=15, width=50, wrap="word",
                      bg="#3c3c3c", fg="white", insertbackground="white", font=normal_font)
text_result.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame_text, command=text_result.yview, bg="#2e2e2e", troughcolor="#444444")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_result.config(yscrollcommand=scrollbar.set)
text_result.tag_configure("bold", font=bold_font)

# ---------- Kereső függvény ----------
def keres():
    keresett = entry.get().lower()
    text_result.config(state=tk.NORMAL)
    text_result.delete("1.0", tk.END)

    talalatok = 0

    for elem in osztalyok:
        for szam, lista in elem.items():
            if search_type.get() == "szam":
                if keresett == szam.lower():
                    text_result.insert(tk.END, "Számlaszám: ", "bold")
                    text_result.insert(tk.END, f"{szam}\n")
                    text_result.insert(tk.END, "Neve (RO): ", "bold")
                    text_result.insert(tk.END, f"{lista[0]}\n")
                    text_result.insert(tk.END, "Neve (HU): ", "bold")
                    text_result.insert(tk.END, f"{lista[1]}\n")
                    text_result.insert(tk.END, "-"*50 + "\n")
                    talalatok += 1
            else:
                if keresett in lista[0].lower():
                    text_result.insert(tk.END, "Számlaszám: ", "bold")
                    text_result.insert(tk.END, f"{szam}\n")
                    text_result.insert(tk.END, "Neve (RO): ", "bold")
                    text_result.insert(tk.END, f"{lista[0]}\n")
                    text_result.insert(tk.END, "Neve (HU): ", "bold")
                    text_result.insert(tk.END, f"{lista[1]}\n")
                    text_result.insert(tk.END, "-"*50 + "\n")
                    talalatok += 1

    if talalatok == 0:
        text_result.insert(tk.END, f"Nincs találat erre: {keresett}")

    text_result.config(state=tk.DISABLED)

# ---------- Enter billentyű ----------
entry.bind("<Return>", lambda event: keres())

root.mainloop()
