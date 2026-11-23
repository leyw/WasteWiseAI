import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.analysis import Analysis
from schemas.analysis import AnalysisResponse, AnalysisSummary

router = APIRouter(prefix="/api/history", tags=["Riwayat"])


def _parse_recommendation(analysis: Analysis) -> AnalysisResponse:
    """Konversi objek Analysis ke AnalysisResponse dengan recommendation di-parse dari JSON."""
    response = AnalysisResponse.model_validate(analysis)
    if analysis.recommendation:
        try:
            response.recommendation = json.loads(analysis.recommendation)
        except Exception:
            pass
    return response


@router.get("", response_model=List[AnalysisSummary])
def get_history(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    category: Optional[str] = Query(default=None, description="Filter berdasarkan kategori"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ambil daftar riwayat analisis milik pengguna aktif (terbaru lebih dulu)."""
    query = db.query(Analysis).filter(Analysis.user_id == current_user.id)
    if category:
        query = query.filter(Analysis.category == category.lower())
    items = query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()
    return items


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_history_detail(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ambil detail satu riwayat analisis berdasarkan ID."""
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Riwayat analisis tidak ditemukan.",
        )
    return _parse_recommendation(analysis)


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Hapus satu riwayat analisis berdasarkan ID."""
    analysis = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id)
        .first()
    )
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Riwayat analisis tidak ditemukan.",
        )

    # Hapus file gambar jika ada
    from pathlib import Path
    image_file = Path(analysis.image_path)
    if image_file.exists():
        image_file.unlink(missing_ok=True)

    db.delete(analysis)
    db.commit()
