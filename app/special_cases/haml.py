from __future__ import annotations

"""
Perhitungan untuk Haml (Janin dalam Kandungan)
Kasus ketika pewaris meninggal dan ada istri yang hamil
"""

from typing import List, Dict
from app.schemas.calculation import CalculationResult, HeirShare
from app.schemas.heir import HeirInput
from app.core.calculator import FaroidCalculator
from app.utils.constants import HeirID


def calculate_haml(heirs: List[HeirInput], tirkah: float, 
                   notes: List[str]) -> Dict[str, CalculationResult]:
    """
    Hitung dua skenario untuk Haml:
    1. Skenario bayi laki-laki
    2. Skenario bayi perempuan
    
    Warisan ditahan (mauquf) sampai bayi lahir
    
    Returns:
        Dict dengan key "laki_laki" dan "perempuan"
    """
    notes.append("🤰 Kasus HAML (Janin dalam Kandungan)")
    notes.append("")
    notes.append("⚠️ Warisan DITAHAN (Mauquf) sampai bayi lahir")
    notes.append("   Perhitungan dibuat untuk 2 skenario:")
    notes.append("")
    
    # Skenario 1: Bayi Laki-laki
    notes_laki = notes.copy()
    notes_laki.append("📘 SKENARIO 1: Bayi Laki-laki")
    notes_laki.append("")
    
    heirs_with_boy = heirs.copy()
    heirs_with_boy.append(HeirInput(id=HeirID.IBN, quantity=1))
    
    from app.schemas.calculation import CalculationInput
    calc_input_boy = CalculationInput(heirs=heirs_with_boy, tirkah=tirkah)
    calculator_boy = FaroidCalculator(calc_input_boy)
    calculator_boy.notes = notes_laki
    result_boy = calculator_boy._calculate_normal()
    
    # Skenario 2: Bayi Perempuan
    notes_perempuan = notes.copy()
    notes_perempuan.append("📙 SKENARIO 2: Bayi Perempuan")
    notes_perempuan.append("")
    
    heirs_with_girl = heirs.copy()
    heirs_with_girl.append(HeirInput(id=HeirID.BINT, quantity=1))
    
    calc_input_girl = CalculationInput(heirs=heirs_with_girl, tirkah=tirkah)
    calculator_girl = FaroidCalculator(calc_input_girl)
    calculator_girl.notes = notes_perempuan
    result_girl = calculator_girl._calculate_normal()
    
    # Tambahkan catatan penting
    result_boy.notes.append("")
    result_boy.notes.append("⚖️ KETENTUAN HAML:")
    result_boy.notes.append("   • Warisan ditahan sampai bayi lahir")
    result_boy.notes.append("   • Setiap ahli waris mendapat bagian MINIMUM dari 2 skenario")
    result_boy.notes.append("   • Sisanya ditahan untuk bayi")
    result_boy.notes.append("   • Setelah lahir, dilakukan pembagian ulang sesuai jenis kelamin bayi")
    
    result_girl.notes = result_boy.notes.copy()
    
    return {
        "laki_laki": result_boy,
        "perempuan": result_girl
    }
