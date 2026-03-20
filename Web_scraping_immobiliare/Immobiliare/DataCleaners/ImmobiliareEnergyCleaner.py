from Abstractions.ICleaner import ICleaner
import pandas as pd

class ImmobiliareEnergyCleaner(ICleaner):

    def __init__(self):
        self._cleaned_columns = []

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        energy_class_order = ["A4", "A3", "A2", "A1", "A", "B", "C", "D", "E", "F", "G"]

        data["Riscaldamento"] = (
            data["Riscaldamento"]
            .astype("category")
            .cat.codes
            .add(1)
        )
        data["Certificazione energetica"] = (
            data["Certificazione energetica"]
            .astype("category")
            .cat.codes
            .add(1)
        )
        if data.__contains__("Climatizzazione"):
            self._cleaned_columns.append("Climatizzazione")
            data["Climatizzazione"] = (
                data["Climatizzazione"]
                .astype("category")
                .cat.codes
                .add(1)
            )
        if data.__contains__("Climatizzatore"):
            self._cleaned_columns.append("Climatizzatore")
            data["Climatizzatore"] = (
                data["Climatizzatore"]
                .astype("category")
                .cat.codes
                .add(1)
            )

        if data.__contains__("Classe energetica"):
            self._cleaned_columns.append("Classe energetica")
            data["Classe energetica"] = (
                pd.Categorical(data["Classe energetica"],
                               categories=energy_class_order,
                               ordered=True)
                .codes
            )
        if data.__contains__("Prestazione energetica del fabbricato"):
            self._cleaned_columns.append("Prestazione energetica del fabbricato")
            data["Prestazione energetica del fabbricato"] = (
                data["Prestazione energetica del fabbricato"]
                .astype("category")
                .cat.codes
                .add(1)
            )
        if data.__contains__("Indice prest. energetica rinnovabile"):
            self._cleaned_columns.append("Indice prest. energetica rinnovabile")
            data = data.drop(columns=["Indice prest. energetica rinnovabile"])

        return data

    def get_cleaned_columns(self):
        return self._cleaned_columns + ["Riscaldamento", "Certificazione energetica"]

        return ["Riscaldamento",
                "Certificazione energetica",
                "Climatizzazione",
                "Climatizzatore",
                "Classe energetica",
                "Prestazione energetica del fabbricato"]