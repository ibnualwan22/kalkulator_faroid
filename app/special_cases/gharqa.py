from __future__ import annotations

"""
Perhitungan untuk Gharqa/Hadm (Meninggal Bersamaan)
Ketika beberapa orang meninggal bersamaan (misal: kecelakaan, bencana)
"""

from typing import List, Dict
from app.schemas.calculation import CalculationResult
from app.schemas.heir import HeirInput


def calculate_gharqa(deceased_list: List[Dict], notes: List[str]) -> Dict[str, CalculationResult]:
    """
    Hitung warisan untuk kasus Gharqa (meninggal bersamaan)
    
    Aturan:
    - Jika tidak diketahui siapa yang meninggal duluan
    - Masing-masing dianggap tidak saling mewarisi
    - Setiap orang diwariskan kepada ahli warisnya masing-masing
    
    Args:
        deceased_list: List of deceased persons dengan harta dan ahli warisnya
        notes: Notes perhitungan
        
    Returns:
        Dict berisi hasil perhitungan untuk setiap orang yang meninggal
    """
    notes.append("🌊 Kasus GHARQA/HADM (Meninggal Bersamaan)")
    notes.append("")
    notes.append("📋 Ketentuan:")
    notes.append("   • Tidak diketahui siapa yang meninggal lebih dulu")
    notes.append("   • Mereka tidak saling mewarisi")
    notes.append("   • Masing-masing diwariskan kepada ahli warisnya yang hidup")
    notes.append("")
    
    results = {}
    
    for i, deceased in enumerate(deceased_list, 1):
        name = deceased.get("name", f"Pewaris {i}")
        tirkah = deceased.get("tirkah", 0)
        heirs = deceased.get("heirs", [])
        
        notes.append(f"{'='*50}")
        notes.append(f"Perhitungan untuk: {name}")
        notes.append(f"Harta: Rp {tirkah:,.0f}")
        notes.append("")
        
        # Hitung normal untuk masing-masing
        from app.core.calculator import FaroidCalculator
        from app.schemas.calculation import CalculationInput
        
        calc_input = CalculationInput(heirs=heirs, tirkah=tirkah)
        calculator = FaroidCalculator(calc_input)
        result = calculator.calculate()
        
        results[name] = result
        notes.extend(result.notes)
        notes.append("")
    
    return results
