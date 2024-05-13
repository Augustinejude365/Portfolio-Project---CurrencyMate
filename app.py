#!/c/Users/TOSHIBA/Documents/Portfolio-Project---CurrencyMate/my-venv/Scripts/python

""" DON'T DELETE!!!!
shebang for my local windows venv
#!/usr/bin/env python3
#!/c/Users/TOSHIBA/Documents/Portfolio-Project---CurrencyMate/my-venv/Scripts/python
"""


import os
import requests
import smtplib
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from whitenoise import WhiteNoise
from wtforms import Form, StringField, TextAreaField, validators


sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

if not (sender_email and sender_password and receiver_email):
    raise ValueError("Email credentials are not set in environment variables")


# Form validation
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.Length(min=6, max=50), validators.DataRequired()])
    subject = StringField('Subject', [validators.Length(min=1, max=100), validators.DataRequired()])
    message = TextAreaField('Message', [validators.Length(min=10), validators.DataRequired()])

app = Flask(__name__, static_url_path='/currencymate/static')
app.secret_key = b'\xf2PUc\x92M\x95U\xc9*\x9b\xf8\xa8\x8d\xd7-\xea\xd6\xd4\x19 \xe2\xe9\x98'
app.url_map.strict_slashes = False
app.wsgi_app = WhiteNoise(app.wsgi_app)
app.static_folder = 'static'


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


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate():
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            message = form.message.data

            success, error_message = send_email(subject, message, name, email)
            if success:
                flash(('Your message has been sent successfully.', 'success'))
            else:
                flash((f'Failed to send email: {error_message}', 'error'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash((f"Error in {field}: {error}", 'error'))
    return render_template('index.html', scroll_to_contact=True)


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


def send_email(subject, message, user_name, user_email):
    """
    Sends an email using SMTP protocol with error handling.

    Args:
        subject (str): The subject of the email.
        message (str): The body content of the email.
        user_name (str): The user's name captured from the form.
        user_email (str): The user's email address captured from the form.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """

    smtp_server = 'us2.smtp.mailhostbox.com'
    port = 587

    email_content = f"Subject: {subject}\n\nFrom: {user_name} <{user_email}>\n\nMessage: {message}"

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_content.encode('utf-8'))
            print("delivered")
        return True, None
    except Exception as e:
        print("not delivered", str(e))
        return False, str(e)


# app entry point
if __name__ == "__main__":
    app.run(debug=True, port=8000)
