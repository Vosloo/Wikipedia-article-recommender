import re
from bs4 import BeautifulSoup

# ---
# Regex patterns
# ---

# Separate merged words (with dot if present)
REGEX_SMALL_LARGE = (rf"([a-z])(\.*)([A-Z])", r"\1\2 \3")
REGEX_NUMBER_LARGE = (r"([0-9])(\.*)([A-Z])", r"\1\2 \3")

# Escape special characters
REGEX_COMMA = (",", ", ")
REGEX_ANGLE_BRACKETS = (r"[<>]", " ")
REGEX_DASHES = (r"[‑–]", "-")
REGEX_SPECIAL_SPACE = (r"[\t\xa0]", " ")
REGEX_SPECIAL_NEWLINE = (r"[\x03\r]", "\n")

# Wikipedia specifics
REGEX_WIKI_STYLING = (r"{.+?}", "")
REGEX_WIKI_BRACKETS = (r"}+", "")
REGEX_WIKI_ANNONATIONS = (r"\[\d+?\]", "")

# Multiple new lines and whitespaces
REGEX_SPACES_NEWLINES = (r"\s*\n\s*", "\n")
REGEX_MULTIP_NEWLINES = (r"\n{3,}", "\n\n")
REGEX_MULTIP_SPACES = (r"( ){2,}", " ")

# After lemma cleaning
REGEX_SPECIAL_CHARS = (r"[;`']", "")


class Purifier:
    def process_paragraphs(self, text) -> str:
        """
        Returns list of all paragraphs
        To find tags:
            <p>...</p>
        Returns:
            str: list with all found matching Tags
        """

        soup = BeautifulSoup(text, "html.parser")
        return "".join([tag.text for tag in soup.find_all("p")])

    def purify_after_lemma(self, text):
        text = re.sub(*REGEX_SPECIAL_CHARS, text)
        text = re.sub(*REGEX_MULTIP_SPACES, text)

        return "".join(text.strip())

    def purify_text(self, text: str):
        """
        Removes whitespaces, special (and problematic characters) and seperates words from the text
        """
        # Seperate merged words
        text = re.sub(*REGEX_SMALL_LARGE, text)
        text = re.sub(*REGEX_NUMBER_LARGE, text)

        # Escape special characters
        text = re.sub(*REGEX_COMMA, text)
        text = re.sub(*REGEX_ANGLE_BRACKETS, text)
        text = re.sub(*REGEX_DASHES, text)
        text = re.sub(*REGEX_SPECIAL_SPACE, text)
        text = re.sub(*REGEX_SPECIAL_NEWLINE, text)

        # Multiple new lines and whitespaces
        text = re.sub(*REGEX_SPACES_NEWLINES, text)
        text = re.sub(*REGEX_MULTIP_NEWLINES, text)
        text = re.sub(*REGEX_MULTIP_SPACES, text)
        text = re.sub(*REGEX_WIKI_STYLING, text)
        text = re.sub(*REGEX_WIKI_BRACKETS, text)
        text = re.sub(*REGEX_WIKI_ANNONATIONS, text)

        return text.strip()
