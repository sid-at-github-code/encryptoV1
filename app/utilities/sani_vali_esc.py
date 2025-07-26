import re
from markupsafe import escape

class HazardProcessor:
    def sanitization(self, raw: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9., ]", " ", raw)
        return cleaned.lower()

    def validation(self, text: str) -> str:
        if re.search(r'[^a-zA-Z0-9 .,]', text):
            raise TypeError("Enter only alphabets, spaces, numbers, comma or dot.")
        return text

    def escaping(self, check: str) -> str:
        return escape(check)

    def process_all(self, raw: str) -> str:
        # Chained processing in one go
        step1 = self.sanitization(raw)
        step2 = self.validation(step1)
        final = self.escaping(step2)
        return final

if __name__=="__main__":
    check=HazardProcessor()

    raw="sidHFK67,/JKYmfi@@@u>L"

    raw=check.process_all(raw)
    print(raw)