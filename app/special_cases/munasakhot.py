from __future__ import annotations

"""
Munasakhot (المناسخات) - Warisan Bertingkat
Kasus: Ahli waris meninggal sebelum pembagian warisan selesai
"""

from typing import List, Dict, Any
from app.schemas.calculation import CalculationResult, HeirShare
from app.schemas.heir import HeirInput, HeirResponse
from app.core.calculator import FaroidCalculator
from app.schemas.calculation import CalculationInput
from app.utils.constants import HEIR_NAMES


class MunasakhotCase:
    """Class untuk menangani kasus Munasakhot"""
    
    def __init__(self):
        self.levels = []  # Tingkatan pewaris
        self.results = {}  # Hasil perhitungan per tingkat
        
    def add_level(self, pewaris_name: str, tirkah: float, 
                  heirs: List[HeirInput], level: int = 1):
        """
        Tambahkan tingkat pewaris
        
        Args:
            pewaris_name: Nama pewaris
            tirkah: Harta yang akan dibagi
            heirs: Ahli waris
            level: Tingkat ke berapa (1, 2, 3, dst)
        """
        self.levels.append({
            "level": level,
            "pewaris": pewaris_name,
            "tirkah": tirkah,
            "heirs": heirs
        })
    
    def calculate(self) -> Dict[str, CalculationResult]:
        """
        Hitung munasakhot untuk semua tingkat
        
        Returns:
            Dict berisi hasil perhitungan per tingkat
        """
        results = {}
        
        for level_data in self.levels:
            level = level_data["level"]
            pewaris = level_data["pewaris"]
            tirkah = level_data["tirkah"]
            heirs = level_data["heirs"]
            
            # Hitung warisan untuk tingkat ini
            notes = []
            notes.append(f"{'='*60}")
            notes.append(f"📊 TINGKAT {level}: Warisan {pewaris}")
            notes.append(f"{'='*60}")
            notes.append(f"Harta yang dibagi: Rp {tirkah:,.0f}")
            notes.append("")
            
            calc_input = CalculationInput(heirs=heirs, tirkah=tirkah)
            calculator = FaroidCalculator(calc_input)
            calculator.notes = notes
            result = calculator._calculate_normal()
            
            # Simpan hasil
            results[f"tingkat_{level}_{pewaris}"] = result
            
        return results


def calculate_munasakhot(levels_data: List[Dict[str, Any]], 
                        notes: List[str]) -> Dict[str, CalculationResult]:
    """
    Hitung Munasakhot (warisan bertingkat)
    
    Contoh kasus:
    1. A meninggal, meninggalkan B, C, D sebagai ahli waris
    2. Sebelum warisan A dibagi, B meninggal
    3. Warisan B (termasuk bagian dari A) dibagi ke ahli waris B
    
    Args:
        levels_data: List data tingkatan warisan
            Format: [
                {
                    "pewaris": "Ahmad",
                    "tirkah": 100000000,
                    "heirs": [...],
                    "level": 1
                },
                {
                    "pewaris": "Budi (ahli waris Ahmad)",
                    "tirkah": 50000000,  # Bagian dari Ahmad + harta sendiri
                    "heirs": [...],
                    "level": 2
                }
            ]
        notes: List untuk catatan perhitungan
        
    Returns:
        Dict hasil perhitungan per tingkat
    """
    notes.append("🔗 Kasus MUNASAKHOT (Warisan Bertingkat)")
    notes.append("")
    notes.append("📋 Penjelasan:")
    notes.append("   • Munasakhot terjadi ketika ahli waris meninggal")
    notes.append("     sebelum pembagian warisan selesai")
    notes.append("   • Bagian ahli waris yang meninggal diwariskan lagi")
    notes.append("     kepada ahli warisnya sendiri")
    notes.append("")
    notes.append(f"   Jumlah tingkatan: {len(levels_data)}")
    notes.append("")
    
    # Buat instance Munasakhot
    munasakhot = MunasakhotCase()
    
    # Tambahkan semua tingkat
    for level_data in levels_data:
        munasakhot.add_level(
            pewaris_name=level_data["pewaris"],
            tirkah=level_data["tirkah"],
            heirs=level_data["heirs"],
            level=level_data.get("level", 1)
        )
    
    # Hitung
    results = munasakhot.calculate()
    
    # Tambahkan catatan ringkasan
    notes.append("")
    notes.append("="*60)
    notes.append("📝 RINGKASAN MUNASAKHOT")
    notes.append("="*60)
    
    for key, result in results.items():
        notes.append(f"\n{key.upper()}:")
        notes.append(f"  Status: {result.status}")
        notes.append(f"  Total yang dibagi: Rp {result.tirkah:,.0f}")
        notes.append(f"  Jumlah ahli waris: {len(result.shares)}")
    
    notes.append("")
    notes.append("⚖️ CARA KERJA MUNASAKHOT:")
    notes.append("   1. Hitung warisan tingkat pertama (pewaris awal)")
    notes.append("   2. Tentukan bagian ahli waris yang meninggal")
    notes.append("   3. Bagian tersebut + harta pribadi = tirkah tingkat kedua")
    notes.append("   4. Hitung warisan tingkat kedua untuk ahli warisnya")
    notes.append("   5. Lanjutkan untuk tingkat berikutnya (jika ada)")
    
    return results


