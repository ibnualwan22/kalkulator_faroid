from __future__ import annotations

"""
API Endpoints untuk Perhitungan Warisan
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List
from app.schemas.calculation import CalculationInput, CalculationResult
from app.schemas.response import APIResponse, ErrorResponse
from app.core.calculator import calculate_inheritance

router = APIRouter()


@router.post(
    "/calculate",
    response_model=APIResponse[CalculationResult],
    status_code=status.HTTP_200_OK,
    summary="Hitung Warisan",
    description="Endpoint utama untuk menghitung pembagian warisan berdasarkan ahli waris dan tirkah"
)
async def calculate_faraid(calculation_input: CalculationInput) -> APIResponse[CalculationResult]:
    """
    Hitung pembagian warisan
    
    **Input:**
    - heirs: List ahli waris dengan ID dan jumlah
    - tirkah: Total harta warisan
    
    **Output:**
    - Hasil perhitungan lengkap dengan bagian masing-masing ahli waris
    - Notes langkah perhitungan
    - Informasi 'Aul, Radd, atau kasus khusus
    """
    try:
        # Validasi input
        if not calculation_input.heirs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ahli waris tidak boleh kosong"
            )
        
        if calculation_input.tirkah <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tirkah harus lebih besar dari 0"
            )
        
        # Hitung
        result = calculate_inheritance(calculation_input)
        
        return APIResponse(
            status="success",
            message="Perhitungan warisan berhasil",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan dalam perhitungan: {str(e)}"
        )


@router.post(
    "/calculate/haml",
    response_model=APIResponse[Dict[str, CalculationResult]],
    summary="Hitung Warisan dengan Haml (Janin)",
    description="Perhitungan untuk kasus ada janin dalam kandungan"
)
async def calculate_haml_case(calculation_input: CalculationInput) -> APIResponse[Dict[str, CalculationResult]]:
    """
    Hitung warisan dengan kasus Haml (janin dalam kandungan)
    
    Mengembalikan 2 skenario: bayi laki-laki dan bayi perempuan
    """
    try:
        from app.special_cases import calculate_haml
        
        notes = []
        results = calculate_haml(
            calculation_input.heirs,
            calculation_input.tirkah,
            notes
        )
        
        return APIResponse(
            status="success",
            message="Perhitungan Haml berhasil",
            data=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan: {str(e)}"
        )


@router.post(
    "/calculate/khuntsa",
    response_model=APIResponse[Dict[str, CalculationResult]],
    summary="Hitung Warisan dengan Khuntsa (Hermafrodit)",
    description="Perhitungan untuk kasus ahli waris hermafrodit"
)
async def calculate_khuntsa_case(
    calculation_input: CalculationInput,
    khuntsa_heir_id: int
) -> APIResponse[Dict[str, CalculationResult]]:
    """
    Hitung warisan dengan kasus Khuntsa
    
    Mengembalikan 2 skenario: dianggap laki-laki dan dianggap perempuan
    """
    try:
        from app.special_cases import calculate_khuntsa
        
        notes = []
        results = calculate_khuntsa(
            calculation_input.heirs,
            calculation_input.tirkah,
            khuntsa_heir_id,
            notes
        )
        
        return APIResponse(
            status="success",
            message="Perhitungan Khuntsa berhasil",
            data=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan: {str(e)}"
        )

@router.post(
    "/calculate/munasakhot",
    response_model=APIResponse[Dict[str, CalculationResult]],
    summary="Hitung Warisan Munasakhot (Bertingkat)",
    description="Perhitungan untuk kasus warisan bertingkat (ahli waris meninggal sebelum pembagian)"
)
async def calculate_munasakhot_case(
    levels_data: List[Dict[str, Any]]
) -> APIResponse[Dict[str, CalculationResult]]:
    """
    Hitung warisan Munasakhot (bertingkat)
    
    **Input Format:**
    ```
    [
        {
            "pewaris": "Ahmad",
            "tirkah": 100000000,
            "heirs": [
                {"id": 4, "quantity": 1},
                {"id": 1, "quantity": 1},
                {"id": 16, "quantity": 1}
            ],
            "level": 1
        },
        {
            "pewaris": "Budi (anak Ahmad)",
            "tirkah": 80000000,
            "heirs": [
                {"id": 4, "quantity": 1},
                {"id": 1, "quantity": 2}
            ],
            "level": 2
        }
    ]
    ```
    
    Mengembalikan hasil perhitungan untuk setiap tingkat
    """
    try:
        from app.special_cases import calculate_munasakhot
        
        notes = []
        results = calculate_munasakhot(levels_data, notes)
        
        return APIResponse(
            status="success",
            message="Perhitungan Munasakhot berhasil",
            data=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan: {str(e)}"
        )


@router.post(
    "/calculate/munasakhot-simple",
    response_model=APIResponse[Dict[str, CalculationResult]],
    summary="Hitung Warisan Munasakhot Sederhana (2 Tingkat)",
    description="Perhitungan sederhana untuk 2 tingkat warisan"
)
async def calculate_munasakhot_simple_case(
    pewaris1: Dict[str, Any],
    pewaris2: Dict[str, Any]
) -> APIResponse[Dict[str, CalculationResult]]:
    """
    Hitung warisan Munasakhot sederhana (2 tingkat)
    
    **Input Format:**
    ```
    {
        "pewaris1": {
            "name": "Ahmad",
            "tirkah": 100000000,
            "heirs": [...]
        },
        "pewaris2": {
            "name": "Budi",
            "bagian_dari_pewaris1": 40000000,
            "harta_sendiri": 20000000,
            "heirs": [...]
        }
    }
    ```
    """
    try:
        from app.special_cases import calculate_munasakhot_simple
        
        notes = []
        results = calculate_munasakhot_simple(pewaris1, pewaris2, notes)
        
        return APIResponse(
            status="success",
            message="Perhitungan Munasakhot sederhana berhasil",
            data=results
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan: {str(e)}"
        )