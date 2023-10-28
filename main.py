import json
import requests

EXIT_SUCCESS = 0
CONNECTION_ERROR = 1
WRONG_RATE_CODE = 2

request = requests.request("GET", "https://api.nbp.pl/api/exchangerates/tables/A/?format=json")

def display_rate_list(rates):
    print("This is list of codes of all available rates:")
    for rate in rates:
        currency = rate['currency']
        code = rate['code']
        print(f"* {code} ({currency})")


def ask_user_for_code(rates):
    user_rate_code = input("Please provide valid exchange rate code: ")
    found = False
    for rate in rates:
        if rate['code'] == user_rate_code:
            found = True
    if not found:
        print("You provided wrong exchange rate code!")
        exit(WRONG_RATE_CODE)
    return user_rate_code


def find_rate(rates, user_rate_code):
    for rate in rates:
        if rate['code'] == user_rate_code:
            return rate
    return None


if not request.ok:
    print("Something went wrong!")
    exit(CONNECTION_ERROR)

obj = json.loads(request.text)
budget = float(input("Please provide you budget in PLN to change: "))
rates = obj[0]['rates']
display_rate_list(rates)
user_rate_code = ask_user_for_code(rates)
rate = find_rate(rates, user_rate_code)
exchange_rate = rate['mid']
budget_foreign = budget / exchange_rate
print(f"You can exchange {budget} PLN to {budget_foreign} {rate['code']}")
