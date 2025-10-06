from __future__ import annotations

"""
Schemas untuk Perhitungan Warisan
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .heir import HeirInput, HeirResponse


class CalculationInput(BaseModel):
    """Schema untuk input perhitungan warisan"""
    heirs: List[HeirInput] = Field(..., description="Daftar ahli waris")
    tirkah: float = Field(..., description="Jumlah harta warisan (tirkah)", gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "heirs": [
                    {"id": 3, "quantity": 1},  # Suami
                    {"id": 18, "quantity": 1}, # Ibu
                    {"id": 16, "quantity": 2}  # Anak perempuan
                ],
                "tirkah": 100000000
            }
        }


class HeirShare(BaseModel):
    """Schema untuk bagian ahli waris"""
    heir: HeirResponse = Field(..., description="Info ahli waris")
    quantity: int = Field(..., description="Jumlah ahli waris")
    fardh: Optional[str] = Field(None, description="Bagian fardh (1/2, 1/4, dll)")
    share_fraction: str = Field(..., description="Pecahan bagian (misal: 3/12)")
    saham: float = Field(..., description="Jumlah saham")
    reason: str = Field(..., description="Alasan hukum pembagian")
    share_amount: float = Field(..., description="Bagian dalam rupiah")
    percentage: Optional[str] = Field(None, description="Persentase bagian")
    is_mahjub: bool = Field(False, description="Apakah terhalang (mahjub)")
    mahjub_reason: Optional[str] = Field(None, description="Alasan terhalang")
    
    class Config:
        json_schema_extra = {
            "example": {
                "heir": {
                    "id": 3,
                    "name_id": "Suami",
                    "name_ar": "زوج"
                },
                "quantity": 1,
                "fardh": "1/2",
                "share_fraction": "6/12",
                "saham": 6,
                "reason": "Suami mendapat 1/2 karena pewaris tidak memiliki anak",
                "share_amount": 50000000,
                "percentage": "50.00%",
                "is_mahjub": False
            }
        }


class CalculationResult(BaseModel):
    """Schema untuk hasil perhitungan warisan"""
    tirkah: float = Field(..., description="Total harta warisan")
    ashlul_masalah_awal: int = Field(..., description="Ashl al-mas'alah awal (KPK penyebut)")
    ashlul_masalah_akhir: int = Field(..., description="Ashl al-mas'alah akhir (setelah 'aul/radd)")
    total_saham: float = Field(..., description="Total saham dari semua ahli waris")
    
    # Status pembagian
    status: str = Field(..., description="Status: Adil, 'Aul, atau Radd")
    is_aul: bool = Field(False, description="Apakah terjadi 'Aul")
    is_radd: bool = Field(False, description="Apakah terjadi Radd")
    aul_type: Optional[str] = Field(None, description="Jenis 'Aul jika terjadi")
    
    # Special cases
    is_special_case: bool = Field(False, description="Apakah termasuk kasus khusus")
    special_case_name: Optional[str] = Field(None, description="Nama kasus khusus")
    
    # Bagian ahli waris
    shares: List[HeirShare] = Field(..., description="Bagian masing-masing ahli waris")
    
    # Catatan perhitungan
    notes: List[str] = Field(default_factory=list, description="Catatan langkah perhitungan")
    
    # Metadata
    calculation_metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata perhitungan")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tirkah": 100000000,
                "ashlul_masalah_awal": 12,
                "ashlul_masalah_akhir": 12,
                "total_saham": 12,
                "status": "Adil",
                "is_aul": False,
                "is_radd": False,
                "is_special_case": False,
                "shares": [
                    {
                        "heir": {"id": 3, "name_id": "Suami", "name_ar": "زوج"},
                        "quantity": 1,
                        "fardh": "1/4",
                        "share_fraction": "3/12",
                        "saham": 3,
                        "reason": "Suami mendapat 1/4 karena ada anak",
                        "share_amount": 25000000,
                        "percentage": "25.00%"
                    }
                ],
                "notes": [
                    "Menentukan furudh ahli waris",
                    "Menghitung ashl al-mas'alah: 12",
                    "Distribusi harta warisan"
                ]
            }
        }
