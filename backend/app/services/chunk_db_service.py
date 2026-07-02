from sqlalchemy.orm import Session

from app.models.chunk import Chunk


class ChunkDBService:

    @staticmethod
    def save_chunks(
        db: Session,
        document_id: int,
        chunks: list[str]
    ):

        for index, chunk in enumerate(chunks):

            db_chunk = Chunk(
                document_id=document_id,
                chunk_index=index,
                content=chunk
            )

            db.add(db_chunk)

        db.commit()