from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class RecommendationSchema(BaseModel):
    pemilahan: Optional[str] = None
    daur_ulang: Optional[str] = None
    persiapan: Optional[str] = None
    pembuangan: Optional[str] = None
    tips_pengurangan: Optional[str] = None


class AnalysisResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    image_path: str
    waste_name: Optional[str] = None
    category: Optional[str] = None
    material: Optional[str] = None
    description: Optional[str] = None
    confidence: Optional[float] = None
    recommendation: Optional[Any] = None   # dict setelah di-parse dari JSON
    is_mock: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AnalysisSummary(BaseModel):
    """Versi ringkas untuk daftar riwayat."""
    id: int
    filename: str
    image_path: str
    waste_name: Optional[str] = None
    category: Optional[str] = None
    is_mock: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
