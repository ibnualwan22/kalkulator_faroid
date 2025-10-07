"""
Validator untuk 'Aul (العول) - Kenaikan Ashl
"""

# Mapping 'Aul yang valid menurut kitab
AUL_VALID_CASES = {
    6: [7, 8, 9, 10],     # Ashl 6 bisa naik ke 7,8,9,10
    12: [13, 15, 17],     # Ashl 12 bisa naik ke 13,15,17
    24: [27]              # Ashl 24 bisa naik ke 27
}

# Nama 'Aul
AUL_NAMES = {
    (6, 7): "Al-'Aul al-Ula (العول الأولى)",
    (6, 8): "Al-'Aul ats-Tsaniyah (العول الثانية)",
    (6, 9): "Al-'Aul ats-Tsalitsah (العول الثالثة)",
    (6, 10): "Al-'Aul ar-Rabi'ah (العول الرابعة)",
    (12, 13): "Al-'Aul al-Ula min Itsnay 'Ashar",
    (12, 15): "Al-'Aul ats-Tsaniyah min Itsnay 'Ashar",
    (12, 17): "Al-'Aul ats-Tsalitsah min Itsnay 'Ashar",
    (24, 27): "Al-'Aul min Arba'ah wa 'Isyrin"
}

def validate_aul(ashl_awal: int, ashl_akhir: int) -> tuple[bool, str]:
    """Validasi apakah 'aul yang terjadi sesuai dengan kitab"""
    if ashl_awal not in AUL_VALID_CASES:
        return False, f"Ashl {ashl_awal} tidak pernah mengalami 'aul"
    
    if ashl_akhir not in AUL_VALID_CASES[ashl_awal]:
        return False, f"'Aul dari {ashl_awal} ke {ashl_akhir} tidak valid"
    
    aul_name = AUL_NAMES.get((ashl_awal, ashl_akhir), "")
    return True, f"✅ Valid: {aul_name}"
