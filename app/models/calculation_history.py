"""
Model untuk menyimpan history perhitungan
"""

from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base


class CalculationHistory(Base):
    """Model untuk history perhitungan warisan"""
    
    __tablename__ = "calculation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Input data
    heirs_input = Column(JSON, nullable=False, comment="Input ahli waris dalam format JSON")
    tirkah = Column(Float, nullable=False, comment="Total harta warisan")
    
    # Result data
    result_json = Column(JSON, nullable=False, comment="Hasil perhitungan dalam format JSON")
    
    # Metadata
    ashlul_masalah_awal = Column(Integer, nullable=True)
    ashlul_masalah_akhir = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True, comment="Adil, Aul, atau Radd")
    is_special_case = Column(Integer, default=0, comment="0=False, 1=True")
    special_case_name = Column(String(100), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True, comment="Catatan perhitungan")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<CalculationHistory(id={self.id}, tirkah={self.tirkah}, status={self.status})>"
