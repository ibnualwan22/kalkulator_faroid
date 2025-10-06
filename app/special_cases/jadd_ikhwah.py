from __future__ import annotations

"""
Jadd ma'al-Ikhwah (جد مع الإخوة)
Kasus: Kakek bersama saudara/i (tanpa ayah)
"""

from typing import List
from app.schemas.calculation import CalculationResult, HeirShare
from app.schemas.heir import HeirInput, HeirResponse
from app.utils.constants import HeirID, HEIR_NAMES
from app.core.calculator import FaroidCalculator
from app.schemas.calculation import CalculationInput


def is_jadd_ikhwah(heirs: List[HeirInput]) -> bool:
    """
    Cek apakah kasus Jadd ma'al-Ikhwah
    
    Syarat:
    - Ada Jadd (kakek)
    - Ada saudara/i (kandung atau seayah)
    - Tidak ada Abb (ayah)
    """
    heir_dict = {h.id: h.quantity for h in heirs}
    
    has_jadd = heir_dict.get(HeirID.JADD, 0) > 0
    has_abb = heir_dict.get(HeirID.ABB, 0) > 0
    
    sibling_ids = [
        HeirID.AKH_ABAWAYN, HeirID.AKH_AB,
        HeirID.UKHT_ABAWAYN, HeirID.UKHT_AB
    ]
    has_siblings = any(heir_dict.get(sid, 0) > 0 for sid in sibling_ids)
    
    return has_jadd and has_siblings and not has_abb


def calculate_jadd_ikhwah(heirs: List[HeirInput], tirkah: float,
                         notes: List[str]) -> CalculationResult:
    """
    Hitung Jadd ma'al-Ikhwah
    
    Kakek memilih yang lebih baik dari:
    1. Muqasamah (bagi bersama saudara seperti saudara laki-laki)
    2. 1/3 dari seluruh harta (jika tidak ada dzawil furudh lain)
    3. 1/3 dari sisa (jika ada dzawil furudh lain)
    4. 1/6 (jika jumlah saudara banyak)
    """
    notes.append("🔄 Kasus Jadd ma'al-Ikhwah")
    notes.append("   Kakek memilih opsi terbaik:")
    notes.append("   1. Muqasamah dengan saudara")
    notes.append("   2. 1/3 dari harta/sisa")
    notes.append("   3. 1/6")
    notes.append("")
    
    # Untuk saat ini, implementasi sederhana: muqasamah
    # TODO: Implement full logic dengan 3 opsi
    
    calc_input = CalculationInput(heirs=heirs, tirkah=tirkah)
    calculator = FaroidCalculator(calc_input)
    calculator.notes = notes
    result = calculator._calculate_normal()
    
    result.is_special_case = True
    result.special_case_name = "Jadd ma'al-Ikhwah"
    
    return result
