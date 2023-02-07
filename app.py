from bestchange_api import BestChange
import json
import time
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)

class Downloader:
    def __init__(self):

        self.api = BestChange(cache=True)
        self.rates = self.api.rates().get()
        self.file_whitetickers = self.read_whitetickers()
        self.file_exchengers = self.read_exchangers()


    def _update_rates(self):
        while True:
            self.api = BestChange(cache=True)
            try:
                self.rates = self.api.rates().get()
                self.exchangers = self.api.exchangers().get()
                self.clear_rates = self.filter_whitetickers_black_exchengers_add_status_ex_name()
                # with open('../var/www/html/clear_rates.json', 'w') as file:
                #     json.dump(self.clear_rates, file)
            except:
                print('ОШИБКА получения информации с Bestchange.ru')
            time.sleep(1)


    def read_whitetickers(self):
        with open('whitetickers.txt', 'r') as file:
            text = file.readlines()
            data = []
            for line in text:
                line = line.split(';')
                monet = {'id': line[0].split('=')[1],
                         'name': line[2].split('=')[1],
                         'ticker': line[3].split('=')[1],
                         'wallet': line[4].split('=')[1],
                         'memo': line[5].split('=')[1],
                         'network_fee': '0'}
                data.append(monet)

            return data


    def read_exchangers(self):
        with open('exchangers.txt', 'r') as file:
            text2 = file.readlines()
            data2 = []
            for line2 in text2:
                line2 = line2.split(';')
                data2.append(
                    {'status': line2[0].split('=')[1],
                     'id': line2[1].split('=')[1],
                     'name': line2[2].split('=')[1][:-1]}
                )
            return data2


    def filter_whitetickers_black_exchengers_add_status_ex_name(self):
        self.id_monets = [monet['id'] for monet in self.file_whitetickers]

        self.id_black_exchengers = [exchenger['id'] for exchenger in self.file_exchengers if
                                    exchenger['status'] == 'red']
        status_ex = {ex['id']: ex['status'] for ex in self.file_exchengers}
        half_filt_rates = [rate for rate in self.rates if
                           str(rate['give_id']) in self.id_monets and str(rate['get_id']) in self.id_monets]
        clear_rates = []
        for rate in half_filt_rates:
            if str(rate['exchange_id']) in self.id_black_exchengers:
                continue
            else:
                rate['status'] = status_ex.get(str(rate['exchange_id']), 'gray')
                clear_rates.append(rate)
        ex_name = {ex['id']: ex['name'] for ex_id, ex in self.exchangers.items()}
        for rate in clear_rates:
            rate['exchange_name'] = ex_name[rate['exchange_id']]
        return clear_rates

@app.route('/get')
def get_page():
    return jsonify(downloader.clear_rates)


if __name__ == "__main__":
    downloader = Downloader()
    Thread(target=downloader._update_rates()).start()