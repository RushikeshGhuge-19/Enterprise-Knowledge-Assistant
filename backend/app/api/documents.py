from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.users import User
from app.services.document_service import DocumentService
from app.api.auth import get_current_user
from app.services.pdf_service import PDFService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Allow only PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Create uploads directory if it doesn't exist
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    # Save uploaded file
    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata in database
    document = DocumentService.create_document(
        db=db,
        filename=file.filename,
        filepath=str(file_path),
        uploaded_by=current_user.id
    )

    # Extract text from PDF
    extracted_pdf = PDFService.extract_text(str(file_path))

    # Temporary return for Day 2 testing
    return {
        "document_id": document.id,
        "filename": document.filename,
        "pages": extracted_pdf["pages"],
        "text": extracted_pdf["text"][:2000]  # Return only first 2000 chars
    }