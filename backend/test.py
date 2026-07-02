from app.services.text_cleaner import TextCleaner
from app.services.chunk_service import ChunkService

text = """

Hello



World


Enterprise Knowledge Assistant

"""

clean = TextCleaner.clean(text)

chunks = ChunkService.chunk_text(clean)

print(clean)

print(len(chunks))