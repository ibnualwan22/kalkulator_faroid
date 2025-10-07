# File: app/core/calculator_fix.py

"""
Fix untuk calculator.py - Return proper CalculationResult
"""

from app.schemas.calculation import CalculationResult


def create_error_result(tirkah: float, notes: list) -> CalculationResult:
    """
    Buat CalculationResult untuk error case yang valid
    
    Args:
        tirkah: Total harta warisan
        notes: Catatan error
        
    Returns:
        CalculationResult yang valid
    """
    return CalculationResult(
        # ✅ Required fields dari schema
        tirkah=tirkah,
        ashlul_masalah_awal=0,
        ashlul_masalah_akhir=0,
        total_saham=0,
        status="ERROR",
        
        # ✅ Default values
        is_aul=False,
        is_radd=False,
        is_special_case=False,
        
        # ✅ Empty shares
        shares=[],
        
        # ✅ Notes
        notes=notes
    )