def calculate_munasakhot_simple(pewaris1_data: Dict, pewaris2_data: Dict,
                                notes: List[str]) -> Dict[str, CalculationResult]:
    """
    Versi sederhana Munasakhot untuk 2 tingkat
    
    Args:
        pewaris1_data: Data pewaris pertama
            {
                "name": "Ahmad",
                "tirkah": 100000000,
                "heirs": [...]
            }
        pewaris2_data: Data pewaris kedua (ahli waris dari pewaris 1)
            {
                "name": "Budi",
                "bagian_dari_pewaris1": 30000000,
                "harta_sendiri": 20000000,
                "heirs": [...]
            }
        notes: List catatan
        
    Returns:
        Dict hasil perhitungan
    """
    # Tingkat 1: Pewaris pertama
    notes.append("🔗 MUNASAKHOT SEDERHANA (2 Tingkat)")
    notes.append("")
    notes.append("="*60)
    notes.append(f"📊 TINGKAT 1: {pewaris1_data['name']}")
    notes.append("="*60)
    
    calc_input_1 = CalculationInput(
        heirs=pewaris1_data["heirs"],
        tirkah=pewaris1_data["tirkah"]
    )
    calculator_1 = FaroidCalculator(calc_input_1)
    result_1 = calculator_1.calculate()
    
    # Tingkat 2: Ahli waris yang meninggal
    bagian_dari_pewaris1 = pewaris2_data.get("bagian_dari_pewaris1", 0)
    harta_sendiri = pewaris2_data.get("harta_sendiri", 0)
    tirkah_2 = bagian_dari_pewaris1 + harta_sendiri
    
    notes.append("")
    notes.append("="*60)
    notes.append(f"📊 TINGKAT 2: {pewaris2_data['name']}")
    notes.append("="*60)
    notes.append(f"Bagian dari {pewaris1_data['name']}: Rp {bagian_dari_pewaris1:,.0f}")
    notes.append(f"Harta sendiri: Rp {harta_sendiri:,.0f}")
    notes.append(f"Total Tirkah: Rp {tirkah_2:,.0f}")
    notes.append("")
    
    calc_input_2 = CalculationInput(
        heirs=pewaris2_data["heirs"],
        tirkah=tirkah_2
    )
    calculator_2 = FaroidCalculator(calc_input_2)
    result_2 = calculator_2.calculate()
    
    return {
        "pewaris_1": result_1,
        "pewaris_2": result_2
    }


# Contoh penggunaan
def example_munasakhot():
    """
    Contoh kasus Munasakhot:
    
    Kasus:
    - Ahmad meninggal dengan harta Rp 120.000.000
    - Ahli waris: Istri, Anak laki-laki (Budi), Anak perempuan (Siti)
    - Sebelum warisan dibagi, Budi meninggal
    - Budi memiliki harta sendiri Rp 30.000.000
    - Ahli waris Budi: Istri dan 1 anak laki-laki
    """
    from app.utils.constants import HeirID
    
    # Data pewaris pertama (Ahmad)
    pewaris1 = {
        "name": "Ahmad",
        "tirkah": 120_000_000,
        "heirs": [
            HeirInput(id=HeirID.ZAWJAH, quantity=1),  # Istri
            HeirInput(id=HeirID.IBN, quantity=1),      # Budi (akan meninggal)
            HeirInput(id=HeirID.BINT, quantity=1)      # Siti
        ]
    }
    
    # Hitung dulu untuk tahu bagian Budi
    # Istri = 1/8, Budi:Siti = 2:1
    # Ashl = 8, Istri=1, Sisa=7, Budi=7*2/3=14/3, Siti=7*1/3=7/3
    bagian_budi = (120_000_000 * 14/3) / 8  # Sekitar 70 juta
    
    # Data pewaris kedua (Budi)
    pewaris2 = {
        "name": "Budi (anak Ahmad)",
        "bagian_dari_pewaris1": bagian_budi,
        "harta_sendiri": 30_000_000,
        "heirs": [
            HeirInput(id=HeirID.ZAWJAH, quantity=1),  # Istri Budi
            HeirInput(id=HeirID.IBN, quantity=1)       # Anak Budi
        ]
    }
    
    notes = []
    results = calculate_munasakhot_simple(pewaris1, pewaris2, notes)
    
    return results
