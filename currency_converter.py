# Currency Converter App
# Create a program that allows users to convert between different currencies.
# The program should allow the user to enter the amount and the initial and target currencies.
# The program should convert the amount from the initial currency to the target currency and display the result.
# The program should use the fixer.io API to convert the amount from the initial currency to the target currency.
# The fixer.io API key should be stored in a .env file. 
# API KEY : f4r03x0pjhbvKoJpv15TaNhzibN2c0d8

import requests

initial_currency = input("Enter an intial currency: ")
target_currency = input("Enter an target currency: ")

while True:
    try:
        amount = float(input("Enter the amount: "))
    except:
        print("The amout must be a numberic value!")
        continue

    if amount == 0:
        print("The amount must be greater than 0")
        continue
    else:
        break

url = ("https://api.apilayer.com/fixer/convert?to="
        + target_currency + "&from=" + initial_currency
        + "&amount=" + str(amount))

payload = {}
headers= {
  "apikey": "f4r03x0pjhbvKoJpv15TaNhzibN2c0d8"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text  # result = response.json()

if status_code == 200:  
    print(result)
else:
    print("Error code:", status_code)

