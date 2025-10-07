"""
Module untuk menangani Inkisar (Tashih) sesuai dengan kitab Faroidh.
"""

from typing import List, Tuple
from math import gcd


def _relation(a: int, b: int) -> str:
    """Menentukan hubungan perbandingan antara dua bilangan"""
    # ✅ FIX: Convert to INT
    a = int(a)
    b = int(b)
    
    if a == b:
        return "mumatsalah"
    if a % b == 0 or b % a == 0:
        return "mudakholah"
    g = gcd(a, b)
    if g == 1:
        return "mubayanah"
    return "muwafaqoh"


def _single_group_adad_madhrub(ruus: int, saham: int) -> Tuple[int, str]:
    """Hitung عدد المضروب untuk 1 kelompok"""
    # ✅ FIX: Convert to INT
    ruus = int(ruus)
    saham = int(saham)
    
    rel = _relation(ruus, saham)
    
    if rel == "mubayanah":
        return ruus, rel
    if rel == "muwafaqoh":
        g = gcd(ruus, saham)
        return ruus // g, rel
    return 1, rel


def _compare_madhrub(madhrub_list: List[int]) -> int:
    """Bandingkan semua عدد المضروب"""
    if not madhrub_list:
        return 1
    
    filtered = [m for m in madhrub_list if m > 1]
    if not filtered:
        return 1
    if len(filtered) == 1:
        return filtered[0]
    
    result = filtered[0]
    for i in range(1, len(filtered)):
        current = filtered[i]
        rel = _relation(result, current)
        
        if rel == "mumatsalah":
            result = result
        elif rel == "mudakholah":
            result = max(result, current)
        elif rel == "mubayanah":
            result = result * current
        elif rel == "muwafaqoh":
            g = gcd(result, current)
            result = (result * current) // g
    
    return result


def compute_inkisar_single_group(ruus: int, saham: int, ashl: int, notes: List[str]) -> Tuple[int, List[str]]:
    """KASUS 1: Hanya 1 kelompok yang tidak bisa dibagi utuh"""
    ruus = int(ruus)
    saham = int(saham)
    ashl = int(ashl)
    
    if saham % ruus == 0:
        return ashl, notes
    
    # Detail analysis
    notes.append(f"   📊 ANALISIS DETAIL:")
    notes.append(f"   عدد الرؤوس : Saham = {ruus} : {saham}")
    notes.append(f"   Pembagian: {saham} ÷ {ruus} = {saham/ruus:.3f} ❌ (tidak utuh)")
    
    g = gcd(ruus, saham)
    notes.append(f"   GCD({ruus}, {saham}) = {g}")
    
    rel = _relation(ruus, saham)
    
    if rel == "mubayanah":
        ashl_baru = ashl * ruus
        notes.append(f"   Hubungan: MUBAYANAH (مباينة)")
        notes.append(f"   عدد المضروب = عدد الرؤوس = {ruus}")
        notes.append(f"   Ashl baru = {ashl} × {ruus} = {ashl_baru}")
    elif rel == "muwafaqoh":
        wafq = ruus // g
        ashl_baru = ashl * wafq
        notes.append(f"   Hubungan: MUWAFAQOH (موافقة)")
        notes.append(f"   عدد المضروب = {ruus} ÷ {g} = {wafq}")
        notes.append(f"   Ashl baru = {ashl} × {wafq} = {ashl_baru}")
    elif rel == "mudakholah":
        if saham < ruus:
            multiplier = ruus // saham
            ashl_baru = ashl * multiplier
            notes.append(f"   Hubungan: MUDAKHOLAH (تداخل)")
            notes.append(f"   عدد المضروب = {ruus} ÷ {saham} = {multiplier}")
            notes.append(f"   Ashl baru = {ashl} × {multiplier} = {ashl_baru}")
        else:
            ashl_baru = ashl
            notes.append(f"   Hubungan: MUDAKHOLAH (تداخل) - sudah bisa dibagi")
    else:
        ashl_baru = ashl
        notes.append(f"   Hubungan: MUMATSALAH (متماثلة) - sudah bisa dibagi")
    
    return ashl_baru, notes




