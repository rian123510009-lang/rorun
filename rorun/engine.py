import datetime
from database_jadwal import hal_higdon_db

# ─────────────────────────────────────────────
# DATA: VDOT TABLE (seconds)
# ─────────────────────────────────────────────
_VDOT_TABLE = {
    30: {"5k": 1927, "10k": 4008, "hm": 8880, "fm": 18598},
    31: {"5k": 1870, "10k": 3890, "hm": 8625, "fm": 17992},
    32: {"5k": 1818, "10k": 3779, "hm": 8384, "fm": 17421},
    33: {"5k": 1769, "10k": 3674, "hm": 8156, "fm": 16882},
    34: {"5k": 1723, "10k": 3574, "hm": 7939, "fm": 16374},
    35: {"5k": 1680, "10k": 3480, "hm": 7733, "fm": 15894},
    36: {"5k": 1639, "10k": 3391, "hm": 7536, "fm": 15440},
    37: {"5k": 1601, "10k": 3306, "hm": 7349, "fm": 15010},
    38: {"5k": 1565, "10k": 3226, "hm": 7170, "fm": 14603},
    39: {"5k": 1531, "10k": 3150, "hm": 7000, "fm": 14215},
    40: {"5k": 1498, "10k": 3078, "hm": 6836, "fm": 13846},
    41: {"5k": 1467, "10k": 3009, "hm": 6680, "fm": 13494},
    42: {"5k": 1438, "10k": 2944, "hm": 6531, "fm": 13158},
    43: {"5k": 1410, "10k": 2882, "hm": 6387, "fm": 12837},
    44: {"5k": 1383, "10k": 2823, "hm": 6249, "fm": 12530},
    45: {"5k": 1358, "10k": 2767, "hm": 6117, "fm": 12237},
    46: {"5k": 1334, "10k": 2714, "hm": 5990, "fm": 11956},
    47: {"5k": 1310, "10k": 2663, "hm": 5868, "fm": 11688},
    48: {"5k": 1288, "10k": 2614, "hm": 5751, "fm": 11430},
    49: {"5k": 1267, "10k": 2568, "hm": 5638, "fm": 11183},
    50: {"5k": 1246, "10k": 2524, "hm": 5530, "fm": 10946},
    51: {"5k": 1227, "10k": 2481, "hm": 5426, "fm": 10718},
    52: {"5k": 1208, "10k": 2441, "hm": 5326, "fm": 10499},
    53: {"5k": 1190, "10k": 2402, "hm": 5229, "fm": 10289},
    54: {"5k": 1173, "10k": 2365, "hm": 5136, "fm": 10086},
    55: {"5k": 1156, "10k": 2330, "hm": 5046, "fm": 9891},
    56: {"5k": 1140, "10k": 2296, "hm": 4959, "fm": 9703},
    57: {"5k": 1124, "10k": 2263, "hm": 4875, "fm": 9522},
    58: {"5k": 1109, "10k": 2232, "hm": 4794, "fm": 9347},
    59: {"5k": 1095, "10k": 2202, "hm": 4716, "fm": 9179},
    60: {"5k": 1081, "10k": 2173, "hm": 4640, "fm": 9017},
}

# Training paces per VDOT (seconds/km)
TRAINING_PACES = {
    30: {"easy_min": 463, "easy_max": 520, "marathon": 441, "threshold": 406, "interval": 374, "rep": 345},
    35: {"easy_min": 399, "easy_max": 447, "marathon": 377, "threshold": 347, "interval": 320, "rep": 295},
    40: {"easy_min": 349, "easy_max": 390, "marathon": 328, "threshold": 302, "interval": 277, "rep": 256},
    45: {"easy_min": 308, "easy_max": 344, "marathon": 289, "threshold": 265, "interval": 244, "rep": 225},
    50: {"easy_min": 274, "easy_max": 306, "marathon": 259, "threshold": 235, "interval": 217, "rep": 200},
    55: {"easy_min": 246, "easy_max": 275, "marathon": 234, "threshold": 211, "interval": 195, "rep": 179},
    60: {"easy_min": 223, "easy_max": 248, "marathon": 213, "threshold": 190, "interval": 175, "rep": 161},
}

PLAN_MIN_WEEKS = {
    "5K Novice": 8, "5K Intermediate": 8, "5K Advanced": 8,
    "10K Novice": 8, "10K Intermediate": 8, "10K Advanced": 8,
    "HM Novice 1": 12, "HM Novice 2": 12, "HM Intermediate 1": 12,
    "HM Intermediate 2": 12, "HM Advanced": 12, "HM3": 12,
    "FM Novice 1": 18, "FM Novice 2": 18, "FM Intermediate 1": 18,
    "FM Intermediate 2": 18, "FM Advanced 1": 18, "FM Advanced 2": 18,
    "Marathon 3": 24, "FM Senior Program": 8,
    "Base Training (Walk/Jog)": 4, "Rest / Fisioterapi": 1,
}

PLAN_ORDER_5K = ["5K Novice", "5K Intermediate", "5K Advanced"]
PLAN_ORDER_10K = ["10K Novice", "10K Intermediate", "10K Advanced"]
PLAN_ORDER_HM = ["HM Novice 1", "HM Novice 2", "HM3", "HM Intermediate 1", "HM Intermediate 2", "HM Advanced"]
PLAN_ORDER_FM = ["FM Novice 1", "FM Novice 2", "Marathon 3", "FM Intermediate 1", "FM Intermediate 2", "FM Advanced 1", "FM Advanced 2"]

