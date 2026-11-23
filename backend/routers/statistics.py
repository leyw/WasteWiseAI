from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.analysis import Analysis

router = APIRouter(prefix="/api/statistics", tags=["Statistik"])

CATEGORY_LABELS = {
    "organik":    "Organik",
    "plastik":    "Plastik",
    "kertas":     "Kertas",
    "logam":      "Logam",
    "kaca":       "Kaca",
    "elektronik": "Elektronik",
    "b3":         "B3 / Limbah Berbahaya",
    "lainnya":    "Lainnya",
}


class CategoryStat(BaseModel):
    category: str
    label: str
    count: int


class StatisticsResponse(BaseModel):
    total_analyses: int
    categories: List[CategoryStat]
    top_category: str | None
    top_category_label: str | None
    top_category_count: int


@router.get("", response_model=StatisticsResponse)
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Statistik analisis sampah milik pengguna aktif."""
    total = db.query(func.count(Analysis.id)).filter(
        Analysis.user_id == current_user.id
    ).scalar() or 0

    # Jumlah per kategori
    rows = (
        db.query(Analysis.category, func.count(Analysis.id).label("cnt"))
        .filter(Analysis.user_id == current_user.id)
        .group_by(Analysis.category)
        .order_by(func.count(Analysis.id).desc())
        .all()
    )

    categories = [
        CategoryStat(
            category=row.category or "lainnya",
            label=CATEGORY_LABELS.get(row.category or "lainnya", row.category or "Lainnya"),
            count=row.cnt,
        )
        for row in rows
    ]

    top = categories[0] if categories else None

    return StatisticsResponse(
        total_analyses=total,
        categories=categories,
        top_category=top.category if top else None,
        top_category_label=top.label if top else None,
        top_category_count=top.count if top else 0,
    )
