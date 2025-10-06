from __future__ import annotations

"""
API Endpoints untuk Data Ahli Waris
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.heir import HeirResponse
from app.schemas.response import APIResponse
from app.utils.constants import HeirID, HEIR_NAMES

router = APIRouter()


@router.get(
    "/",
    response_model=APIResponse[List[HeirResponse]],
    summary="Dapatkan Semua Ahli Waris",
    description="Endpoint untuk mendapatkan daftar semua ahli waris yang tersedia"
)
async def get_all_heirs() -> APIResponse[List[HeirResponse]]:
    """
    Dapatkan daftar semua ahli waris
    
    **Output:**
    - List semua ahli waris dengan ID, nama Indonesia, dan nama Arab
    """
    heirs = []
    
    for heir_id in HeirID:
        if heir_id in HEIR_NAMES:
            heir_info = HEIR_NAMES[heir_id]
            heirs.append(
                HeirResponse(
                    id=heir_id,
                    name_id=heir_info["id"],
                    name_ar=heir_info["ar"]
                )
            )
    
    return APIResponse(
        status="success",
        message=f"Berhasil mengambil {len(heirs)} ahli waris",
        data=heirs
    )


@router.get(
    "/{heir_id}",
    response_model=APIResponse[HeirResponse],
    summary="Dapatkan Detail Ahli Waris",
    description="Endpoint untuk mendapatkan detail satu ahli waris berdasarkan ID"
)
async def get_heir_by_id(heir_id: int) -> APIResponse[HeirResponse]:
    """
    Dapatkan detail ahli waris berdasarkan ID
    
    **Input:**
    - heir_id: ID ahli waris (1-25)
    
    **Output:**
    - Detail ahli waris
    """
    if heir_id not in HEIR_NAMES:
        raise HTTPException(
            status_code=404,
            detail=f"Ahli waris dengan ID {heir_id} tidak ditemukan"
        )
    
    heir_info = HEIR_NAMES[heir_id]
    heir = HeirResponse(
        id=heir_id,
        name_id=heir_info["id"],
        name_ar=heir_info["ar"]
    )
    
    return APIResponse(
        status="success",
        message="Berhasil mengambil detail ahli waris",
        data=heir
    )
