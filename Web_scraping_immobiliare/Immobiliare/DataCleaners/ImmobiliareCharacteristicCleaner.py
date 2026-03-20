from Abstractions.ICleaner import ICleaner
import pandas as pd

class ImmobiliareCharacteristicsCleaner(ICleaner):

    def __init__(self):
        self._parking_columns = []

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop(columns=["Dati catastali"])
        data = data.drop(columns=["Tipologia"])
        data = data.drop(columns=["Contratto"])
        data = data.drop(columns=["Disponibilità"])

        data["Piani edificio"] = data["Piani edificio"].fillna(1).astype(int)
        data["Anno di costruzione"] = data["Anno di costruzione"].fillna(1990).astype(int) #TODO riempire con 1990 non è corretto
        data["Anno non riportato"] = data["Anno di costruzione"].isna().astype(int)

        data["Arredato"] = data["Arredato"].map({'No': 0, 'Sì': 1}).fillna(0)
        data["Ascensore"] = data["Ascensore"].map({'No': 0, 'Sì': 1}).fillna(0)
        data["Balcone"] = data["Balcone"].map({'No': 0, 'Sì': 1}).fillna(0)
        data["Terrazzo"] = data["Terrazzo"].map({'No': 0, 'Sì': 1}).fillna(0)
        data["Cantina"] = data["Cantina"].map({'No': 0, 'Sì': 1}).fillna(0)
        data["Accesso disabili"] = data["Accesso disabili"].map({'No': 0, 'Sì': 1}).fillna(0)

        data["Locali"] = data["Locali"].map({'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '5+': 6})
        data["Camere da letto"] = data["Camere da letto"].map({'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '5+': 6}).fillna(1)
        data["Bagni"] = data["Bagni"].map({'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '5+': 6}).fillna(1)

        data["Piano"] = (
            data["Piano"]
            .astype("category")
            .cat.codes
            .add(1)
        )
        data["Cucina"] = (
            data["Cucina"]
            .astype("category")
            .cat.codes
            .add(1)
        )
        data["Giardino"] = (
            data["Giardino"]
            .astype("category")
            .cat.codes
            .add(1)
        )
        data["Stato"] = (
            data["Stato"]
            .astype("category")
            .cat.codes
            .add(1)
        )

        data["Superficie"] = (
            data["Superficie"]
            .str.replace(r"m².*", "", regex=True)
            .str.strip()
            .astype(float)
        )

        data_parcheggi = (
            data["Box, posti auto"]
            .str.findall(r"(\d+)\s+in\s+([^,]+)")
            .apply(lambda x: {cat.strip(): int(num) for num, cat in x} if isinstance(x, list) else {})
        )

        all_categories = set()  # uso set per evitare duplicati

        for d in data_parcheggi:
            all_categories.update(d.keys())

        self._parking_columns = list(all_categories)
        print(self._parking_columns)

        data_parcheggi = pd.json_normalize(data_parcheggi).fillna(0)
        data = pd.concat([data, data_parcheggi], axis=1)
        data = data.drop(columns=["Box, posti auto"])

        return data

    def get_cleaned_columns(self):
        cleaned_columns = ["Piani edificio",
                           "Arredato",
                           "Ascensore",
                           "Balcone",
                           "Terrazzo",
                           "Cantina",
                           "Accesso disabili",
                           "Locali",
                           "Camere da letto",
                           "Bagni",
                           "Piano",
                           "Cucina",
                           "Giardino",
                           "Stato",
                           "Superficie",
                           "Anno di costruzione",
                           "Anno non riportato"]
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(list(self._parking_columns))
        print(self._parking_columns)
        return list(cleaned_columns) + list(self._parking_columns)