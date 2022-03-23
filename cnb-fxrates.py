import argparse
import urllib.request
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("currency", help="currency ISO code, e.g. USD")
parser.add_argument(
    "date",
    nargs="?",
    default=date.today().isoformat(),
    help="optional date in ISO format, e.g. 2022-01-01; default: today",
)
args = parser.parse_args()

my_date = date.fromisoformat(args.date)
file_url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
url_query = f"?date={my_date.strftime('%d.%m.%Y')}"

with urllib.request.urlopen(file_url + url_query) as response:
    data = response.read().decode("utf-8")  # FIXME: don't guess the data encoding

for line in data.split("\n")[2:]:  # skip ID and header lines
    if args.currency in line:
        fx_rate = line.split("|")[-1]
        break

# print(data.split("\n")[:2])
print(fx_rate)
