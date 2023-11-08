#!/usr/bin/env python3

"""
database.py: TODO: Headline...

TODO: Description...
"""

# Header.
__author__ = "Lennart Haack"
__email__ = "lennart-haack@mail.de"
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__date__ = "2023-11-06"
__status__ = "Prototype/Development/Production"

# Imports.
from dataclasses import dataclass
from datetime import datetime


class Database:
    ...


@dataclass
class Entry(Database):
    """
    Database: TODO: Headline...
    """
    url: str
    score: int
    user_score: int
    score_readable: str = None
    user_score_readable: str = None
    category: str = None
    last_updated: datetime = datetime.now()

    def __post_init__(self):
        self.score_readable = self._convert_scores(self.score)
        self.user_score_readable = self._convert_scores(self.user_score)

    @staticmethod
    def _convert_scores(score: int) -> str:
        scores = {
                0: "F",
                1: "E-",
                2: "E",
                3: "E+",
                4: "D-",
                5: "D",
                6: "D+",
                7: "C-",
                8: "C",
                9: "C+",
                10: "B-",
                11: "B",
                12: "B+",
                13: "A-",
                14: "A",
                15: "A+"
                }

        return scores[score]


if __name__ == "__main__":
    entry = Entry("https://example.com", 0, 0)
    # print(entry)
    print(chr(15 + 65))
