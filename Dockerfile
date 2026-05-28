# Gunakan base image Python yang ringan dan stabil
FROM python:3.9-slim

# Atur working directory di dalam container
WORKDIR /app

# Salin requirements.txt terlebih dahulu agar Docker caching berjalan optimal
COPY rorun/requirements.txt .

# Install dependensi yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh file projek dari komputer ke container
COPY . .

# Ubah working directory ke dalam subfolder rorun agar Flask/Gunicorn
# bisa membaca file python lokal (engine.py, dll) dan aset HTML secara langsung
WORKDIR /app/rorun

# Expose port 7860 yang merupakan port default Hugging Face Spaces
EXPOSE 7860

# Jalankan server menggunakan Gunicorn (production server) agar sangat cepat dan stabil
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app_api:app"]