def compute_inkisar_multiple_groups(groups: List[Tuple[str, int, int]], ashl: int, notes: List[str]) -> Tuple[int, List[str]]:
    """KASUS 2: Lebih dari 1 kelompok yang tidak bisa dibagi utuh"""
    # ✅ FIX: Convert to INT
    ashl = int(ashl)
    
    notes.append(f"🔹 INKISAR - Kasus Banyak Kelompok")
    notes.append(f"   Jumlah kelompok: {len(groups)}")
    notes.append("")
    
    # STEP A: Detail perbandingan individual
    madhrub_list = []
    notes.append(f"   📊 STEP A: Analisis Individual per Kelompok")
    
    for i, (nama, ruus, saham) in enumerate(groups, 1):
        ruus = int(ruus)  
        saham = int(saham)  
        
        notes.append(f"   ┌─ Kelompok {i}: {nama}")
        notes.append(f"   │  عدد الرؤوس : Saham = {ruus} : {saham}")
        notes.append(f"   │  Pembagian: {saham} ÷ {ruus} = {saham/ruus:.3f} ❌ (tidak utuh)")
        
        # Hitung GCD dan relasi
        g = gcd(ruus, saham)
        notes.append(f"   │  GCD({ruus}, {saham}) = {g}")
        
        # Tentukan relasi
        if g == 1:
            rel = "MUBAYANAH"
            madhrub = ruus
            notes.append(f"   │  Hubungan: {rel} (مباينة)")
            notes.append(f"   │  عدد المضروب = عدد الرؤوس = {madhrub}")
        elif ruus % saham == 0 or saham % ruus == 0:
            rel = "MUDAKHOLAH" 
            if ruus > saham:
                madhrub = ruus // g
                notes.append(f"   │  Hubungan: {rel} (تداخل)")
                notes.append(f"   │  عدد المضروب = {ruus} ÷ {g} = {madhrub}")
            else:
                madhrub = saham // g
                notes.append(f"   │  Hubungan: {rel} (تداخل)")
                notes.append(f"   │  عدد المضروب = {saham} ÷ {g} = {madhrub}")
        else:
            rel = "MUWAFAQOH"
            madhrub = ruus // g
            notes.append(f"   │  Hubungan: {rel} (موافقة)")
            notes.append(f"   │  عدد المضروب = {ruus} ÷ {g} = {madhrub}")
        
        madhrub_list.append(madhrub)
        notes.append(f"   └─ Hasil: عدد المضروب = {madhrub}")
        notes.append("")
    
    # STEP B: Perbandingan عدد المضروب
    notes.append(f"   🔄 STEP B: Perbandingan عدد المضروب")
    notes.append(f"   Daftar عدد المضروب: {madhrub_list}")
    notes.append("")
    
    # Proses perbandingan bertingkat
    if len(madhrub_list) == 2:
        a, b = madhrub_list[0], madhrub_list[1]
        notes.append(f"   Bandingkan: {a} dengan {b}")
        
        g_final = gcd(a, b)
        notes.append(f"   GCD({a}, {b}) = {g_final}")
        
        if a == b:
            multiplier = a
            notes.append(f"   Hubungan: MUMATSALAH (متماثلة)")
            notes.append(f"   Multiplier = {a}")
        elif a % b == 0 or b % a == 0:
            multiplier = max(a, b)
            notes.append(f"   Hubungan: MUDAKHOLAH (تداخل)")
            notes.append(f"   Multiplier = max({a}, {b}) = {multiplier}")
        elif g_final == 1:
            multiplier = a * b
            notes.append(f"   Hubungan: MUBAYANAH (مباينة)")
            notes.append(f"   Multiplier = {a} × {b} = {multiplier}")
        else:
            multiplier = (a * b) // g_final
            notes.append(f"   Hubungan: MUWAFAQOH (موافقة)")
            notes.append(f"   Multiplier = ({a} × {b}) ÷ {g_final} = {multiplier}")
            
    else:
        # Lebih dari 2 kelompok - proses bertahap
        notes.append(f"   Proses bertahap untuk {len(madhrub_list)} kelompok:")
        multiplier = madhrub_list[0]
        
        for i in range(1, len(madhrub_list)):
            current = madhrub_list[i]
            g_step = gcd(multiplier, current)
            
            notes.append(f"   Langkah {i}: {multiplier} dengan {current}")
            notes.append(f"   GCD({multiplier}, {current}) = {g_step}")
            
            if multiplier == current:
                notes.append(f"   Hubungan: MUMATSALAH → Result = {multiplier}")
            elif multiplier % current == 0 or current % multiplier == 0:
                multiplier = max(multiplier, current)
                notes.append(f"   Hubungan: MUDAKHOLAH → Result = {multiplier}")
            elif g_step == 1:
                multiplier = multiplier * current
                notes.append(f"   Hubungan: MUBAYANAH → Result = {multiplier}")
            else:
                multiplier = (multiplier * current) // g_step
                notes.append(f"   Hubungan: MUWAFAQOH → Result = {multiplier}")
    
    ashl_baru = ashl * multiplier
    notes.append("")
    notes.append(f"   🎯 HASIL AKHIR:")
    notes.append(f"   Multiplier final = {multiplier}")
    notes.append(f"   Ashl baru = {ashl} × {multiplier} = {ashl_baru}")
    
    return ashl_baru, notes



def check_and_apply_inkisar(furudh_saham: List[Tuple], ashl: int, notes: List[str]) -> Tuple[int, List[Tuple], List[str]]:
    """Main function: Cek apakah perlu Inkisar dan apply jika diperlukan"""
    from app.utils.constants import HEIR_NAMES
    
    # ✅ FIX: Convert to INT
    ashl = int(ashl)
    
    groups_need_inkisar = []
    
    for furudh, saham in furudh_saham:
        saham = int(saham)  # ✅ FIX
        if furudh.quantity > 1:
            if saham % furudh.quantity != 0:
                heir_name = HEIR_NAMES.get(furudh.heir_id, {}).get("id", "Unknown")
                groups_need_inkisar.append((
                    f"{furudh.quantity} {heir_name}",
                    furudh.quantity,
                    saham
                ))
    
    if not groups_need_inkisar:
        notes.append("✅ Tidak perlu Inkisar (semua saham bisa dibagi utuh)")
        return ashl, furudh_saham, notes
    
    if len(groups_need_inkisar) == 1:
        nama, ruus, saham_k = groups_need_inkisar[0]
        ashl_baru, notes = compute_inkisar_single_group(ruus, saham_k, ashl, notes)
    else:
        ashl_baru, notes = compute_inkisar_multiple_groups(groups_need_inkisar, ashl, notes)
    
    multiplier = ashl_baru // ashl
    furudh_saham_updated = [
        (furudh, int(saham * multiplier))  # ✅ FIX
        for furudh, saham in furudh_saham
    ]
    
    return ashl_baru, furudh_saham_updated, notes
