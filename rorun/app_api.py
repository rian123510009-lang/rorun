#!/usr/bin/env python3
# app_api.py
# ─────────────────────────────────────────────────────────────────────────────
# ROrun – Flask API Server
# Digunakan oleh loading.html untuk memanggil analisis engine dan mendapatkan
# hasil jadwal dalam format JSON.
#
# Cara pakai:
#   pip install flask flask-cors
#   python app_api.py
#
# Endpoint:
#   POST /api/analisis   → terima semua data user dari localStorage, return hasil
#   POST /api/jadwal     → terima data hasil analisis + level, return tabel jadwal
#
# Frontend (loading.html) memanggil:
#   1. POST /api/analisis  → simpan hasil ke localStorage
#   2. redirect ke calendar.html
# ─────────────────────────────────────────────────────────────────────────────

import json
import os
import datetime
import threading
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from engine import analisis_pengguna, generate_jadwal

app = Flask(__name__)
CORS(app)  # Izinkan request dari file:// dan localhost

DB_FILE = "database_user.json"


def send_to_google_sheets(url: str, payload: dict):
    """Background task untuk mengirim data ke Google Sheets Web App."""
    try:
        requests.post(url, json=payload, timeout=10, allow_redirects=True)
    except Exception as e:
        print(f"Error sending to Google Sheets: {e}")

def simpan_ke_db(data: dict):
    """
    Simpan data user ke Google Sheets jika GOOGLE_SHEET_WEBAPP_URL diset.
    Jika tidak, simpan ke file JSON lokal (fallback untuk local dev).
    """
    payload = {
        "timestamp": datetime.datetime.now().isoformat(),
        **data
    }

    # Gunakan environment variable jika ada, atau URL hardcode sebagai default untuk lokal
    sheet_url = os.environ.get(
        "GOOGLE_SHEET_WEBAPP_URL",
        "https://script.google.com/macros/s/AKfycbwYx1tGVDkFMMH9nQKTibxVbYOsBT8HfHiKi7GKUYU1faumiZjWPDj8DLuTRSWKm-Vwqg/exec"
    )
    
    if sheet_url:
        # Kirim secara asynchronous agar tidak memblokir response API
        threading.Thread(target=send_to_google_sheets, args=(sheet_url, payload), daemon=True).start()
    else:
        # Fallback ke JSON lokal
        db = []
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    db = json.load(f)
            except Exception:
                db = []
        db.append(payload)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "ROrun API"})


@app.route("/api/analisis", methods=["POST"])
def api_analisis():
    """
    Menerima semua input dari localStorage (dikirim oleh loading.html),
    menjalankan analisis lengkap, dan mengembalikan hasil dalam JSON.
    
    Request body: JSON object dengan semua key dari localStorage
    Response: JSON object berisi hasil analisis lengkap
    """
    try:
        input_data = request.get_json(force=True)
        if not input_data:
            return jsonify({"error": "Request body kosong"}), 400

        hasil = analisis_pengguna(input_data)

        # Simpan ke Database
        try:
            # Hanya simpan tipe data primitif ke spreadsheet
            data_to_save = {k: v for k, v in hasil.items() if not isinstance(v, dict) and not isinstance(v, list)}
            simpan_ke_db(data_to_save)
        except Exception as e:
            print(f"Error calling simpan_ke_db: {e}")

        return jsonify({"success": True, "data": hasil})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jadwal", methods=["POST"])
def api_jadwal():
    """
    Menghasilkan tabel jadwal dari data hasil analisis.
    
    Request body:
        {
            "analisis_data": {...},   ← hasil dari /api/analisis
            "level": "Novice 1",      ← level yang dipilih
            "rp_sec": 390.0           ← race pace yang dipakai
        }
    """
    try:
        body = request.get_json(force=True)
        analisis_data = body.get("analisis_data", {})
        level         = body.get("level", "")
        rp_sec        = float(body.get("rp_sec", 390))

        if not analisis_data or not level:
            return jsonify({"error": "Parameter tidak lengkap"}), 400

        jadwal = generate_jadwal(analisis_data, level, rp_sec)
        return jsonify({"success": True, "jadwal": jadwal})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/jadwal_lengkap", methods=["POST"])
def api_jadwal_lengkap():
    """
    Shortcut: satu endpoint yang mengembalikan semua yang dibutuhkan
    oleh calendar.html — analisis + jadwal utama + jadwal aman (jika dual track).
    
    Request body: JSON object sama seperti /api/analisis
    """
    try:
        input_data = request.get_json(force=True)
        if not input_data:
            return jsonify({"error": "Request body kosong"}), 400

        # Jalankan analisis
        hasil = analisis_pengguna(input_data)

        # Generate jadwal utama
        jadwal_utama = generate_jadwal(hasil, hasil["level"], hasil["rp_sec"])

        # Generate jadwal aman jika dual track
        jadwal_aman = None
        if hasil.get("resiko_ditemukan"):
            jadwal_aman = generate_jadwal(hasil, hasil["level_aman"], hasil["rp_sec_aman"])

        # Simpan ke Database
        try:
            # Hanya simpan tipe data primitif ke spreadsheet
            data_to_save = {k: v for k, v in hasil.items() if not isinstance(v, dict) and not isinstance(v, list)}
            simpan_ke_db(data_to_save)
        except Exception as e:
            print(f"Error calling simpan_ke_db: {e}")

        return jsonify({
            "success":      True,
            "analisis":     hasil,
            "jadwal_utama": jadwal_utama,
            "jadwal_aman":  jadwal_aman,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ─────────────────────────────────────────────────────────────────────────────
# Frontend Static Routing (Untuk hosting terpadu di Hugging Face / Vercel dll)
# ─────────────────────────────────────────────────────────────────────────────

@app.route("/")
def serve_root():
    return send_from_directory("html", "home.html")

@app.route("/assets/<path:path>")
def serve_assets(path):
    return send_from_directory("assets", path)

@app.route("/<path:path>")
def serve_html(path):
    # Jika path adalah file html, kita layani langsung dari folder html
    return send_from_directory("html", path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print("=" * 60)
    print("  ROrun Unified Server")
    print(f"  Berjalan di: http://0.0.0.0:{port}")
    print("  Endpoint:")
    print("    GET  /")
    print("    GET  /api/health")
    print("    POST /api/analisis")
    print("    POST /api/jadwal")
    print("    POST /api/jadwal_lengkap")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=port)