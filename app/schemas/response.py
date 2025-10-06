from __future__ import annotations

"""
Schemas untuk API Response
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Generic, TypeVar

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response"""
    status: str = Field(..., description="Status: success atau error")
    message: Optional[str] = Field(None, description="Pesan untuk user")
    data: Optional[T] = Field(None, description="Data hasil")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Perhitungan berhasil",
                "data": {}
            }
        }


class ErrorResponse(BaseModel):
    """Schema untuk error response"""
    status: str = Field("error", description="Status selalu 'error'")
    message: str = Field(..., description="Pesan error")
    detail: Optional[Any] = Field(None, description="Detail error")
    code: Optional[str] = Field(None, description="Error code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Input tidak valid",
                "detail": "Ahli waris tidak boleh kosong",
                "code": "INVALID_INPUT"
            }
        }