# Konfigurasi mapping level ke DB
# Format nama di return value select_plan -> [top level key, plan key]
DB_MAP = {
    "5K Novice": ["5K", "Novice"],
    "5K Intermediate": ["5K", "Intermediate"],
    "5K Advanced": ["5K", "Advanced"],
    "10K Novice": ["10K", "Novice"],
    "10K Intermediate": ["10K", "Intermediate"],
    "10K Advanced": ["10K", "Advanced"],
    "HM Novice 1": ["Half Marathon", "Novice 1"],
    "HM Novice 2": ["Half Marathon", "Novice 2"],
    "HM Intermediate 1": ["Half Marathon", "Intermediate 1"],
    # HM Intermediate 2 -> fallback ke HM Advanced krn tidak ada
    "HM Intermediate 2": ["Half Marathon", "Advanced"], 
    "HM Advanced": ["Half Marathon", "Advanced"],
    "HM3": ["Half Marathon", "HM3"],
    "FM Novice 1": ["Marathon", "Novice 1"],
    "FM Novice 2": ["Marathon", "Novice 2"],
    # FM Intermediate 1 -> fallback ke FM Intermediate 2 krn tidak ada
    "FM Intermediate 1": ["Marathon", "Intermediate 2"],
    "FM Intermediate 2": ["Marathon", "Intermediate 2"],
    "FM Advanced 1": ["Marathon", "Advanced 1"],
    "FM Advanced 2": ["Marathon", "Advanced 2"],
    "Marathon 3": ["Marathon", "Marathon 3"],
    "FM Senior Program": ["Marathon", "Senior Program"],
}

NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

TARGET_JARAK_MAP = {
    "5k":  "5K",
    "10k": "10K",
    "hm":  "Half Marathon",
    "fm":  "Marathon",
}
JARAK_KE_KM = {"5K": 5.0, "10K": 10.0, "Half Marathon": 21.1, "Marathon": 42.2}

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def format_waktu(total_detik: float) -> str:
    if total_detik <= 0: return "Sprint"
    m, s = divmod(int(total_detik), 60)
    return f"{m}:{s:02d}/km"

def vdot_from_time(dist, total_secs):
    best_v, best_diff = 30.0, float("inf")
    # First exact match or closest
    for v, t in _VDOT_TABLE.items():
        if dist in t:
            d = abs(t[dist] - total_secs)
            if d < best_diff:
                best_diff, best_v = d, v
    
    # Interpolate
    vdots = sorted(_VDOT_TABLE.keys())
    for i in range(len(vdots)-1):
        v_lo, v_hi = vdots[i], vdots[i+1]
        t_lo, t_hi = _VDOT_TABLE[v_lo].get(dist, 99999), _VDOT_TABLE[v_hi].get(dist, 0)
        # Note: as vdot increases, time decreases. so t_hi < t_lo
        if t_hi <= total_secs <= t_lo:
            frac = (t_lo - total_secs) / max(1, t_lo - t_hi)
            best_v = v_lo + frac * (v_hi - v_lo)
            break
            
    return round(best_v, 1)

def projected_vdot(current, weeks):
    if weeks <= 8:   gain = 2.5
    elif weeks <= 12: gain = 3.5
    elif weeks <= 18: gain = 5.0
    else:            gain = 6.5
    return current + gain

def race_time_from_vdot(vdot, dist):
    vdots = sorted(_VDOT_TABLE.keys())
    if vdot <= vdots[0]:  return _VDOT_TABLE[vdots[0]].get(dist, 0)
    if vdot >= vdots[-1]: return _VDOT_TABLE[vdots[-1]].get(dist, 0)
    lo = max(v for v in vdots if v <= vdot)
    hi = min(v for v in vdots if v >= vdot)
    if lo == hi: return _VDOT_TABLE[lo].get(dist, 0)
    r = (vdot - lo) / (hi - lo)
    t_lo, t_hi = _VDOT_TABLE[lo].get(dist, 0), _VDOT_TABLE[hi].get(dist, 0)
    return t_lo + r * (t_hi - t_lo)

def interp_paces(vdot):
    keys = sorted(TRAINING_PACES.keys())
    if vdot <= keys[0]:  return TRAINING_PACES[keys[0]]
    if vdot >= keys[-1]: return TRAINING_PACES[keys[-1]]
    lo = max(k for k in keys if k <= vdot)
    hi = min(k for k in keys if k >= vdot)
    if lo == hi: return TRAINING_PACES[lo]
    r = (vdot - lo) / (hi - lo)
    return {k: TRAINING_PACES[lo][k] + r * (TRAINING_PACES[hi][k] - TRAINING_PACES[lo][k])
            for k in TRAINING_PACES[lo]}

def downgrade_plan(plan, levels):
    for order in [PLAN_ORDER_5K, PLAN_ORDER_10K, PLAN_ORDER_HM, PLAN_ORDER_FM]:
        if plan in order:
            idx = max(0, order.index(plan) - levels)
            return order[idx]
    return plan

