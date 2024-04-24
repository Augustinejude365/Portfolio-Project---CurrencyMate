#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


def get_exchange_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["rates"].get(to_currency)
    else:
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["GET"])
def convert():
    amount = float(request.args.get("amount"))
    from_currency = request.args.get("from_currency").upper()
    to_currency = request.args.get("to_currency").upper()
    result = convert_currency(amount, from_currency, to_currency)
    if isinstance(result, float):
        return jsonify({"result": result})
    else:
        return jsonify({"error": result})


def convert_currency(amount, from_currency, to_currency):
    rate = get_exchange_rate(from_currency, to_currency)
    if rate is not None:
        converted_amount = amount * rate
        return converted_amount
    else:
        return "Unable to perform conversion. Please check the currencies\
                 provided."


if __name__ == "__main__":
    app.run(debug=True)
