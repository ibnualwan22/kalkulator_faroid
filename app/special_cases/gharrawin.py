from __future__ import annotations

"""
Al-Gharrawin (الغرّاوين)
Kasus: Dua nenek yang sederajat
"""

from typing import List
from app.schemas.calculation import CalculationResult
from app.schemas.heir import HeirInput
from app.utils.constants import HeirID


def is_gharrawin(heirs: List[HeirInput]) -> bool:
    """
    Cek apakah kasus Gharrawin (dua nenek)
    
    Syarat:
    - Ada nenek dari ibu dan nenek dari ayah
    - Keduanya sama derajatnya
    """
    heir_dict = {h.id: h.quantity for h in heirs}
    
    has_jaddah_umm = heir_dict.get(HeirID.JADDAH_UMM, 0) > 0
    has_jaddah_abb = heir_dict.get(HeirID.JADDAH_ABB, 0) > 0
    
    return has_jaddah_umm and has_jaddah_abb


def calculate_gharrawin(heirs: List[HeirInput], tirkah: float,
                       notes: List[str]) -> CalculationResult:
    """
    Hitung Gharrawin
    
    Dua nenek yang sederajat berbagi 1/6 (dibagi dua)
    """
    notes.append("👵 Kasus Al-Gharrawin (Dua Nenek)")
    notes.append("   Nenek dari Ibu dan Nenek dari Ayah berbagi 1/6")
    notes.append("   Masing-masing mendapat 1/12")
    notes.append("")
    
    from app.core.calculator import FaroidCalculator
    from app.schemas.calculation import CalculationInput
    
    calc_input = CalculationInput(heirs=heirs, tirkah=tirkah)
    calculator = FaroidCalculator(calc_input)
    calculator.notes = notes
    result = calculator._calculate_normal()
    
    result.is_special_case = True
    result.special_case_name = "Al-Gharrawin"
    
    return result
