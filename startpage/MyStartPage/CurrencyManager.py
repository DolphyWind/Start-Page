import requests
import threading
import datetime
from dataclasses import dataclass

@dataclass
class CurrencyData:
    target: str
    rate: int
    last_updated_day: int

class CurrencyManager:
    currency_dict: dict[str, CurrencyData]  = {}

    def __init__(self):
        self.api_url: str = "https://open.er-api.com/v6/latest/{}"
        self.currency_icons = {
            "TRY": "₺",
            "USD": "$",
            "EUR": "€",
            "INR": "₹",
            "GBP": "£",
        }
    def get_currency_icon(self, currency_name: str) -> str:
        """Returns the icon of the currency. Returns the currency itself if it has no icon"""
        if currency_name not in self.currency_icons.keys():
            return currency_name

        return self.currency_icons[currency_name]

    def fetch_currency(self, base_currency: str, target_currency: str) -> str:
        converted_currency = None
        current_day = datetime.datetime.now().day

        if base_currency in CurrencyManager.currency_dict.keys() and CurrencyManager.currency_dict[base_currency].last_updated_day == current_day and target_currency == CurrencyManager.currency_dict[base_currency].target:
            converted_currency = CurrencyManager.currency_dict[base_currency].rate
        else:
            full_url = self.api_url.format(base_currency)
            try:
                req = requests.get(full_url)
            except:
                return ""

            if not str(req.status_code).startswith('2'):
                return ""

            data = req.json()
            CurrencyManager.currency_dict[base_currency] = CurrencyData(target=target_currency, rate=data['rates'][target_currency], last_updated_day=current_day)
            if data["result"] != "success":
                return ""
            converted_currency = data['rates'][target_currency]

        base_currency = self.get_currency_icon(base_currency)
        target_currency = self.get_currency_icon(target_currency)

        if len(base_currency) != 1:
            base_currency = " " + base_currency
        if len(target_currency) != 1:
            target_currency = " " + target_currency

        return f"1{base_currency} = {round(converted_currency, 2)}{target_currency}"

    def fetch_multiple_currencies(self, currencyList: list[dict[str, str]]) -> list[str]:
        result: list = []
        for _ in currencyList:
            result.append(None)
        thread_list: list[threading.Thread] = []

        def fetch_currency_in_thread(base, target, index):
            result[index] = self.fetch_currency(base, target)

        for idx, d in enumerate(currencyList):
            base_curr = list(d.keys())[0]
            target_curr = d[base_curr]
            
            thread_list.append(threading.Thread(target=fetch_currency_in_thread, args=(base_curr, target_curr, idx)))
            thread_list[-1].start()

        for t in thread_list:
            t.join()

        clean_result = []
        for r in result:
            if r:
                clean_result.append(r)

        return clean_result


if __name__ == "__main__":
    # Tests
    print(CurrencyManager().fetch_multiple_currencies([
        {"USD": "TRY"},
        {"EUR": "TRY"},
    ]))
