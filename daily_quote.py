import requests
import random
import json
import os
import tkinter as tk
from tkinter import messagebox

# Local file to store used quotes
used_quotes_file = "used_quotes.json"

# Initialize storage file if it doesn't exist
if not os.path.exists(used_quotes_file):
    with open(used_quotes_file, "w") as f:
        json.dump([], f)

# Load used quotes
with open(used_quotes_file, "r") as f:
    used_quotes = json.load(f)

# Quote source 1: ZenQuotes (philosophical, inspirational)
def fetch_zenquote():
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=10)
        if res.status_code == 200:
            data = res.json()[0]
            return f'"{data["q"]}" - {data["a"]}'
    except:
        return None

# Quote source 2: Quotable (wisdom, business, motivational)
def fetch_quotable():
    try:
        tags = ["inspirational", "wisdom", "business"]
        res = requests.get(f"https://api.quotable.io/random?tags={'|'.join(tags)}", timeout=10)
        if res.status_code == 200:
            data = res.json()
            return f'"{data["content"]}" - {data["author"]}'
    except:
        return None

# Quote source 3: API Ninjas (business/motivational) — requires your API key
def fetch_api_ninjas():
    try:
        api_key = "YOUR_API_KEY"  # Replace with your API key
        headers = {"X-Api-Key": api_key}
        res = requests.get("https://api.api-ninjas.com/v1/quotes?category=business", headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()[0]
            return f'"{data["quote"]}" - {data["author"]}'
    except:
        return None

# Shuffle APIs and get first unique quote
def get_unique_quote():
    sources = [fetch_zenquote, fetch_quotable, fetch_api_ninjas]
    random.shuffle(sources)
    for func in sources:
        quote = func()
        if quote and quote not in used_quotes:
            used_quotes.append(quote)
            # Keep only last 100 to prevent overgrowth
            with open(used_quotes_file, "w") as f:
                json.dump(used_quotes[-100:], f)
            return quote
    return "No new quote found today."

# GUI window to display quote
def show_quote_window(quote):
    root = tk.Tk()
    root.title("💡 Daily Quote")
    root.geometry("500x250")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    label = tk.Label(frame, text=quote, wraplength=460, justify="left", font=("Segoe UI", 11))
    label.pack(pady=10)

    close_button = tk.Button(frame, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    root.mainloop()

# Main logic
quote = get_unique_quote()
show_quote_window(quote)
