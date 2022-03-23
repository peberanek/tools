import urllib.request

file_url = "https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/daily.txt"
url_query = "?date=01.01.2022"  # FIXME: no hardcoded vals!
currency_code = "EUR"  # FIXME: no hardcoded vals!

with urllib.request.urlopen(file_url + url_query) as response:
   data = response.read().decode("utf-8")  # FIXME: don't guess the data encoding

for line in data.split("\n")[2:]:  # skip ID and header lines
    if currency_code in line:
        fx_rate = line.split("|")[-1]
        break

print(fx_rate)
