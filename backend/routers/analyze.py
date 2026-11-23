import os
import uuid
import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from PIL import Image

from core.config import get_settings
from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.analysis import Analysis
from schemas.analysis import AnalysisResponse
from services.ai_service import analyze_image

settings = get_settings()
router = APIRouter(prefix="/api/analyze", tags=["Analisis"])

ALLOWED_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_BYTES = settings.MAX_FILE_SIZE_MB * 1024 * 1024


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload gambar sampah dan jalankan analisis AI.

    - Format yang diterima: JPG, PNG, WEBP
    - Ukuran maksimal: 5 MB
    """
    # ── Validasi content-type ──────────────────────────────────────────────────
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Format file tidak didukung ({file.content_type}). Gunakan JPG, PNG, atau WEBP.",
        )

    # ── Baca & validasi ukuran ─────────────────────────────────────────────────
    contents = await file.read()
    if len(contents) > MAX_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Ukuran file melebihi batas {settings.MAX_FILE_SIZE_MB} MB.",
        )

    # ── Validasi gambar via Pillow ─────────────────────────────────────────────
    try:
        from io import BytesIO
        img = Image.open(BytesIO(contents))
        img.verify()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File bukan gambar yang valid atau rusak.",
        )

    # ── Simpan file ke uploads/ ────────────────────────────────────────────────
    ext = Path(file.filename).suffix.lower() or ".jpg"
    unique_name = f"{uuid.uuid4().hex}{ext}"
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / unique_name

    with open(file_path, "wb") as f_out:
        f_out.write(contents)

    # ── Jalankan AI service ────────────────────────────────────────────────────
    try:
        result = await analyze_image(str(file_path))
    except Exception as exc:
        # Hapus file jika AI gagal total
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analisis gagal: {str(exc)}",
        )

    # ── Simpan ke database ─────────────────────────────────────────────────────
    recommendation_json = json.dumps(
        result.get("recommendation", {}), ensure_ascii=False
    )

    analysis = Analysis(
        user_id=current_user.id,
        filename=file.filename,
        image_path=f"uploads/{unique_name}",
        waste_name=result.get("waste_name"),
        category=result.get("category"),
        material=result.get("material"),
        description=result.get("description"),
        confidence=result.get("confidence"),
        recommendation=recommendation_json,
        is_mock=result.get("is_mock", True),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # ── Kembalikan response dengan recommendation sebagai dict ─────────────────
    response_data = AnalysisResponse.model_validate(analysis)
    try:
        response_data.recommendation = json.loads(analysis.recommendation)
    except Exception:
        pass

    return response_data
