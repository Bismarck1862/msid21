import time

import requests

BIDS = 'bids'
ASKS = 'asks'
ADDRESS_BITBAY = 'https://bitbay.net/API/Public/'
ADDRESS_ORDERBOOK = '/orderbook.json'


def get_data(name):
    address = ADDRESS_BITBAY + name + ADDRESS_ORDERBOOK
    return requests.get(address)


def print_difference(name, bids_avg, asks_avg, diff):
    print(name, "Avg sells:", asks_avg, ", Avg purchases:", bids_avg)
    print(name, "Difference:", diff, "%")


def print_bids_asks_difference(name, elements_to_average):
    bids_sum = 0.0
    asks_sum = 0.0
    response = get_data(name)
    if response:
        response_json = response.json()

        min_length = min(len(response_json[BIDS]), len(response_json[ASKS]))
        if elements_to_average > min_length:
            elements_to_average = min_length

        for i in range(0, elements_to_average):
            bids_sum += response_json[BIDS][i][0]
            asks_sum += response_json[ASKS][i][0]

        bids_avg = bids_sum / elements_to_average
        asks_avg = asks_sum / elements_to_average
        diff = (1 - (asks_avg - bids_avg) / bids_avg) * 100
        print_difference(name, bids_avg,  asks_avg, diff)
    else:
        print(name, ' data not found')


def print_updating_data(name, max_bound, delay):
    while True:
        print_bids_asks_difference(name, max_bound)
        time.sleep(delay)


def main():
    print_bids_asks_difference('BTCUSD', 80)
    print_bids_asks_difference('DASHUSD', 50)
    print_bids_asks_difference('LTCUSD', 50)
    print_updating_data('BTCUSD', 50, 5)


if __name__ == '__main__':
    main()

