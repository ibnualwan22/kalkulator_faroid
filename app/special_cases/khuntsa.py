from __future__ import annotations

"""
Perhitungan untuk Khuntsa (Hermafrodit/Banci)
Ketika jenis kelamin ahli waris tidak jelas
"""

from typing import List, Dict
from app.schemas.calculation import CalculationResult
from app.schemas.heir import HeirInput
from app.core.calculator import FaroidCalculator
from app.schemas.calculation import CalculationInput


def calculate_khuntsa(heirs: List[HeirInput], tirkah: float,
                      khuntsa_heir_id: int, notes: List[str]) -> Dict[str, CalculationResult]:
    """
    Hitung dua skenario untuk Khuntsa:
    1. Skenario dianggap laki-laki
    2. Skenario dianggap perempuan
    
    Args:
        heirs: List ahli waris
        tirkah: Total harta
        khuntsa_heir_id: ID ahli waris yang khuntsa
        notes: Notes perhitungan
        
    Returns:
        Dict dengan key "laki_laki" dan "perempuan"
    """
    notes.append("⚧ Kasus KHUNTSA (Hermafrodit)")
    notes.append(f"   Ahli waris dengan ID {khuntsa_heir_id} jenis kelaminnya tidak jelas")
    notes.append("")
    notes.append("📋 Perhitungan dibuat untuk 2 skenario:")
    notes.append("")
    
    # Skenario 1: Dianggap Laki-laki
    notes_laki = notes.copy()
    notes_laki.append("📘 SKENARIO 1: Dianggap Laki-laki")
    notes_laki.append("")
    
    calc_input_male = CalculationInput(heirs=heirs, tirkah=tirkah)
    calculator_male = FaroidCalculator(calc_input_male)
    calculator_male.notes = notes_laki
    result_male = calculator_male._calculate_normal()
    
    # Skenario 2: Dianggap Perempuan
    notes_perempuan = notes.copy()
    notes_perempuan.append("📙 SKENARIO 2: Dianggap Perempuan")
    notes_perempuan.append("")
    
    calc_input_female = CalculationInput(heirs=heirs, tirkah=tirkah)
    calculator_female = FaroidCalculator(calc_input_female)
    calculator_female.notes = notes_perempuan
    result_female = calculator_female._calculate_normal()
    
    # Tambahkan catatan
    result_male.notes.append("")
    result_male.notes.append("⚖️ KETENTUAN KHUNTSA:")
    result_male.notes.append("   • Khuntsa mendapat bagian MINIMUM dari 2 skenario")
    result_male.notes.append("   • Ahli waris lain mendapat bagian MAKSIMUM dari 2 skenario")
    result_male.notes.append("   • Jika jenis kelamin diketahui kemudian, dilakukan pembagian ulang")
    
    result_female.notes = result_male.notes.copy()
    
    return {
        "laki_laki": result_male,
        "perempuan": result_female
    }
