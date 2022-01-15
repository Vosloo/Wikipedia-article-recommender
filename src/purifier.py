import re
from typing import List, Union

from bs4 import BeautifulSoup
from bs4.element import Tag
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.summarizers.lsa import LsaSummarizer

# GER_SM = "".join(["\u00E4", "\u00F6", "\u00FC", "\u00DF"])  # German small letters
# GER_LG = "".join(["\u00C4", "\u00D6", "\u00DC", "\u1E9E"])  # German large letters

# TOKENIZER_LANG = "german"
# SUMMARIZE_SENTENCE_COUNT = 10

# ---
# Regex patterns
# ---

# Separate merged words (with dot if present)
REGEX_SMALL_LARGE     = (rf"([a-z])(\.*)([A-Z])", r"\1\2 \3")
REGEX_NUMBER_LARGE    = (r"([0-9])(\.*)([A-Z])", r"\1\2 \3")

# Escape special characters
REGEX_COMMA           = (",", ", ")
REGEX_APOSTROPHE      = ("'", "`")
REGEX_PERCENTAGE      = ("%", "%%")
REGEX_ANGLE_BRACKETS  = (r"[<>]", " ")
REGEX_DASHES          = (r"[‑–]", "-")
REGEX_QUERY_BINDING   = (r"(:)([a-zA-Z0-9])", r"\1 \2") # Removes potential parameter bindings in SQLAlchemy
REGEX_SPECIAL_SPACE   = (r"[\t\xa0]", " ")
REGEX_SPECIAL_NEWLINE = (r"[\x03\r]", "\n")

# Multiple new lines and whitespaces
REGEX_SPACES_NEWLINES = (r"\s*\n\s*", "\n")
REGEX_MULTIP_NEWLINES = (r"\n{3,}", "\n\n")
REGEX_MULTIP_SPACES   = (r"( ){2,}", " ")


class Purifier:
    def __init__(self, text: str, text_limit=5000) -> None:
        self.soup = BeautifulSoup(text, "html.parser")
        # self.lsa_summarizer = LsaSummarizer()

        self.raw_text = self.soup.get_text()
        self.text_limit = text_limit

    def is_pdf(self) -> bool:
        """Returns True if document is a PDF file, False otherwise"""
        if re.search(r"PDF-[0-9]\.[0-9]", self.raw_text) is not None:
            return True

        return False

    def process_meta_tags(
        self, attribute: str = None, attr_list: Union[str, list] = None,
    ) -> dict:
        """
            Returns dictionary with cleared content of meta description 
            for given attribute and its values
        
            To find tags:
                <meta name="description" content="...">\n
                <meta name="keywords" content="...">
            attribute   = "name"
            attr_list   = ["description", "keywords"]
            Returns:
                dict: attribute as a key and its content as a value
        """
        tags = self._get_tag(tag="meta", attribute=attribute, attr_list=attr_list)

        meta_desc = {}
        if tags:
            for tag in tags:
                if content := self.purify_text(tag.get("content", "")):
                    meta_desc[tag[attribute]] = content

        return meta_desc

    def purify_text(self, text):
        """
        Removes whitespaces, special (and problematic characters) and seperates words from the text
        """
        # Seperate merged words
        text = re.sub(*REGEX_SMALL_LARGE, text)
        text = re.sub(*REGEX_NUMBER_LARGE, text)

        # Escape special characters
        text = re.sub(*REGEX_COMMA, text)
        text = re.sub(*REGEX_APOSTROPHE, text)
        text = re.sub(*REGEX_PERCENTAGE, text)
        text = re.sub(*REGEX_ANGLE_BRACKETS, text)
        text = re.sub(*REGEX_DASHES, text)
        text = re.sub(*REGEX_QUERY_BINDING, text)
        text = re.sub(*REGEX_SPECIAL_SPACE, text)
        text = re.sub(*REGEX_SPECIAL_NEWLINE, text)

        # Multiple new lines and whitespaces
        text = re.sub(*REGEX_SPACES_NEWLINES, text)
        text = re.sub(*REGEX_MULTIP_NEWLINES, text)
        text = re.sub(*REGEX_MULTIP_SPACES, text)

        # text = self._cut_above_limit(text)

        return text.strip()

    # def summarize_text(self, text: str) -> str:
    #     parser = PlaintextParser.from_string(text, Tokenizer(TOKENIZER_LANG))

    #     summarized = self.lsa_summarizer(
    #         parser.document, sentences_count=SUMMARIZE_SENTENCE_COUNT
    #     )
    #     summarized = "\n".join([str(sent) for sent in summarized])

    #     return summarized

    def _cut_above_limit(self, text: str):
        """Cuts the text to the text_limit upper bound if it's too long"""
        if len(text) > self.text_limit:
            text = text[: self.text_limit] + " [...]"

        return text

    def _get_tag(
        self, tag: str, attribute: str = None, attr_list: Union[str, list] = None,
    ) -> List[Tag]:
        """
            Returns list of all tags found for given attribute and its values
            To find tags:
                <meta name="description" content="...">\n
                <meta name="keywords" content="...">
            tag         = "meta"
            attribute   = "name"
            attr_list   = ["description", "keywords"]
            Returns:
                list: list with all found matching Tags
        """
        if attribute:
            if isinstance(attr_list, str):
                return self.soup.find_all(tag, attrs={attribute: attr_list})

            results = []
            for attr_val in attr_list:
                results.extend(self.soup.find_all(tag, attrs={attribute: attr_val}))

            return results

        return list(self.soup.find_all(tag))