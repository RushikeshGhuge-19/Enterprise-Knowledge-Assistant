from sqlalchemy.orm import Session

from app.services.document_service import DocumentService
from app.services.pdf_service import PDFService
from app.services.text_cleaner import TextCleaner
from app.services.chunk_service import ChunkService
from app.services.chunk_db_service import ChunkDBService


class IngestionService:

    @staticmethod
    def ingest_document(
        db: Session,
        filename: str,
        filepath: str,
        uploaded_by: int
    ):

        # Step 1 - Save document metadata
        document = DocumentService.create_document(
            db=db,
            filename=filename,
            filepath=filepath,
            uploaded_by=uploaded_by
        )

        # Step 2 - Extract PDF text
        pdf = PDFService.extract_text(filepath)

        # Step 3 - Clean text
        cleaned_text = TextCleaner.clean(pdf["text"])

        # Step 4 - Split into chunks
        chunks = ChunkService.chunk_text(cleaned_text)

        # Step 5 - Save chunks
        ChunkDBService.save_chunks(
            db=db,
            document_id=document.id,
            chunks=chunks
        )

        # Step 6 - Return summary
        return {
            "document_id": document.id,
            "filename": document.filename,
            "pages": pdf["pages"],
            "chunks_created": len(chunks),
            "status": "completed"
        }