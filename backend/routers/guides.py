from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.guide import Guide
from schemas.guide import GuideCreate, GuideUpdate, GuideResponse, GuideSummary

router = APIRouter(prefix="/api/guides", tags=["Panduan"])


@router.get("", response_model=List[GuideSummary])
def list_guides(
    category: Optional[str] = Query(default=None, description="Filter berdasarkan kategori"),
    db: Session = Depends(get_db),
):
    """Ambil daftar semua panduan. Tidak memerlukan autentikasi."""
    query = db.query(Guide)
    if category:
        query = query.filter(Guide.category == category.lower())
    return query.order_by(Guide.category, Guide.title).all()


@router.get("/{guide_id}", response_model=GuideResponse)
def get_guide(guide_id: int, db: Session = Depends(get_db)):
    """Ambil detail satu panduan berdasarkan ID. Tidak memerlukan autentikasi."""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Panduan tidak ditemukan.",
        )
    return guide


@router.post("", response_model=GuideResponse, status_code=status.HTTP_201_CREATED)
def create_guide(
    payload: GuideCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Buat panduan baru. Memerlukan autentikasi."""
    guide = Guide(**payload.model_dump())
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return guide


@router.put("/{guide_id}", response_model=GuideResponse)
def update_guide(
    guide_id: int,
    payload: GuideUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Update panduan yang ada. Memerlukan autentikasi."""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Panduan tidak ditemukan.",
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(guide, field, value)
    db.commit()
    db.refresh(guide)
    return guide


@router.delete("/{guide_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    """Hapus panduan. Memerlukan autentikasi."""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Panduan tidak ditemukan.",
        )
    db.delete(guide)
    db.commit()
