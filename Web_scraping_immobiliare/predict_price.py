import joblib
import pandas as pd

def predict_price():
    # carico modello
    model = joblib.load("Models/random_forest_model.pkl")

    # carico colonne
    with open("Models/columns.txt", "r", encoding="utf-8") as f:
        columns = [line.strip() for line in f]

    # raccolgo i valori dati dall'utente
    user_data = {}

    for col in columns:
        value = float(input(f"Inserisci valore per {col}: "))
        user_data[col] = value

    # creo DataFrame con stesso ordine colonne
    df = pd.DataFrame([user_data])[columns]

    # predizione
    prediction = model.predict(df)

    print("Prezzo stimato:", prediction[0])

if __name__ == "__main__":
    predict_price()