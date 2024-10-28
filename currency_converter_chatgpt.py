import requests
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

def list_currencies():
    """Fetch and display all available currency symbols."""
    url = "https://api.apilayer.com/fixer/symbols"
    headers = {"apikey": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Error: Unable to fetch currency symbols.")
        return
    
    data = response.json()
    symbols = data.get("symbols", {})
    print("\nAvailable currencies:")
    for code, name in symbols.items():
        print(f"{code}: {name}")

def get_currency_conversion(amount, initial_currency, target_currency):
    url = (f"https://api.apilayer.com/fixer/convert?to={target_currency}"
           f"&from={initial_currency}&amount={amount}")
    headers = {"apikey": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None, f"Error: Unable to fetch data. Status code: {response.status_code}"
    
    data = response.json()
    if not data.get("success"):
        return None, "Error: Conversion failed. Please check the currency codes."
    
    return data.get("result"), None

def input_currency(prompt):
    currency = input(prompt).strip().upper()
    if len(currency) != 3 or not currency.isalpha():
        print("Error: Currency code should be a three-letter alphabetic code (e.g., USD, EUR).")
        return input_currency(prompt)
    return currency

def input_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                print("The amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("The amount must be a numeric value.")

def main():
    print("Welcome to the Currency Converter App")
    while True:
        print("\nOptions:")
        print("1. Convert currency")
        print("2. List available currencies")
        print("3. Exit")
        choice = input("Choose an option (1, 2, or 3): ").strip()
        
        if choice == "1":
            initial_currency = input_currency("Enter the initial currency (e.g., USD): ")
            target_currency = input_currency("Enter the target currency (e.g., EUR): ")
            amount = input_amount()
            
            result, error = get_currency_conversion(amount, initial_currency, target_currency)
            
            if error:
                print(error)
            else:
                print(f"{amount} {initial_currency} is equal to {result:.2f} {target_currency}")
        
        elif choice == "2":
            list_currencies()
        
        elif choice == "3":
            print("Thank you for using the Currency Converter App!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
