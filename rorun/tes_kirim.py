import requests

# Masukkan URL Google Script milikmu yang panjang itu di dalam tanda kutip ini
GOOGLE_URL = "https://script.google.com/macros/s/AKfycbwYx1tGVDkFMMH9nQKTibxVbYOsBT8HfHiKi7GKUYU1faumiZjWPDj8DLuTRSWKm-Vwqg/exec"

data_tes = {
    "nama": "Tester ROrun",
    "usia": 25,
    "status": "Percobaan Sistem"
}

print("Mencoba menembak data ke Google Sheets...")
try:
    # Ingat: allow_redirects=True ini WAJIB untuk Google Script
    response = requests.post(GOOGLE_URL, json=data_tes, allow_redirects=True)
    print(f"Status Code: {response.status_code}")
    print(f"Jawaban Google: {response.text}")
except Exception as e:
    print(f"Gagal total: {e}")