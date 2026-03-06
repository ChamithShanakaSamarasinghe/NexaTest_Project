import re

class ResponsePostProcessor:
    def clean(delf, text: str) -> str:
        """
        Cleans raw LLM output
        """

        #Removing trailing spaces
        text = text.strip()

        #Removing common LLM filler Phrases
        filler_patterns = [
            r"^sure[,!]*",
            r"^here(?:'s| is) the answer[:\-]*",
            r"^the answer is[:\-]*",
            r"^of course[,! ]*"
        ]

        for pattern in filler_patterns:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)

        #Removing multiple spaces
        return text.strip()