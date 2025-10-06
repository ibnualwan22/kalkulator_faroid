from __future__ import annotations

"""
Al-Musytarakah / Al-Himariyyah (المشتركة / الحمارية)
Kasus: Suami/Istri + Ibu/Nenek + Saudara seibu + Saudara kandung/seayah
"""

from typing import List
from app.schemas.calculation import CalculationResult
from app.schemas.heir import HeirInput
from app.utils.constants import HeirID


def is_musytarakah(heirs: List[HeirInput]) -> bool:
    """
    Cek apakah kasus Musytarakah
    
    Syarat:
    - Ada Suami atau Istri
    - Ada Ibu atau Nenek
    - Ada Saudara seibu
    - Ada Saudara kandung atau seayah
    """
    heir_dict = {h.id: h.quantity for h in heirs}
    
    has_spouse = (heir_dict.get(HeirID.ZAWJ, 0) > 0 or 
                  heir_dict.get(HeirID.ZAWJAH, 0) > 0)
    
    has_mother = (heir_dict.get(HeirID.UMM, 0) > 0 or
                  heir_dict.get(HeirID.JADDAH_UMM, 0) > 0 or
                  heir_dict.get(HeirID.JADDAH_ABB, 0) > 0)
    
    has_sibling_umm = (heir_dict.get(HeirID.AKH_UMM, 0) > 0 or
                       heir_dict.get(HeirID.UKHT_UMM, 0) > 0)
    
    has_sibling_full = (heir_dict.get(HeirID.AKH_ABAWAYN, 0) > 0 or
                        heir_dict.get(HeirID.UKHT_ABAWAYN, 0) > 0 or
                        heir_dict.get(HeirID.AKH_AB, 0) > 0 or
                        heir_dict.get(HeirID.UKHT_AB, 0) > 0)
    
    return has_spouse and has_mother and has_sibling_umm and has_sibling_full


def calculate_musytarakah(heirs: List[HeirInput], tirkah: float,
                         notes: List[str]) -> CalculationResult:
    """
    Hitung Musytarakah
    
    Dalam kasus ini, saudara kandung/seayah berserikat dengan saudara seibu
    pada bagian 1/3, padahal normalnya mereka mahjub.
    
    Ini adalah pengecualian berdasarkan keputusan Umar bin Khattab RA
    """
    notes.append("🤝 Kasus Al-Musytarakah (Al-Himariyyah)")
    notes.append("   Saudara kandung/seayah berserikat dengan saudara seibu")
    notes.append("   pada bagian 1/3 (pengecualian)")
    notes.append("")
    
    # Implementation lengkap
    from app.core.calculator import FaroidCalculator
    from app.schemas.calculation import CalculationInput
    
    calc_input = CalculationInput(heirs=heirs, tirkah=tirkah)
    calculator = FaroidCalculator(calc_input)
    calculator.notes = notes
    result = calculator._calculate_normal()
    
    result.is_special_case = True
    result.special_case_name = "Al-Musytarakah (Al-Himariyyah)"
    
    return result
