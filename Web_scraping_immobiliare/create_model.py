import asyncio
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from Browsers.Nodriver.NodriverBrowser import NodriverBrowser
from Enums.SearchBy import SearchBy
from Immobiliare.DataCleaners.ImmobiliareCharacteristicCleaner import ImmobiliareCharacteristicsCleaner
from Immobiliare.DataCleaners.ImmobiliareEnergyCleaner import ImmobiliareEnergyCleaner
from Immobiliare.DataCleaners.ImmobiliarePositionCleaner import ImmobiliarePositionCleaner
from Immobiliare.DataCleaners.ImmobiliarePriceCleaner import ImmobiliarePriceCleaner
from Immobiliare.DataCleaners.ImmobiliareTitleCleaner import ImmobiliareTitleCleaner
from Immobiliare.Removers.ImmobiliareHomeCookieBannersRemover import ImmobiliareHomeCookieBannersRemover
from Immobiliare.Scrapers.ImmobiliareEnergyScraper import ImmobiliareEnergyScraper
from Immobiliare.Scrapers.ImmobiliarePriceScraper import ImmobiliarePriceScraper
from Immobiliare.Scrapers.ImmobiliareTitleScraper import ImmobiliareTitleScraper
from Immobiliare.Scrapers.ImmobiliareCharacteristicsScraper import ImmobiliareCharacteristicsScraper
from Immobiliare.Scrapers.ImmobiliarePositionScraper import ImmobiliarePositionScraper

async def create_model():

    #TODO: aggiungi tutte funzioni di sicurezza, ossia se fallisce qualcosa si comunica invece che lanciare eccezioni
    #TODO: aggiungi diversi user agents strings (stringhe che i browser usano per le richieste http, contengono info base)
    #TODO: usa diverse proxies (ip e proxy server rotanti)
    #TODO: sarebbe da farlo non hard-coded, quindi senza tutti gli asyncio sleep

    #DATA SCRAPING

    browser = NodriverBrowser()
    await browser.start()
    await browser.set_url("https://www.immobiliare.it/vendita-case/fabriano/")
      
    input("Completa il CAPTCHA e premi INVIO per continuare...")

    await ImmobiliareHomeCookieBannersRemover().remove(browser)

    scrapers = [ImmobiliarePriceScraper(),
                ImmobiliareTitleScraper(),
                ImmobiliareCharacteristicsScraper(),
                ImmobiliareEnergyScraper(),
                ImmobiliarePositionScraper()]
    data = {}
    is_not_finished = True
    i = 1

    while is_not_finished:
        flat_ads = await browser.find_elements(SearchBy.CSS, ".nd-mediaObject__content.PropertyContent_content__xMf_x")
        flat_data = {}

        for ad in flat_ads:
            print(f"Scraping page {i}:")
            await ad.click()
            await asyncio.sleep(3)
            await browser.switch_to_window((await browser.get_all_windows())[-1])

            for scraper in scrapers:
                result = await scraper.scrape(browser)
                flat_data = flat_data | result

            data[f"Appartamento numero {i}"] = flat_data
            i = i + 1
            flat_data = {}

            await browser.close_window()
            await browser.switch_to_window((await browser.get_all_windows())[0])

            #TODO: toglilo, era solo per farlo piu veloce
            if i == 13:
                break

        change_page_buttons = await browser.find_elements(SearchBy.CSS, ".PaginationItem_item__Wnh_o.nd-button.nd-button--ghost")
        next_page_button = change_page_buttons[-2]
        is_not_finished = False #TODO: questo qui è per solo la prima pagina, quello sotto per tutte
        #is_not_finished = not (await next_page_button.get_attributes())[1] == "nd-button nd-button--ghost is-disabled PaginationItem_item__Wnh_o"
        await next_page_button.click()

    print(data)

    #DATA CLEANING AND MACHINE LEARNING MODEL CREATION

    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    data = pd.DataFrame(data)
    data = data.T

    cleaners = [ImmobiliareCharacteristicsCleaner(),
                ImmobiliareEnergyCleaner(),
                ImmobiliarePositionCleaner(0.005),
                ImmobiliarePriceCleaner(False),
                ImmobiliareTitleCleaner()]

    print(data)

    cleaned_columns = []

    for cleaner in cleaners:
        data = cleaner.clean(data)
        cleaned_columns += cleaner.get_cleaned_columns()

    print(cleaned_columns)
    print(data)

    data = data[cleaned_columns]

    print(data)

    #scegli il modello di ml da creare (linear regression, random forest...)

    x = data.drop(columns=["Prezzo"])
    y = data["Prezzo"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    columns = x_train.columns.tolist()

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    model.fit(x_train, y_train)

    prediction = model.predict(x_test)
    print(mean_absolute_error(y_test, prediction))

    #salva il modello (o sostituisci il precedente)

    joblib.dump(model, "Models/random_forest_model.pkl")

    with open("Models/columns.txt", "w", encoding="utf-8") as f:
        for col in columns:
            f.write(col + "\n")

if __name__ == "__main__":
    asyncio.run(create_model())