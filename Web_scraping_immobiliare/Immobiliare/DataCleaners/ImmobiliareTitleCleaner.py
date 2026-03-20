from Abstractions.ICleaner import ICleaner
import pandas as pd

class ImmobiliareTitleCleaner(ICleaner):

    def __init__(self):
        pass

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop("Titolo", axis=1)

    def get_cleaned_columns(self):
        return []