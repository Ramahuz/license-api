import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import hashlib
import json
import os

LICENSE_FILE = "licenses.json"
SECRET_KEY = "rahasia_super"

VERSION_CODE_MAP = {
    "1.0": "A",
    "1.1": "B",
    "2.0": "C"
}
REVERSE_VERSION_CODE_MAP = {v: k for k, v in VERSION_CODE_MAP.items()}

def generate_license(username, version):
    version_code = VERSION_CODE_MAP.get(version, "Z")
    raw = username + version + SECRET_KEY
    full_hash = hashlib.sha256(raw.encode()).hexdigest().upper()
    code = full_hash[:13]
    return f"ra{version_code}{code}"

def save_license(entry):
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

import requests

# Ganti ini dengan URL Replit kamu!
API_URL = "https://license-api.replit.app/verify"

def validate_license_online():
    try:
        with open("user.lic", "r") as f:
            license_data = json.load(f)
    except:
        messagebox.showerror("Gagal", "File user.lic tidak ditemukan atau rusak.")
        return

    try:
        response = requests.post(API_URL, json=license_data)
        result = response.json()
        if result.get("valid"):
            messagebox.showinfo("Sukses", "License valid ✅")
        else:
            messagebox.showwarning("Tidak Valid", "License tidak valid ❌")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal konek ke server:\n{e}")

def on_generate():
    username = entry_user.get().strip()
    version = entry_version.get().strip()
    expired = entry_expired.get().strip()

    if not username or not version:
        messagebox.showerror("Error", "Isi nama user dan versi plugin!")
        return

    license_key = generate_license(username, version)
    result_label.config(text=f"License: {license_key}")

    save_license({
        "username": username,
        "license": license_key,
        "version": version,
        "expired": expired
    })

    # Export ke file .lic
    lic_data = {
        "username": username,
        "license": license_key,
        "version": version,
        "expired": expired
    }

    with open("user.lic", "w") as f:
        json.dump(lic_data, f, indent=4)

    messagebox.showinfo("Berhasil", f"License berhasil dibuat dan disimpan ke user.lic:\n{license_key}")

def show_main_window():
    splash.destroy()
    global entry_user, entry_version, result_label
    root = tk.Tk()
    root.title("RALicense Generator")

    tk.Label(root, text="Nama User:").grid(row=0, column=0, sticky="e")
    entry_user = tk.Entry(root, width=30)
    entry_user.grid(row=0, column=1)

    tk.Label(root, text="Versi Plugin:").grid(row=1, column=0, sticky="e")
    entry_version = tk.Entry(root, width=30)
    entry_version.grid(row=1, column=1)

    tk.Label(root, text="Expired Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e")
    global entry_expired
    entry_expired = tk.Entry(root, width=30)
    entry_expired.grid(row=2, column=1)

    tk.Button(root, text="Generate License", command=on_generate).grid(row=3, column=0, columnspan=2, pady=10)
    result_label = tk.Label(root, text="")
    result_label.grid(row=4, column=0, columnspan=2)

    tk.Button(root, text="Verifikasi License Online", command=validate_license_online).grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()

# === Splash Screen ===
splash = tk.Tk()
splash.overrideredirect(True)

screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
splash_width = 800
splash_height = 800
pos_x = int((screen_width - splash_width) / 2)
pos_y = int((screen_height - splash_height) / 2)
splash.geometry(f"{splash_width}x{splash_height}+{pos_x}+{pos_y}")

# Tampilkan splash image
try:
    image = Image.open("splash.png")
    splash_img = ImageTk.PhotoImage(image)
    img_label = tk.Label(splash, image=splash_img)
    img_label.pack()
except:
    img_label = tk.Label(splash, text="RALicense Generator\nLoading...", font=("Arial", 20))
    img_label.pack(expand=True)

# Label loading animasi titik
loading_label = tk.Label(splash, text="Loading", font=("Arial", 14))
loading_label.pack(pady=10)

# Fungsi untuk animasi titik loading
def animate_loading(count=0):
    dots = "." * (count % 4)
    loading_label.config(text=f"Loading{dots}")
    splash.after(500, animate_loading, count + 1)

animate_loading()

splash.after(2000, show_main_window)
splash.mainloop()
