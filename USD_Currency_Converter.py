from requests import get
from pprint import PrettyPrinter #Used only in the beginning, to explore the API

BASE_URL = "https://api.currencyfreaks.com/"
API_KEY = "1bc6c917af6c4947968d9bf58550250f"

#ENDPOINTS
supported_currencies = "v2.0/supported-currencies"
supported_currencies_symbols = "v2.0/currency-symbols"
historical_data_limits = "v2.0/historical-data-limits"
latest_exchange_rates = f"v2.0/rates/latest?apikey={API_KEY}"

printer = PrettyPrinter()

def get_currencies(): #get all the supported currencies
    url = BASE_URL + supported_currencies
    data = get(url).json()['supportedCurrenciesMap'] # data will become a dictionary

    data = list(data.items()) #converting dictionary to a list of tuples so it can be sorted
    data.sort() # sorting the list alphabetically

    return data # Return the sorted list of currencies

def print_currencies(currencies):
    for code, currency in currencies:   # because currencies is a list of tuples: (name ,{info1,info2})
        name = currency['currencyName'] # get full currency name
        _id = currency['currencyCode']  #get currency code
        print(f"{_id} - {name}")

def exchange_rate(currency2):
    desired_exchange_rates = f"v2.0/rates/latest?apikey={API_KEY}&symbols={currency2}"
    url = BASE_URL + desired_exchange_rates
    response = get(url).json()  # Send request and get JSON response

    # Check if response contains 'rates' and if the given currency exists in the response
    if 'rates' not in response or currency2 not in response['rates']:
        print(f"Error: Invalid currency '{currency2}'.")
        return None # Return None to indicate failure

    data_exchange_rate = list(response['rates'].items())[0]  # converting the dictionary into list so we can split it below and getting the 1st item
    currency2_code, currency2_rate = data_exchange_rate # unpack tuple into variables
    return currency2_rate   # Return exchange rate as a string

def convert(amount, currency2):
    rate = exchange_rate(currency2) # Get the exchange rate

    if rate is None:    # Check if currency is invalid
        print(f"Error: No exchange rate found for {currency2}.")
        return

    else:
        rate = float(exchange_rate(currency2))   # Convert exchange rate to float
        try:
            amount = float(amount)  # Convert user input to a float
        except ValueError:  #do not use broad exception. If input is not a number, show an error
            print("Invalid amount.")
            return

    converted_amount = rate * amount    # Perform conversion
    print(f"USD {amount} = {currency2} {converted_amount}") # Print result
    return converted_amount # Return converted amount

def main():
    currencies = get_currencies()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True: # Infinite loop for user interaction
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            amount = input(f"Enter an amount in USD: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(amount, currency2)
        elif command == "rate":
            currency2 = input("Enter a currency to convert to: ").upper()
            rate = exchange_rate(currency2)
            if rate:
                print(f"1 USD is equal to {currency2} {rate}")
        else:
            print("Unrecognized command!")


main()  # Start the program