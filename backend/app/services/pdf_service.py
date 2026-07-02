import fitz


class PDFService:

    @staticmethod
    def extract_text(file_path: str):

        document = fitz.open(file_path)

        full_text = ""

        for page in document:
            full_text += page.get_text()

        return {
            "text": full_text,
            "pages": len(document)
        }