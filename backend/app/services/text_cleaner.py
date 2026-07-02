import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n+", "\n", text)

        # Remove tabs
        text = text.replace("\t", " ")

        return text.strip()