def select_plan(dist, freq, speed, target, weeks):
    """Returns (safe_plan, ambitious_plan_or_None, needs_dual)"""
    if freq == "F1":
        amb_plan_result = select_plan(dist, "F2", speed, target, weeks)
        amb_plan = amb_plan_result[1] if amb_plan_result[1] else amb_plan_result[0]
        return "Base Training (Walk/Jog)", amb_plan, True

    use_m3 = (dist == "fm" and weeks >= 24)

    matrix = {
        # ── 5K ──────────────────────────────────────────────────────
        ("5k","F2","S0","T1"): ("5K Novice", None, False),
        ("5k","F2","S0","T2"): ("5K Novice", None, False),
        ("5k","F2","S0","T3"): ("5K Novice", "5K Intermediate", True),
        ("5k","F2","S1","T1"): ("5K Novice", None, False),
        ("5k","F2","S1","T2"): ("5K Novice", None, False),
        ("5k","F2","S1","T3"): ("5K Novice", "5K Intermediate", True),
        ("5k","F2","S2","T1"): ("5K Novice", None, False),
        ("5k","F2","S2","T2"): ("5K Intermediate", None, False),
        ("5k","F2","S2","T3"): ("5K Intermediate", "5K Advanced", True),
        ("5k","F3","S0","T1"): ("5K Novice", None, False),
        ("5k","F3","S0","T2"): ("5K Novice", None, False),
        ("5k","F3","S0","T3"): ("5K Novice", "5K Intermediate", True),
        ("5k","F3","S1","T1"): ("5K Novice", None, False),
        ("5k","F3","S1","T2"): ("5K Intermediate", None, False),
        ("5k","F3","S1","T3"): ("5K Intermediate", "5K Advanced", True),
        ("5k","F3","S2","T1"): ("5K Intermediate", None, False),
        ("5k","F3","S2","T2"): ("5K Intermediate", None, False),
        ("5k","F3","S2","T3"): ("5K Advanced", None, False),
        ("5k","F4","S0","T1"): ("5K Intermediate", None, False),
        ("5k","F4","S0","T2"): ("5K Intermediate", None, False),
        ("5k","F4","S0","T3"): ("5K Intermediate", "5K Advanced", True),
        ("5k","F4","S1","T1"): ("5K Intermediate", None, False),
        ("5k","F4","S1","T2"): ("5K Intermediate", None, False),
        ("5k","F4","S1","T3"): ("5K Advanced", None, False),
        ("5k","F4","S2","T1"): ("5K Advanced", None, False),
        ("5k","F4","S2","T2"): ("5K Advanced", None, False),
        ("5k","F4","S2","T3"): ("5K Advanced", None, False),

        # ── 10K ─────────────────────────────────────────────────────
        ("10k","F2","S0","T1"): ("10K Novice", None, False),
        ("10k","F2","S0","T2"): ("10K Novice", None, False),
        ("10k","F2","S0","T3"): ("10K Novice", "10K Intermediate", True),
        ("10k","F2","S1","T1"): ("10K Novice", None, False),
        ("10k","F2","S1","T2"): ("10K Novice", None, False),
        ("10k","F2","S1","T3"): ("10K Novice", "10K Intermediate", True),
        ("10k","F2","S2","T1"): ("10K Novice", None, False),
        ("10k","F2","S2","T2"): ("10K Intermediate", None, False),
        ("10k","F2","S2","T3"): ("10K Intermediate", "10K Advanced", True),
        ("10k","F3","S0","T1"): ("10K Novice", None, False),
        ("10k","F3","S0","T2"): ("10K Novice", None, False),
        ("10k","F3","S0","T3"): ("10K Novice", "10K Intermediate", True),
        ("10k","F3","S1","T1"): ("10K Novice", None, False),
        ("10k","F3","S1","T2"): ("10K Intermediate", None, False),
        ("10k","F3","S1","T3"): ("10K Intermediate", "10K Advanced", True),
        ("10k","F3","S2","T1"): ("10K Intermediate", None, False),
        ("10k","F3","S2","T2"): ("10K Intermediate", None, False),
        ("10k","F3","S2","T3"): ("10K Advanced", None, False),
        ("10k","F4","S0","T1"): ("10K Intermediate", None, False),
        ("10k","F4","S0","T2"): ("10K Intermediate", None, False),
        ("10k","F4","S0","T3"): ("10K Intermediate", "10K Advanced", True),
        ("10k","F4","S1","T1"): ("10K Intermediate", None, False),
        ("10k","F4","S1","T2"): ("10K Intermediate", None, False),
        ("10k","F4","S1","T3"): ("10K Advanced", None, False),
        ("10k","F4","S2","T1"): ("10K Advanced", None, False),
        ("10k","F4","S2","T2"): ("10K Advanced", None, False),
        ("10k","F4","S2","T3"): ("10K Advanced", None, False),

        # ── HM ──────────────────────────────────────────────────────
        ("hm","F2","S0","T1"): ("HM3", None, False),
        ("hm","F2","S0","T2"): ("HM Novice 1", None, False),
        ("hm","F2","S0","T3"): ("HM3", "HM Novice 2", True),
        ("hm","F2","S1","T1"): ("HM Novice 1", None, False),
        ("hm","F2","S1","T2"): ("HM Novice 1", None, False),
        ("hm","F2","S1","T3"): ("HM Novice 1", "HM Novice 2", True),
        ("hm","F2","S2","T1"): ("HM Novice 1", None, False),
        ("hm","F2","S2","T2"): ("HM Novice 2", None, False),
        ("hm","F2","S2","T3"): ("HM Novice 2", "HM Intermediate 1", True),
        ("hm","F3","S0","T1"): ("HM Novice 1", None, False),
        ("hm","F3","S0","T2"): ("HM Novice 1", None, False),
        ("hm","F3","S0","T3"): ("HM Novice 1", "HM Novice 2", True),
        ("hm","F3","S1","T1"): ("HM Novice 1", None, False),
        ("hm","F3","S1","T2"): ("HM Novice 2", None, False),
        ("hm","F3","S1","T3"): ("HM Novice 2", "HM Intermediate 1", True),
        ("hm","F3","S2","T1"): ("HM Intermediate 1", None, False),
        ("hm","F3","S2","T2"): ("HM Intermediate 1", None, False),
        ("hm","F3","S2","T3"): ("HM Intermediate 1", "HM Intermediate 2", True),
        ("hm","F4","S0","T1"): ("HM Novice 2", None, False),
        ("hm","F4","S0","T2"): ("HM Novice 2", None, False),
        ("hm","F4","S0","T3"): ("HM Novice 2", "HM Intermediate 1", True),
        ("hm","F4","S1","T1"): ("HM Intermediate 1", None, False),
        ("hm","F4","S1","T2"): ("HM Intermediate 1", None, False),
        ("hm","F4","S1","T3"): ("HM Intermediate 1", "HM Intermediate 2", True),
        ("hm","F4","S2","T1"): ("HM Intermediate 2", None, False),
        ("hm","F4","S2","T2"): ("HM Intermediate 2", None, False),
        ("hm","F4","S2","T3"): ("HM Advanced", None, False),

        # ── FM ──────────────────────────────────────────────────────
        ("fm","F2","S0","T1"): ("Marathon 3" if use_m3 else "FM Novice 1", None, False),
        ("fm","F2","S0","T2"): ("FM Novice 1", None, False),
        ("fm","F2","S0","T3"): ("FM Novice 1", "FM Novice 2", True),
        ("fm","F2","S1","T1"): ("FM Novice 1", None, False),
        ("fm","F2","S1","T2"): ("FM Novice 1", None, False),
        ("fm","F2","S1","T3"): ("FM Novice 1", "FM Novice 2", True),
        ("fm","F2","S2","T1"): ("FM Novice 1", None, False),
        ("fm","F2","S2","T2"): ("FM Novice 2", None, False),
        ("fm","F2","S2","T3"): ("FM Novice 2", "FM Intermediate 1", True),
        ("fm","F3","S0","T1"): ("FM Novice 1", None, False),
        ("fm","F3","S0","T2"): ("FM Novice 1", None, False),
        ("fm","F3","S0","T3"): ("FM Novice 1", "FM Novice 2", True),
        ("fm","F3","S1","T1"): ("FM Novice 1", None, False),
        ("fm","F3","S1","T2"): ("FM Novice 2", None, False),
        ("fm","F3","S1","T3"): ("FM Novice 2", "FM Intermediate 1", True),
        ("fm","F3","S2","T1"): ("FM Intermediate 1", None, False),
        ("fm","F3","S2","T2"): ("FM Intermediate 1", None, False),
        ("fm","F3","S2","T3"): ("FM Intermediate 1", "FM Intermediate 2", True),
        ("fm","F4","S0","T1"): ("FM Novice 2", None, False),
        ("fm","F4","S0","T2"): ("FM Novice 2", None, False),
        ("fm","F4","S0","T3"): ("FM Novice 2", "FM Intermediate 1", True),
        ("fm","F4","S1","T1"): ("FM Intermediate 1", None, False),
        ("fm","F4","S1","T2"): ("FM Intermediate 1", None, False),
        ("fm","F4","S1","T3"): ("FM Intermediate 1", "FM Intermediate 2", True),
        ("fm","F4","S2","T1"): ("FM Intermediate 1", None, False),
        ("fm","F4","S2","T2"): ("FM Intermediate 2", None, False),
        ("fm","F4","S2","T3"): ("FM Intermediate 2", "FM Advanced 1", True),
    }

    return matrix.get((dist, freq, speed, target), ("5K Novice", None, False))

