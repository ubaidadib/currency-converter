import requests
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Load the API key from the .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Function to fetch and convert currency
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

# Function to fetch and display available currencies
def list_currencies():
    url = "https://api.apilayer.com/fixer/symbols"
    headers = {"apikey": API_KEY}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        messagebox.showerror("Error", "Unable to fetch currency symbols.")
        return
    
    data = response.json()
    symbols = data.get("symbols", {})
    
    currency_list.delete(1.0, tk.END)
    for code, name in symbols.items():
        currency_list.insert(tk.END, f"{code}: {name}\n")

# Function to perform currency conversion and display result
def convert_currency():
    initial_currency = initial_currency_entry.get().strip().upper()
    target_currency = target_currency_entry.get().strip().upper()
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a positive numeric value.")
        return
    
    result, error = get_currency_conversion(amount, initial_currency, target_currency)
    if error:
        messagebox.showerror("Conversion Error", error)
    else:
        result_label.config(text=f"{amount} {initial_currency} = {result:.2f} {target_currency}")

# Setting up the GUI window
window = tk.Tk()
window.title("Currency Converter")
window.geometry("400x500")

# Initial currency
tk.Label(window, text="Initial Currency (e.g., USD):").pack()
initial_currency_entry = tk.Entry(window)
initial_currency_entry.pack()

# Target currency
tk.Label(window, text="Target Currency (e.g., EUR):").pack()
target_currency_entry = tk.Entry(window)
target_currency_entry.pack()

# Amount
tk.Label(window, text="Amount:").pack()
amount_entry = tk.Entry(window)
amount_entry.pack()

# Convert button
convert_button = tk.Button(window, text="Convert", command=convert_currency)
convert_button.pack()

# Result label
result_label = tk.Label(window, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# List currencies button
list_button = tk.Button(window, text="List Available Currencies", command=list_currencies)
list_button.pack()

# Scrolled text widget for displaying currency list
currency_list = scrolledtext.ScrolledText(window, width=40, height=10, wrap=tk.WORD)
currency_list.pack(pady=10)

# Run the application
window.mainloop()
