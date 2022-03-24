import argparse
import sys
import urllib.request
from datetime import date


def get_fx_rates(url):
    """Return FX rates from URL as dict.

    Supports only the format provided by the Czech National Bank.

    Returns: dict(currency_code: str, fx_rate: str)
    """
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")  # FIXME: don't guess the data encoding

    fx_rates = dict()
    for line in data.split("\n")[2:]:  # skip ID and header lines
        fields = line.split("|")
        if line == "":
            # If data ends with newline, the last line is empty.
            continue
        fx_rates[fields[-2]] = fields[-1]

    return fx_rates


def main():
    """Script entry point"""

    parser = argparse.ArgumentParser()
    parser.add_argument("currency", help="currency ISO code, e.g. USD")
    parser.add_argument(
        "date",
        nargs="?",
        default=date.today().isoformat(),
        help="optional date in ISO format, e.g. 2022-01-01; default: today",
    )
    args = parser.parse_args()

    valid_currencies = [
        "AUD",
        "BGN",
        "BRL",
        "CAD",
        "CHF",
        "CNY",
        "DKK",
        "EUR",
        "GBP",
        "HKD",
        "HRK",
        "HUF",
        "IDR",
        "ILS",
        "INR",
        "ISK",
        "JPY",
        "KRW",
        "MXN",
        "MYR",
        "NOK",
        "NZD",
        "PHP",
        "PLN",
        "RON",
        "RUB",
        "SEK",
        "SGD",
        "THB",
        "TRY",
        "USD",
        "XDR",
        "ZAR",
    ]
    my_date = date.fromisoformat(args.date)
    file_url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
    url_query = f"?date={my_date.strftime('%d.%m.%Y')}"

    if args.currency not in valid_currencies:
        print(
            f"error: invalid currency code; valid codes: {' '.join(valid_currencies)}"
        )
        sys.exit(1)

    fx_rates = get_fx_rates(file_url + url_query)
    print(fx_rates[args.currency])


if __name__ == "__main__":
    main()