def hitung_bmi(tinggi_cm, berat_kg):
    if tinggi_cm <= 0 or berat_kg <= 0: return 0.0
    return round(berat_kg / ((tinggi_cm / 100.0) ** 2), 1)

def kategori_bmi(bmi):
    if bmi <= 0: return "Tidak Diketahui"
    if bmi < 18.5: return "Kurus"
    if bmi < 25.0: return "Normal"
    if bmi < 30.0: return "Gemuk"
    return "Obesitas"

def format_durasi(sisa_hari):
    minggu = sisa_hari // 7
    sisa   = sisa_hari % 7
    if sisa == 0: return f"{minggu} minggu"
    return f"{minggu} minggu {sisa} hari ({sisa_hari} hari total)"

def hitung_hrmax(usia):
    if usia <= 0: return 190
    return max(150, int(208 - (0.7 * usia)))

def hitung_zona_hr_karvonen(hrmax, rhr):
    if rhr <= 0 or hrmax <= rhr: return {}
    hrr = hrmax - rhr
    def z(lo, hi): return f"{int(lo * hrr + rhr)}–{int(hi * hrr + rhr)} bpm"
    return {
        "Z1_Easy":     z(0.50, 0.60),
        "Z2_Aerobic":  z(0.60, 0.70),
        "Z3_Tempo":    z(0.70, 0.80),
        "Z4_Interval": z(0.80, 0.90),
        "Z5_Max":      z(0.90, 1.00),
        "HRmax":       hrmax,
        "RHR":         rhr,
    }

def hitung_zona_hr_estimasi(hrmax):
    def z(lo, hi): return f"{int(lo * hrmax)}–{int(hi * hrmax)} bpm"
    return {
        "Z1_Easy":     z(0.50, 0.60),
        "Z2_Aerobic":  z(0.60, 0.70),
        "Z3_Tempo":    z(0.70, 0.80),
        "Z4_Interval": z(0.80, 0.90),
        "Z5_Max":      z(0.90, 1.00),
        "HRmax":       hrmax,
        "RHR":         None,
    }

# ─────────────────────────────────────────────
# CORE ANALYSIS
# ─────────────────────────────────────────────

