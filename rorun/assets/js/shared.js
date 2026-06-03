// ============================================
// ROrun – shared.js (v2)
// Menyimpan dan mengambil data antar halaman
// ============================================

// Auto-detect API Base URL (Local vs Production/HF Spaces)
const API_BASE = (function() {
  if (window.location.protocol === 'file:' || 
      ((window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') && window.location.port !== '7860')) {
    return 'http://localhost:7860';
  }
  return '';
})();

const AppState = {

  // Simpan satu data
  save(key, value) {
    try {
      localStorage.setItem('rorun_' + key, JSON.stringify(value));
    } catch(e) {
      console.warn('AppState.save error:', e);
    }
  },

  // Ambil satu data
  get(key) {
    try {
      const val = localStorage.getItem('rorun_' + key);
      return val !== null ? JSON.parse(val) : null;
    } catch(e) {
      return null;
    }
  },

  // Ambil semua data rorun sekaligus (flat object, tanpa prefix)
  getAll() {
    const result = {};
    Object.keys(localStorage)
      .filter(k => k.startsWith('rorun_'))
      .forEach(k => {
        const cleanKey = k.replace('rorun_', '');
        try {
          result[cleanKey] = JSON.parse(localStorage.getItem(k));
        } catch(e) {
          result[cleanKey] = localStorage.getItem(k);
        }
      });
    return result;
  },

  // Hapus semua data (untuk reset/mulai ulang)
  clear() {
    Object.keys(localStorage)
      .filter(k => k.startsWith('rorun_'))
      .forEach(k => localStorage.removeItem(k));
  },

  // Hapus satu data spesifik
  remove(key) {
    try {
      localStorage.removeItem('rorun_' + key);
    } catch(e) {
      console.warn('AppState.remove error:', e);
    }
  }

};

// Navigasi ke halaman lain
function goTo(page) {
  window.location.href = page;
}

// ── Fungsi penyimpan tiap step ──────────────────────────────────────────────

/**
 * Step 1: Profil Dasar (nama, usia, tinggi, berat)
 */
function simpanStep1() {
  const nama   = document.getElementById('nama')?.value.trim();
  const usia   = document.getElementById('usia')?.value;
  const tinggi = document.getElementById('tinggi')?.value;
  const berat  = document.getElementById('berat')?.value;

  if (!nama) {
    alert('Nama lengkap wajib diisi!');
    return;
  }
  if (!tinggi || parseFloat(tinggi) <= 0) {
    alert('Masukkan tinggi badan yang valid!');
    return;
  }
  if (!berat || parseFloat(berat) <= 0) {
    alert('Masukkan berat badan yang valid!');
    return;
  }

  AppState.save('nama',   nama);
  AppState.save('usia',   usia ? parseInt(usia) : '');
  AppState.save('tinggi', parseFloat(tinggi));
  AppState.save('berat',  parseFloat(berat));

  goTo('step2.html');
}

/**
 * Step 2: Target Latihan
 */
function simpanStep2() {
  const frekuensi    = document.querySelector('input[name="frequency"]:checked')?.value || '';
  const jarakMingguan= document.getElementById('distance_slider')?.value || 15;
  const targetJarak  = document.querySelector('input[name="race_target"]:checked')?.value || '';
  const modeLat      = document.querySelector('input[name="training_mode"]:checked')?.value || '';
  const targetJam    = document.querySelector('#ambitious_input input[placeholder="0"]')?.value || '0';
  const targetMenit  = document.querySelector('#ambitious_input input[placeholder="45"]')?.value || '0';

  AppState.save('frekuensi',     frekuensi);
  AppState.save('jarak_mingguan',parseFloat(jarakMingguan));
  AppState.save('target_jarak',  targetJarak);
  AppState.save('mode_latihan',  modeLat);
  AppState.save('target_jam',    parseInt(targetJam)   || 0);
  AppState.save('target_menit',  parseInt(targetMenit) || 0);

  goTo('step3.html');
}

/**
 * Step 3: Monitor Detak Jantung
 */
function simpanStep3() {
  const punyaHRM = document.querySelector('input[name="has_hrm"]:checked')?.value || 'no';
  const tahuRHR  = document.querySelector('input[name="knows_rhr"]:checked')?.value || 'no';
  const nilaiRHR = document.getElementById('rhr-input')?.value || '';

  AppState.save('punya_hrm', punyaHRM);
  AppState.save('tahu_rhr',  tahuRHR);
  AppState.save('rhr',       nilaiRHR ? parseInt(nilaiRHR) : '');

  goTo('step4.html');
}

/**
 * Step 4: Riwayat Medis
 */
function simpanStep4() {
  const kardio = document.getElementById('toggle_cardio')?.checked || false;
  const napas  = document.getElementById('toggle_resp')?.checked   || false;
  const cedera = document.getElementById('toggle_injury')?.checked || false;

  const detailKardio = document.querySelector('#details_cardio textarea')?.value || '';
  const detailNapas  = document.querySelector('#details_resp textarea')?.value   || '';
  const detailCedera = document.querySelector('#details_injury textarea')?.value || '';

  AppState.save('riwayat_kardio', kardio);
  AppState.save('riwayat_napas',  napas);
  AppState.save('riwayat_cedera', cedera);
  AppState.save('detail_kardio',  detailKardio);
  AppState.save('detail_napas',   detailNapas);
  AppState.save('detail_cedera',  detailCedera);

  goTo('step5.html');
}

/**
 * Step 5: Personal Best
 * Dipanggil dari tombol Lanjutkan di step5.html
 */
function simpanStep5() {
  const punyaPB  = document.querySelector('input[name="has_pb"]:checked')?.value  || 'tidak';
  const pbJarak  = document.querySelector('input[name="race_category"]:checked')?.value || '';
  const pbJam    = document.getElementById('input-jam')?.value    || '0';
  const pbMenit  = document.getElementById('input-menit')?.value  || '0';
  const pbDetik  = document.getElementById('input-detik')?.value  || '0';

  AppState.save('punya_pb', punyaPB);
  AppState.save('pb_jarak', pbJarak);
  AppState.save('pb_jam',   parseInt(pbJam)   || 0);
  AppState.save('pb_menit', parseInt(pbMenit) || 0);
  AppState.save('pb_detik', parseInt(pbDetik) || 0);

  goTo('step6.html');
}

/**
 * Step 6: Tanggal Lomba & Konfirmasi
 * Dipanggil dari tombol Mulai Analisis di step6.html
 */
function simpanStep6DanAnalisis() {
  const tanggalLomba = document.getElementById('tanggal_lomba')?.value || '';
  const tanggalMulai = document.getElementById('tanggal_mulai')?.value || '';

  if (!tanggalLomba) {
    alert('Pilih tanggal hari H lomba!');
    return;
  }
  if (!tanggalMulai) {
    alert('Pilih tanggal mulai latihan!');
    return;
  }

  AppState.save('tanggal_lomba', tanggalLomba);
  AppState.save('tanggal_mulai', tanggalMulai);

  goTo('loading.html');
}

// ── Helper functions untuk halaman post-analisis ─────────────────────────

/**
 * Format detik ke M:SS/km
 */
function formatPace(totalDetik) {
  if (!totalDetik || totalDetik <= 0) return '-';
  const m = Math.floor(totalDetik / 60);
  const s = Math.floor(totalDetik % 60);
  return m + ':' + String(s).padStart(2, '0');
}

/**
 * Format tanggal ke format Indonesia (contoh: 24 Mei 2026)
 */
function formatTanggalID(dateStr) {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' });
}

/**
 * Hitung selisih hari dari sekarang ke tanggal target
 */
function hitungCountdown(tanggalLomba) {
  if (!tanggalLomba) return 0;
  const now = new Date();
  now.setHours(0,0,0,0);
  const target = new Date(tanggalLomba);
  target.setHours(0,0,0,0);
  return Math.max(0, Math.round((target - now) / 86400000));
}