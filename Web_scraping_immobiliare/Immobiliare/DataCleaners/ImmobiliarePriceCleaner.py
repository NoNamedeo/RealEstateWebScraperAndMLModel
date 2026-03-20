from Abstractions.ICleaner import ICleaner
import pandas as pd

class ImmobiliarePriceCleaner(ICleaner):

    def __init__(self, is_asta=False):
        self.is_asta = is_asta

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.dropna(subset=["Prezzo"])
        data = data[data["Asta"] == self.is_asta]
        data = data.drop(columns=["Asta"])

        data["Prezzo"] = (
            data["Prezzo"]
            .str.replace("€", "", regex=False)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .astype(float)
        )

        return data

    def get_cleaned_columns(self):
        return ["Prezzo"]