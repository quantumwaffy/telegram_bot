import requests
from bs4 import BeautifulSoup, NavigableString

SOURCE = "https://myfin.by/currency/"

CITIES = {
    "1": ("minsk", "Минск"),
    "2": ("brest", "Брест"),
    "3": ("vitebsk", "Витебск"),
    "4": ("gomel", "Гомель"),
    "5": ("grodno", "Гродно"),
    "6": ("mogilev", "Могилев"),
}

PROPOSAL = (
    ("usd_buy", "best_usd_buy"),
    ("usd_sell", "best_usd_sell"),
    ("euro_buy", "best_euro_buy"),
    ("euro_sell", "best_euro_sell"),
    ("rub_buy", "best_rub_buy"),
    ("rub_sell", "best_rub_sell"),
    ("usd_buy_from euro", "best_usd_buy_from euro"),
    ("usd_sell_from euro", "best_usd_sell_from euro"),
)


def make_soup(data):
    city = CITIES.get(data)[0]
    if city:
        file = "temporary_" + city + ".html"
        url = SOURCE + city
        response = requests.get(url, headers={"User-agent": "your bot 0.1"})
        with open(file, "w") as f:
            f.write(str(BeautifulSoup(response.text, "lxml")))
            print(url)
        return file


def parsing_soup(file):
    dict_currency = {}
    dict_best_currency = {}

    with open(file) as f:
        html = f.read()
    soup = BeautifulSoup(html, "lxml")
    table_currnecy = soup.find("tbody", {"id": "currency_tbody"})
    banks = table_currnecy.findAll("tr")
    bank_name = ""
    for bank in banks:
        if bank.has_attr("data-bank_id"):
            for td in bank:
                if not isinstance(td, NavigableString):
                    if td.find("span"):
                        bank_name = td.find("span").get_text()
                        dict_currency[bank_name] = {}
                        dict_best_currency[bank_name] = {}
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[0][0]):
                        dict_currency[bank_name].update({PROPOSAL[0][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[0][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[1][0]):
                        dict_currency[bank_name].update({PROPOSAL[1][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[1][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[2][0]):
                        dict_currency[bank_name].update({PROPOSAL[2][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[2][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[3][0]):
                        dict_currency[bank_name].update({PROPOSAL[3][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[3][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[4][0]):
                        dict_currency[bank_name].update({PROPOSAL[4][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[4][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[5][0]):
                        dict_currency[bank_name].update({PROPOSAL[5][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[5][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[6][0]):
                        dict_currency[bank_name].update({PROPOSAL[6][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[6][1]: td.get_text()})
                        continue
                    if not dict_currency[bank_name].get(PROPOSAL[7][0]):
                        dict_currency[bank_name].update({PROPOSAL[7][0]: td.get_text()})
                        if td.has_attr("class") and td.attrs["class"][0] == "best":
                            dict_best_currency[bank_name].update({PROPOSAL[7][1]: td.get_text()})
                        continue

    dict_best_currency = {bank: currencies for bank, currencies in dict_best_currency.items() if currencies}

    return [dict_currency, dict_best_currency]


def print_banks(dict_currency, chosen_currency=None):
    dynamic_dict = {}
    if chosen_currency == PROPOSAL[0][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[0][1]
        }
    elif chosen_currency == PROPOSAL[1][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[1][1]
        }
    elif chosen_currency == PROPOSAL[2][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[2][1]
        }
    elif chosen_currency == PROPOSAL[3][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[3][1]
        }
    elif chosen_currency == PROPOSAL[4][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[4][1]
        }
    elif chosen_currency == PROPOSAL[5][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[5][1]
        }
    elif chosen_currency == PROPOSAL[6][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[6][1]
        }
    elif chosen_currency == PROPOSAL[7][1]:
        dynamic_dict = {
            bank: {kind: value}
            for bank, currencies in dict_currency.items()
            for kind, value in currencies.items()
            if kind == PROPOSAL[7][1]
        }
    elif not chosen_currency:
        dynamic_dict = dict_currency
    return dynamic_dict


def user_input(choice, list_dicts):
    dynamic_dict = {}
    if choice == "c1":
        dynamic_dict.update(print_banks(list_dicts[0]))
    elif choice == "c2":
        dynamic_dict.update(print_banks(list_dicts[1]))
    elif choice == "c3":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[0][1]))
    elif choice == "c4":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[1][1]))
    elif choice == "c5":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[2][1]))
    elif choice == "c6":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[3][1]))
    elif choice == "c7":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[4][1]))
    elif choice == "c8":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[5][1]))
    elif choice == "c9":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[6][1]))
    elif choice == "c10":
        dynamic_dict.update(print_banks(list_dicts[1], chosen_currency=PROPOSAL[7][1]))
    return dynamic_dict