def analisis_pengguna(input_data: dict) -> dict:
    # ── 1. Parse input
    nama        = str(input_data.get("nama", "Pelari")).strip() or "Pelari"
    usia        = int(input_data.get("usia", 25) or 25)
    tinggi      = float(input_data.get("tinggi", 0) or 0)
    berat       = float(input_data.get("berat", 0) or 0)

    # Health Profile
    riwayat_kardio  = bool(input_data.get("riwayat_kardio", False))
    riwayat_napas   = bool(input_data.get("riwayat_napas", False))
    riwayat_cedera  = bool(input_data.get("riwayat_cedera", False))
    cedera_severity = str(input_data.get("cedera_severity", "rendah")).lower()

    # Training profile
    target_jarak_raw = str(input_data.get("target_jarak", "10k")).lower()
    frekuensi_raw    = str(input_data.get("frekuensi", "3-4x"))
    speedwork_raw    = str(input_data.get("speedwork", "S0")).upper()
    mode_latihan_raw = str(input_data.get("mode_latihan", "realistic")).lower()

    easy_menit       = int(input_data.get("easy_menit", 0) or 0)
    easy_detik       = int(input_data.get("easy_detik", 0) or 0)
    target_jam       = int(input_data.get("target_jam", 0) or 0)
    target_menit     = int(input_data.get("target_menit", 0) or 0)

    punya_pb  = str(input_data.get("punya_pb", "tidak")).lower()
    pb_jarak  = str(input_data.get("pb_jarak", "")).lower()
    pb_jam    = int(input_data.get("pb_jam",   0) or 0)
    pb_menit  = int(input_data.get("pb_menit", 0) or 0)
    pb_detik  = int(input_data.get("pb_detik", 0) or 0)

    # HR
    punya_hrm = str(input_data.get("punya_hrm", "no")).lower()
    tahu_rhr  = str(input_data.get("tahu_rhr", "no")).lower()
    rhr_raw   = input_data.get("rhr", "")
    rhr       = int(rhr_raw) if str(rhr_raw).strip().isdigit() else 0

    # Dates
    tanggal_lomba_str = str(input_data.get("tanggal_lomba", ""))
    tanggal_mulai_str = str(input_data.get("tanggal_mulai", ""))

    # Mapping basic
    jarak_target_db = TARGET_JARAK_MAP.get(target_jarak_raw, "10K")
    jarak_km = JARAK_KE_KM.get(jarak_target_db, 10.0)

    # Normalization (F, S, T)
    freq_map = {
        "<1x": "F1", "< 1x": "F1", "1-2x": "F2", "1–2x": "F2",
        "3-4x": "F3", "3–4x": "F3", ">4x": "F4", "> 4x": "F4",
    }
    freq_n = freq_map.get(frekuensi_raw, "F3")
    
    speed_n = speedwork_raw if speedwork_raw in ["S0", "S1", "S2"] else "S0"

    target_map = {
        "beginner": "T1", "realistic": "T2", "ambitious": "T3"
    }
    target_n = target_map.get(mode_latihan_raw, "T2")

    # BMI
    bmi = hitung_bmi(tinggi, berat)
    bmi_kategori = kategori_bmi(bmi)
    bmi_risiko = bmi >= 30.0          # Obesitas
    bmi_kurus  = 0 < bmi < 18.5      # Kurus / Underweight

    # ── LAYER 0: Health Screening
    health_blocked = False
    health_warnings = []
    
    # Defaults modifiers
    level_downgrade = 0
    cap_novice = False

    if riwayat_cedera:
        if cedera_severity == "parah":
            health_blocked = True
            health_warnings.append("Berdasarkan riwayat cederamu yang masih dalam kategori parah, kami tidak dapat merekomendasikan program lari saat ini. Silakan konsultasi dengan fisioterapis atau dokter olahraga terlebih dahulu.")
        elif cedera_severity == "sedang":
            level_downgrade = 2
            health_warnings.append("Karena riwayat cedera sedang, disarankan konsultasi dengan dokter olahraga sebelum memulai. Program akan diturunkan intensitasnya.")
        elif cedera_severity == "rendah":
            level_downgrade = 1
            health_warnings.append("Monitor kondisi area cedera. Jika ada ketidaknyamanan, ganti sesi ini dengan easy run.")

    if riwayat_kardio or riwayat_napas:
        cap_novice = True
        health_warnings.append("Berdasarkan riwayat kesehatan kardio/pernapasan, sangat disarankan berkonsultasi dengan dokter sebelum memulai program lari intensitas apapun. Hentikan latihan jika merasakan nyeri dada, sesak napas tidak normal, atau pusing.")

    # ── LAYER 1: Kalkulasi Waktu
    today = datetime.date.today()
    try: tanggal_lomba = datetime.date.fromisoformat(tanggal_lomba_str)
    except: tanggal_lomba = today + datetime.timedelta(days=56)
    try: tanggal_mulai = datetime.date.fromisoformat(tanggal_mulai_str)
    except: tanggal_mulai = today

    sisa_hari = max(7, (tanggal_lomba - tanggal_mulai).days)
    weeks_available = max(1, sisa_hari // 7)

    # ── LAYER 2: Penentuan Level Plan (F x S x T Matrix)
    safe_plan, amb_plan, needs_dual = select_plan(target_jarak_raw, freq_n, speed_n, target_n, weeks_available)

    # Apply Health Modifiers
    if cap_novice:
        safe_plan = downgrade_plan(safe_plan, 10) # Downgrade completely
        if amb_plan: amb_plan = downgrade_plan(amb_plan, 10)
        needs_dual = False
    
    if level_downgrade > 0:
        safe_plan = downgrade_plan(safe_plan, level_downgrade)
        if amb_plan: amb_plan = downgrade_plan(amb_plan, level_downgrade)
    
    if bmi_risiko and target_n == "T3":
        safe_plan = downgrade_plan(safe_plan, 1)
        if amb_plan: amb_plan = downgrade_plan(amb_plan, 1)
        health_warnings.append("Dengan berat badan saat ini, tekanan pada sendi lutut dan pinggul saat berlari sekitar 3x berat badanmu. Sangat disarankan untuk melakukan sesi cross-training (renang, sepeda) di hari-hari non-lari, dan memantau kondisi lutut secara ketat.")

    if bmi_kurus:
        health_warnings.append("IMT kamu termasuk kategori kurus (underweight). Massa otot yang kurang dapat meningkatkan risiko cedera saat berlari, karena otot berperan sebagai peredam kejut untuk sendi. Pastikan kamu mencukupi asupan protein (1.6–2.0 g/kg berat badan per hari), dan konsultasikan dengan ahli gizi olahraga sebelum memulai program intensitas tinggi.")
        if target_n == "T3":
            safe_plan = downgrade_plan(safe_plan, 1)
            if amb_plan: amb_plan = downgrade_plan(amb_plan, 1)

    # Validate Plan against Time Available
    min_weeks = PLAN_MIN_WEEKS.get(safe_plan, 8)
    if weeks_available < min_weeks:
        gap = min_weeks - weeks_available
        if gap <= 2:
            health_warnings.append(f"Waktu latihanmu sedikit kurang dari ideal ({weeks_available} minggu tersedia, idealnya {min_weeks} minggu). Kami memangkas {gap} minggu awal.")
        else:
            # Huge gap - automatically downgrade or just warn
            health_warnings.append(f"Waktu latihanmu sangat kurang ({weeks_available} minggu tersedia, idealnya {min_weeks} minggu). Kami harus memangkas program secara signifikan, risiko cedera lebih tinggi.")
            # Downgrade 1 level if we can
            safe_plan = downgrade_plan(safe_plan, 1)

    # Check for excess time
    if weeks_available > min_weeks + 2:
        health_warnings.append(f"Kamu punya waktu ekstra sebelum mulai program utama. Kami rekomendasikan kamu mengisi waktu ini dengan Base Training untuk membangun fondasi yang lebih solid.")

    # ── LAYER 3: VDOT Gap Check
    vdot_current = 0.0
    vdot_target = 0.0
    vdot_proyeksi = 0.0
    vdot_gap = 0.0

    # Calculate current VDOT
    if punya_pb == "ya" and pb_jarak:
        # VDOT from PB
        pb_total_secs = pb_jam * 3600 + pb_menit * 60 + pb_detik
        if pb_total_secs > 0:
            vdot_current = vdot_from_time(pb_jarak, pb_total_secs)
    elif target_n in ["T2", "T3"] and easy_menit > 0:
        # VDOT from Easy Pace
        easy_sec_per_km = easy_menit * 60 + easy_detik
        # Reverse lookup from TRAINING_PACES easy_min/easy_max
        best_v, best_diff = 30.0, float("inf")
        for v, paces in TRAINING_PACES.items():
            mid_easy = (paces["easy_min"] + paces["easy_max"]) / 2
            diff = abs(mid_easy - easy_sec_per_km)
            if diff < best_diff:
                best_diff, best_v = diff, v
        vdot_current = best_v

    if vdot_current > 0:
        vdot_proyeksi = projected_vdot(vdot_current, min_weeks)

    dual_option_reasons = []

    # Calculate target VDOT and check GAP
    if target_n == "T3":
        total_detik_target = target_jam * 3600 + target_menit * 60
        if total_detik_target > 0:
            vdot_target = vdot_from_time(target_jarak_raw, total_detik_target)
            
            if vdot_proyeksi > 0:
                vdot_gap = vdot_target - vdot_proyeksi
                
                if vdot_gap >= 3:
                    needs_dual = True
                    if vdot_gap > 5:
                        dual_option_reasons.append("Berdasarkan data larimu saat ini, target waktu ini kemungkinan besar tidak dapat dicapai dalam 1 siklus program ini. Untuk mencapai target ini, kamu mungkin membutuhkan 2-3 siklus latihan (sekitar 6-12 bulan). Kami tetap menampilkan jadwal ini agar kamu bisa berlatih ke arah yang benar, namun disarankan untuk menyesuaikan ekspektasi di race day.")
                    else:
                        dual_option_reasons.append("Target waktu agak ambisius untuk satu siklus latihan. Sangat butuh kedisiplinan dan hindari push terlalu keras jika merasa tidak nyaman.")

    # Other dual option reasons
    if needs_dual:
        if freq_n in ["F1", "F2"] and amb_plan and ("Advanced" in amb_plan or "Intermediate" in amb_plan):
            dual_option_reasons.append("Plan ambisius dirancang untuk pelari yang sudah terbiasa berlari lebih sering. Tubuhmu memerlukan adaptasi bertahap sebelum menangani volume ini. Meningkatkan volume terlalu cepat adalah penyebab utama cedera lari.")
        if speed_n == "S0" and amb_plan and ("Advanced" in amb_plan or "Intermediate" in amb_plan):
            dual_option_reasons.append("Program ini mengandung sesi interval dan tempo run. Speedwork yang dilakukan tanpa dasar yang cukup meningkatkan risiko cedera. Jika kamu belum melakukan berbagai jenis speedwork dalam program ini, sebaiknya pilih program yang lebih rendah.")
            
        if len(dual_option_reasons) == 0:
            needs_dual = False
            if amb_plan:
                safe_plan = amb_plan

    # ── LAYER 4: Zona Latihan
    training_paces = {}
    zona_metode = "rpe"
    rpe_guide = {}
    zona_hr = {}
    hrmax = hitung_hrmax(usia)

    # A: Punya PB / VDOT -> VDOT Daniels paces
    if vdot_current > 0:
        zona_metode = "vdot_daniels"
        training_paces = interp_paces(vdot_current)
    
    # HR overrides
    if punya_hrm == "yes":
        if tahu_rhr == "yes" and rhr > 0:
            zona_metode = "karvonen" if vdot_current == 0 else "vdot_daniels_hr"
            zona_hr = hitung_zona_hr_karvonen(hrmax, rhr)
        else:
            zona_metode = "hrmax_pct" if vdot_current == 0 else "vdot_daniels_hr"
            zona_hr = hitung_zona_hr_estimasi(hrmax)
            if vdot_current == 0:
                health_warnings.append("Karena RHR tidak diketahui, zona HR menggunakan metode persentase dari HR maksimum. Akurasi lebih rendah dibanding metode Karvonen. Sebaiknya ukur RHR kamu besok pagi sebelum bangun tidur untuk hasil yang lebih akurat.")
    
    if zona_metode == "rpe" or (vdot_current == 0 and punya_hrm == "no"):
        zona_metode = "rpe"
        rpe_guide = {
            "Z1_Easy": "RPE 1-2 (Sangat mudah, bisa bernyanyi)",
            "Z2_Aerobic": "RPE 3-4 (Mudah, bisa bicara kalimat panjang)",
            "Z3_Tempo": "RPE 5-6 (Cukup keras, bicara kalimat pendek)",
            "Z4_Interval": "RPE 7-8 (Keras, hanya bisa bicara 1-2 kata)",
            "Z5_Max": "RPE 9-10 (Sangat keras, hampir tidak bicara)"
        }

    # Race Pace
    rp_sec = 0.0
    if vdot_current > 0:
        base_rp = race_time_from_vdot(vdot_current, target_jarak_raw) / jarak_km
        if target_n in ["T1", "T2"]:
            rp_sec = base_rp
        elif target_n == "T3":
            total_detik_target = target_jam * 3600 + target_menit * 60
            if total_detik_target > 0:
                rp_sec = total_detik_target / jarak_km
            else:
                rp_sec = race_time_from_vdot(vdot_proyeksi, target_jarak_raw) / jarak_km
    else:
        # Fallback jika tidak ada PB / VDOT
        if target_n == "T1":
            rp_sec = max(510.0, jarak_km * 60 * 1.5 / jarak_km)
        elif target_n == "T2":
            rp_sec = 420.0 # Default realistis 7:00/km
        elif target_n == "T3":
            total_detik_target = target_jam * 3600 + target_menit * 60
            if total_detik_target > 0:
                rp_sec = total_detik_target / jarak_km
            else:
                rp_sec = 390.0
                
    if rp_sec <= 0:
        rp_sec = 420.0

    # Safe Race Pace
    rp_sec_aman = rp_sec
    if vdot_proyeksi > 0 and target_n == "T3":
        rp_sec_aman = race_time_from_vdot(vdot_proyeksi, target_jarak_raw) / jarak_km

    if level_downgrade > 0 or bmi_risiko or bmi_kurus:
        rp_sec_aman = max(rp_sec_aman + 30, 480.0)

    # Set Final Level
    level_final = amb_plan if amb_plan and needs_dual else safe_plan
    if not needs_dual:
        level_aman = safe_plan
    else:
        level_aman = safe_plan

    # Map target level to DB
    # We store the original string and we will use DB_MAP at scheduling time.

    # ── Kemas Hasil
    return {
        "nama": nama, "usia": usia, "tinggi": tinggi, "berat": berat,
        "bmi": bmi, "bmi_kategori": bmi_kategori, "bmi_risiko": bmi_risiko, "bmi_kurus": bmi_kurus,
        "hrmax": hrmax, "punya_hrm": punya_hrm, "rhr": rhr,
        "zona_hr": zona_hr, "zona_metode": zona_metode,
        "training_paces": training_paces, "rpe_guide": rpe_guide,
        "vdot": vdot_current, "vdot_proyeksi": vdot_proyeksi,
        "vdot_target": vdot_target, "vdot_gap": vdot_gap,
        "punya_pb": punya_pb == "ya",
        "jarak": jarak_target_db, "jarak_km": jarak_km,
        "metode_target": mode_latihan_raw,
        "rp_sec": rp_sec,
        "level": level_final, "level_aman": level_aman, "rp_sec_aman": rp_sec_aman,
        "resiko_ditemukan": needs_dual or len(health_warnings) > 0,
        "needs_dual": needs_dual,
        "health_blocked": health_blocked,
        "health_warnings": health_warnings,
        "dual_option_reasons": dual_option_reasons,
        "tanggal_lomba": tanggal_lomba.isoformat(),
        "tanggal_mulai": tanggal_mulai.isoformat(),
        "sisa_hari": sisa_hari, "sisa_waktu": weeks_available,
        "durasi_str": format_durasi(sisa_hari)
    }

# ─────────────────────────────────────────────
# GENERATE JADWAL TABLE
# ─────────────────────────────────────────────

def generate_jadwal(data: dict, target_level_raw: str, target_rp_sec: float) -> dict:
    jarak         = data["jarak"] # "10K", "Half Marathon", dll
    sisa_waktu    = data["sisa_waktu"]
    tanggal_lomba = datetime.date.fromisoformat(data["tanggal_lomba"])
    tanggal_mulai = datetime.date.fromisoformat(data["tanggal_mulai"])

    race_weekday_idx = tanggal_lomba.weekday()
    nama_hari_race   = NAMA_HARI[race_weekday_idx]

    header_ui = [NAMA_HARI[(race_weekday_idx - 6 + pos) % 7] for pos in range(7)]
    db_to_ui_pos = {NAMA_HARI[i]: i for i in range(7)}
    ui_pos_to_db = {v: k for k, v in db_to_ui_pos.items()}

    # Resolve level dari String -> [TopKey, PlanKey]
    db_mapping = DB_MAP.get(target_level_raw, [jarak, "Novice"])
    db_jarak = db_mapping[0]
    db_level = db_mapping[1]

    # Amankan kalau db_jarak gak sama sama jarak
    if db_jarak not in hal_higdon_db: db_jarak = list(hal_higdon_db.keys())[0]
    if db_level not in hal_higdon_db[db_jarak]: db_level = list(hal_higdon_db[db_jarak].keys())[0]

    durasi_ideal  = hal_higdon_db[db_jarak][db_level]["durasi_minggu"]
    jadwal_mentah = hal_higdon_db[db_jarak][db_level]["jadwal"]

    base_level_str = "Novice"
    if "Intermediate" in target_level_raw: base_level_str = "Intermediate"
    elif "Advanced" in target_level_raw: base_level_str = "Advanced"

    jadwal_terpilih = {}
    if sisa_waktu < durasi_ideal:
        minggu_mulai = durasi_ideal - sisa_waktu + 1
        for i in range(minggu_mulai, durasi_ideal + 1):
            key = str(i) if str(i) in jadwal_mentah else i
            if key in jadwal_mentah:
                jadwal_terpilih[i - minggu_mulai + 1] = jadwal_mentah[key]
    elif sisa_waktu > durasi_ideal:
        selisih = sisa_waktu - durasi_ideal
        try:
            jadwal_base = hal_higdon_db["Base_Training"][base_level_str]["jadwal"]
        except KeyError:
            jadwal_base = {"1": {
                "Senin": "Istirahat", "Selasa": "Lari 4.8 km", "Rabu": "Cross training",
                "Kamis": "Lari 4.8 km", "Jumat": "Istirahat", "Sabtu": "Lari 6.4 km",
                "Minggu": "Lari 9.7 km"
            }}
        for i in range(1, selisih + 1):
            key_base = str(((i - 1) % 12) + 1)
            jadwal_terpilih[i] = jadwal_base.get(key_base, list(jadwal_base.values())[0])
        for i in range(1, durasi_ideal + 1):
            key_inti = str(i) if str(i) in jadwal_mentah else i
            jadwal_terpilih[selisih + i] = jadwal_mentah[key_inti]
    else:
        for i in range(1, durasi_ideal + 1):
            key = str(i) if str(i) in jadwal_mentah else i
            jadwal_terpilih[i] = jadwal_mentah[key]

    list_minggu     = sorted(jadwal_terpilih.keys())
    minggu_terakhir = list_minggu[-1] if list_minggu else 1
    rows            = []

    for m in list_minggu:
        menu_db     = jadwal_terpilih[m]
        is_race_week = (m == minggu_terakhir)
        is_taper     = is_race_week or (db_jarak == "Marathon" and m >= minggu_terakhir - 2)

        tgl_race_minggu = tanggal_lomba - datetime.timedelta(days=(minggu_terakhir - m) * 7)
        tgl_awal_ui     = tgl_race_minggu - datetime.timedelta(days=6)

        label = f"M-{m} | {tgl_awal_ui.strftime('%d %b')} – {tgl_race_minggu.strftime('%d %b')}"
        if is_taper: label += " (Taper)"

        baris = {"minggu": label, "minggu_num": m, "is_taper": is_taper, "is_race_week": is_race_week}

        for ui_col_idx in range(7):
            ui_hari_nama = header_ui[ui_col_idx]
            is_race_col  = (ui_col_idx == 6)
            db_hari_nama = ui_pos_to_db.get(ui_col_idx)
            tgl_kolom    = tgl_awal_ui + datetime.timedelta(days=ui_col_idx)

            if is_race_week and is_race_col:
                sesi = f"🎯 RACE DAY! {jarak}"
                tipe = "race"
            elif tgl_kolom < tanggal_mulai:
                sesi = "➖ Belum Mulai"
                tipe = "blm"
            else:
                raw = menu_db.get(db_hari_nama, "Istirahat") if db_hari_nama else "Istirahat"
                if "istirahat" in raw.lower() and not any(
                    x in raw.lower() for x in ["lari", "km", "cross", "tempo", "jalan"]
                ):
                    sesi = f"🛌 {raw}"
                    tipe = "rest"
                elif any(x in raw.lower() for x in ["lomba", "tes 5k"]):
                    sesi = f"🎯 {raw}"
                    tipe = "race"
                elif any(x in raw.lower() for x in ["km", "tempo", "interval", "hill", "pace", "lari", "jalan"]):
                    sesi = f"🏃 {raw}"
                    tipe = "run"
                else:
                    sesi = raw
                    tipe = "other"

            baris[ui_hari_nama] = {"sesi": sesi, "tipe": tipe}

        rows.append(baris)

    return {
        "header":         header_ui,
        "nama_hari_race": nama_hari_race,
        "rows":           rows,
        "level":          target_level_raw,
    }