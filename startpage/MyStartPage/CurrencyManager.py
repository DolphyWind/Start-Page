import requests

class CurrencyManager:
    def __init__(self):
        self.api_url: str = "https://api.exchangerate.host/latest?base={}"

    def fetch_currency(self, base_currency: str, target_currency: str) -> str:
        full_url = self.api_url.format(base_currency)
        try:
            req = requests.get(full_url)
        except:
            return ""

        data = req.json()
        if not data["success"]:
            return ""

        converted_currency = data['rates'][target_currency]
        return f"1 {target_currency} = {round(converted_currency, 2)} {base_currency}"

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