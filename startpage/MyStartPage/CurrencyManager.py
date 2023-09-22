import requests

class CurrencyManager:
    def __init__(self):
        self.api_url: str = "https://api.exchangerate.host/latest?base={}"
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
        full_url = self.api_url.format(base_currency)
        try:
            req = requests.get(full_url)
        except:
            return ""

        if not str(req.status_code).startswith('2'):
            return ""

        data = req.json()
        if not data["success"]:
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
        result: list[str] = []

        for d in currencyList:
            base_curr = list(d.keys())[0]
            target_curr = d[base_curr]

            current_str = self.fetch_currency(base_curr, target_curr)
            if current_str:
                result.append(current_str)

        return result


if __name__ == "__main__":
    # Tests
    print(CurrencyManager().fetch_multiple_currencies([
        {"USD": "TRY"},
        {"EUR": "TRY"},
    ]))