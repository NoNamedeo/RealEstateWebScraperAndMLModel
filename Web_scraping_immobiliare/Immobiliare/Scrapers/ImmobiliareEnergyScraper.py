from Abstractions.IScraper import IScraper
from Enums.SearchBy import SearchBy

class ImmobiliareEnergyScraper(IScraper):

    def __init__(self):
        pass

    async def scrape(self, browser) -> dict:
        data = {}

        divs = await browser.find_elements(SearchBy.CLASS, "ListingDetail_divider__snZGM")
        energy_section = None
        button = None
        is_detailed = False
        div_children_number = 0

        for div in divs:
            div_children = await div.get_children()
            div_children_number = len(div_children)

            if len(div_children) > 0:
                div_title = div_children[0]
                if (await div_title.get_content()) == "Efficienza energetica" and div_children_number > 1:

                    energy_section = div_children[1]

                    if div_children_number > 2:
                        button = div_children[2]

                        section_attributes = await energy_section.get_attributes()
                        if section_attributes[1] == "Energy_wrapper__HX_mI":
                            is_detailed = True
                    break

        if div_children_number == 2:
            if not energy_section:
                return data

            energy_datas = await energy_section.get_children()

            for energy_data in energy_datas:
                pair = await energy_data.get_children()
                if len(pair) > 1:
                    title = await pair[0].get_content()
                    value = await pair[1].get_content()
                    data[title] = value

        elif div_children_number == 3:
            await button.click()

            datas = await browser.find_element(SearchBy.CLASS, "Energy_features__CAbwq")
            data_pairs = await datas.get_children()
            is_title = True
            title = None
            for data_line in data_pairs:
                if is_title:
                    is_title = False
                    title = await data_line.get_content()
                else:
                    is_title = True
                    data[title] = await data_line.get_content()

            if not is_detailed:
                efficiency_span = await browser.find_element(SearchBy.CLASS, "MainConsumptions_color__QLjS0.Rating_rating__BWzKs")
                efficiency = await efficiency_span.get_content()
                data["Classe energetica"] = efficiency

        return data