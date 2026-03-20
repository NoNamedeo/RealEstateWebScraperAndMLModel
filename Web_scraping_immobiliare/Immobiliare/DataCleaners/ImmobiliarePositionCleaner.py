from Abstractions.ICleaner import ICleaner
import pandas as pd

class ImmobiliarePositionCleaner(ICleaner):

    def __init__(self, quarter_dimension = 0.005):
        self._quarter_dimension = quarter_dimension


    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        data["Latitudine"] = (data["Latitudine"] // self._quarter_dimension) * self._quarter_dimension
        data["Longitudine"] = (data["Longitudine"] // self._quarter_dimension) * self._quarter_dimension

        data["Pseudo-quartiere"] = data["Latitudine"].astype(str) + "_" + data["Longitudine"].astype(str)

        data = data.drop(columns=["Latitudine", "Longitudine"])

        data["Pseudo-quartiere"] = data["Pseudo-quartiere"].astype("category").cat.codes

        return data

    def get_cleaned_columns(self):
        return ["Pseudo-quartiere"]