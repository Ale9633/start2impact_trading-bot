# Start2impact (Super Guida Python): Trading bot
# Coinmarketcap APIs

import requests
import time
from datetime import datetime
from password import COINMARKETCAP_API_KEY
from pprint import pprint


class Bot:
    """ Generic trading bot that get info through Coinmarketcap's APIs """

    def __init__(self):
        # Get first 100 cryptocurrencies sorted by market capitalization
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.parameters = {
          'start': '1',
          'limit': '100',
          'convert': 'USD'
        }
        self.headers = {
          'Accepts': 'application/json',
          'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
        }
        self.orders = []

    def fetch_currencies_data(self):
        # Get and return data using the APIs configuration set in the constructor
        response = requests.get(url=self.url, headers=self.headers, params=self.parameters).json()
        return response['data']

    def can_buy(self):
        # Check if there are open orders
        for order in self.orders:
            if order['status'] == 'open':
                return False
        return True

    def open_order(self, currencies, target, min_currencies):
        # Place a buy order
        n_currencies = 0  # Number of currencies whose price has increased more than 'target_buy' in the last hour
        best_currency = None  # The currency with the highest price revaluation

        for currency in currencies:
            if not best_currency or currency['quote']['USD']['percent_change_1h'] > best_currency['quote']['USD']['percent_change_1h']:
                best_currency = currency
            if currency['quote']['USD']['percent_change_1h'] > target:
                n_currencies += 1
        if n_currencies >= min_currencies:
            new_order = {
                'time': str(datetime.now()),
                'symbol': best_currency['symbol'],
                'enter price': round(best_currency['quote']['USD']['price'], 2),
                'exit price': None,
                'status': 'open'
            }
            self.orders.append(new_order)
            return True
        return False

    def close_order(self, currencies, target):
        # Place a sell order
        try:
            # Try to get the last order if there are
            for currency in currencies:
                if currency['symbol'] == self.orders[-1]['symbol'] and self.orders[-1]['status'] == 'open':
                    if currency['quote']['USD']['percent_change_1h'] < target:
                        self.orders[-1]['exit price'] = round(currency['quote']['USD']['price'], 2)
                        self.orders[-1]['status'] = 'close'
                        return True
        except IndexError:
            # 'self.orders' is empty
            raise IndexError('There are no order to close')
        return False

    def get_statistics(self, initial_amount):
        # Calculates gains and losses based on initial capital and simulated orders
        profit = initial_amount

        for order in self.orders:
            if order['status'] == 'close':
                profit = profit * (order['exit price'] / order['enter price'])
        final_amount = profit
        statistics = {
            'orders': len(self.orders),
            'initial amount': round(initial_amount, 2),
            'final amount': round(final_amount, 2),
            'gain': round((((final_amount - initial_amount) / initial_amount) * 100), 1)
        }
        return statistics


def main():
    # Setup variables
    impact_bot = Bot()
    minutes = 10
    seconds = 60
    target_buy = 3  # Percentage above which to buy the currency
    target_sell = -1  # Percentage under which to sell the currency
    min_currencies = 4  # Minimum of currencies whose price has increased more than 'target_buy' in the last hour
    initial_amount = 10000

    # Check market variations and make orders
    while True:
        currencies = impact_bot.fetch_currencies_data()

        if impact_bot.can_buy():
            # Buy
            impact_bot.open_order(currencies=currencies, target=target_buy, min_currencies=min_currencies)
        else:
            # Sell
            try:
                impact_bot.close_order(currencies=currencies, target=target_sell)
            except IndexError:
                raise IndexError('There are no order to close!')

        # Trading statistics
        stats = impact_bot.get_statistics(initial_amount=initial_amount)
        print('------------------------------')
        print('ORDERS')
        for order in impact_bot.orders:
            print(order)
        print('\nSTATISTICS')
        print('N. orders: ' + str(stats['orders']))
        print('Initial amount: ' + str(stats['initial amount']) + "$")
        print('final amount: ' + str(stats['final amount']) + "$")
        print('Gain: ' + str(stats['gain']) + "%")
        print('------------------------------\n')

        time.sleep(minutes*seconds)


if __name__ == '__main__':
    main()