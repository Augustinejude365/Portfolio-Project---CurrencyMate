#!/usr/bin/env python3

""" DON'T DELETE!!!!
shebang for my local windows venv
#!/c/Users/TOSHIBA/Documents/Portfolio-Project---CurrencyMate/my-venv/Scripts/python
"""

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    """
    Renders the index.html template, which is our main UI
    for the currency converter.

    Returns:
        The rendered index.html template.
    """
    return render_template("index.html")


@app.route("/convert", methods=["GET"])
def convert():
    """
    Performs currency conversion based on user input via GET request.

    Returns:
        A JSON response with either the converted amount or an error message.
    """
    amount = float(request.args.get("amount"))
    from_currency = request.args.get("from_currency").upper()
    to_currency = request.args.get("to_currency").upper()
    result = convert_currency(amount, from_currency, to_currency)
    if isinstance(result, float):
        return jsonify({"result": result})
    else:
        return jsonify({"error": result})


def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount from one currency to another
    using the fetched exchange rate.

    Args:
        amount (float): The amount to convert
        from_currency (str): The currency to convert from
        to_currency (str): The currency to convert to

    Returns:
        The converted amount as a float, or an error message if unsuccessful.
    """
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is not None:
        converted_amount = amount * rate
        return converted_amount
    else:
        return "Unable to perform conversion. Please check the currencies\
                 provided."


def get_exchange_rate(from_currency, to_currency):
    """
    Fetches the exchange rate between two currencies from exchangerate-api.com

    Args:
        from_currency (str): The currency to convert from
        to_currency (str): The currency to convert to

    Returns:
        The exchange rate as a float, or None if an error occurs.
    """
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"].get(to_currency)
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True, port=8000)
