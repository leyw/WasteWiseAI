from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GuideCreate(BaseModel):
    title: str
    category: Optional[str] = None
    content: str
    icon: Optional[str] = None


class GuideUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    icon: Optional[str] = None


class GuideResponse(BaseModel):
    id: int
    title: str
    category: Optional[str] = None
    content: str
    icon: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class GuideSummary(BaseModel):
    """Versi ringkas untuk daftar panduan — tanpa konten penuh."""
    id: int
    title: str
    category: Optional[str] = None
    icon: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
