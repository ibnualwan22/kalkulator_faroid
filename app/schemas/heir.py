"""
Schemas untuk Ahli Waris
"""

from pydantic import BaseModel, Field
from typing import Optional


class HeirBase(BaseModel):
    """Base schema untuk ahli waris"""
    name_id: str = Field(..., description="Nama ahli waris dalam Bahasa Indonesia")
    name_ar: str = Field(..., description="Nama ahli waris dalam Bahasa Arab")


class HeirInput(BaseModel):
    """Schema untuk input ahli waris dalam perhitungan"""
    id: int = Field(..., description="ID ahli waris (sesuai HeirID)", ge=1, le=25)
    quantity: int = Field(1, description="Jumlah ahli waris dengan tipe ini", ge=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "quantity": 2
            }
        }


class HeirResponse(HeirBase):
    """Schema untuk response ahli waris"""
    id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name_id": "Anak Laki-laki",
                "name_ar": "ابن"
            }
        }
