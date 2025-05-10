import hashlib
import json
import os

LICENSE_FILE = "licenses.json"
SECRET_KEY = "rahasia_super"

VERSION_CODE_MAP = {
    "1.0": "A",
    "1.1": "B",
    "2.0": "C"
    # Tambah versi di sini
}
REVERSE_VERSION_CODE_MAP = {v: k for k, v in VERSION_CODE_MAP.items()}

def generate_license(username, version):
    version_code = VERSION_CODE_MAP.get(version, "Z")  # fallback 'Z' jika tidak dikenal
    raw = username + version + SECRET_KEY
    full_hash = hashlib.sha256(raw.encode()).hexdigest().upper()
    code = full_hash[:13]  # total panjang = 2 (ra) + 1 (versi) + 13 = 16
    return f"ra{version_code}{code}"

def extract_version_from_license(license_key):
    if not license_key.startswith("ra") or len(license_key) != 16:
        return "invalid"

    version_code = license_key[2]
    return REVERSE_VERSION_CODE_MAP.get(version_code, "unknown")

def load_licenses():
    if not os.path.exists(LICENSE_FILE):
        return []
    with open(LICENSE_FILE, "r") as f:
        return json.load(f)

def save_license(new_entry):
    data = load_licenses()
    data.append(new_entry)
    with open(LICENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ License berhasil disimpan ke licenses.json")

def main():
    username = input("Masukkan nama user: ").strip()
    version = input("Masukkan versi plugin: ").strip()
    license_key = generate_license(username, version)
    version_detected = extract_version_from_license(license_key)

    print(f"\n🔐 License Key     : {license_key}")
    print(f"🧠 Kode versi deteksi: {version_detected}")

    entry = {
        "username": username,
        "license": license_key,
        "version": version
    }
    save_license(entry)

if __name__ == "__main__":
    main()
