from enum import Enum

class SearchBy(Enum):
    CSS = 0
    XPATH = 1
    CLASS = 2
    ID = 3
    DICT_OF_QUERIES = 4
    RAW_ELEMENT = 5
    BEST_MATCH = 6