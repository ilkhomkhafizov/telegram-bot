# TODO
#
# 1. Get cryptocurrency prices from the CoinMarketCap API
# 2. Create a Telegram bot with BotFather…
# 3. Create a Flask application and handle requests from Telegram (receiving and sending messages). Test it with a tunnel.
# 4. Combine the CoinMarketCap parser and the Telegram bot
# 5. Deploy to the PythonAnyWhere and install Flask-SSLify to solve SSL certificate issue.

from tokens import cmc_token

import json
import re

import requests

from flask import Flask
from flask import request
from flask import Response

from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)


def write_json(data, filename='response.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_cmc_data(crypto):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': crypto, 'convert': 'USD'}
    headers = {'X-CMC_PRO_API_KEY': cmc_token}

    r = requests.get(url, headers=headers, params=params).json()

    price = r['data'][crypto]['quote']['USD']['price']

    return price



def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']   # /btc  or /maid

    pattern = r'/[a-zA-Z]{2,4}'

    ticker = re.findall(pattern, txt)  # [...]

    if ticker:
        symbol = ticker[0][1:].upper()  # /btc > btc   .strip('/')
    else:
        symbol = ''

    return chat_id, symbol


def send_message(chat_id, text='bla-bla-bla'):
    url = f'https://api.telegram.org/bot{cmc_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)

        if not symbol:
            send_message(chat_id, 'Wrong data')
            return Response('Ok', status=200)

        price = get_cmc_data(symbol)
        send_message(chat_id, price)
        write_json(msg, 'telegram_request.json')

        return Response('Ok', status=200)
    else:
        return '<h1>CoinMarketCap bot</h1>'


def main():

    # TODO BOT

    # 1. Locally create a basic Flask application
    # 2. Set up a tunnel
    # 3. Set a webhook
    # 4. Receive and parse a user’s messages
    # 5. Send message to a user.


    print(get_cmc_data('BTC'))

    # https://api.telegram.org/cms_token/getMe
    # https://api.telegram.org/cms_token/sendMessage?chat_id=180876400&text=Hello user

    # https://api.telegram.org/cms_token/setWebhook?url=https://olegmolchanov.pythonanywhere.com/


if __name__ == '__main__':
    # main()
    app.run(debug=True)
