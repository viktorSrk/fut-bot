from time import sleep
import datetime

import module

player_name = 'coutinho'
player_rating = 82
buy_price = 1000
sell_price = 1600
amount = 20     #max 20
csv_doc = 'transfers.csv'

fut_username = 'vik_hh@gmx.de'
fut_password = '2!z2rN-wP'
gmx_username = 'vik_hh@gmx.de'
gmx_password = 'peter12+14'

num = 0

class Bot():
    def __init__(self):
        self.fut = module.Fut()
        self.fut.complete_login_by_gmx(fut_username, fut_password, gmx_username, gmx_password)

    def parent(self):
        return self.fut

    def run(self):
        print('Your coins: ' + self.fut.coin_count())
        print('Players on Transferlist: ' + self.fut.transfer_list_total_count())

        self.fut.delete_old_transfers('transfers.csv')
        sleep(1)
        self.fut.nav_tab('home').click()
        sleep(1)
        self.fut.relist_transfers()
        sleep(1)
        self.fut.nav_tab('home').click()
        sleep(1)

        starttime = int(datetime.datetime.now().strftime('%H%M%S'))

        while 0 == 0:
            sleep(1)
            if int(self.fut.transfer_list_total_count()) == 100:
                print('TRANSFERLIST IS FULL!!')
                self.fut.delete_old_transfers('transfers.csv')
                sleep(1)
                self.fut.nav_tab('home').click()
                sleep(1)
                self.fut.relist_transfers()
                sleep(1)
                self.fut.nav_tab('home').click()
                sleep(1)
            else:
                if int(self.fut.transfer_list_total_count()) > 80:
                    amount_re = 100 - int(self.fut.transfer_list_total_count())
                else: amount_re = amount
                print('transferlist is NOT full!')
                print('players to buy per search are:', amount_re)
                self.fut.resell_player_by_name(player_name, player_rating, buy_price, sell_price, amount_re, csv_doc)
                sleep(1)
                self.fut.nav_tab('home').click()
                sleep(1)
                print('Players on Transferlist: ' + self.fut.transfer_list_total_count())

            controltime = int(datetime.datetime.now().strftime('%H%M%S'))
            print(starttime)
            print(controltime)
            if controltime > (starttime + 10000) or controltime < (starttime - 225000):
                print('OVER 1 HOUR PASSED')
                self.fut.delete_old_transfers('transfers.csv')
                sleep(1)
                self.fut.nav_tab('home').click()
                sleep(1)
                self.fut.relist_transfers()
                sleep(1)
                self.fut.nav_tab('home').click()
                sleep(1)
                starttime = int(datetime.datetime.now().strftime('%H%M%S'))

bot = Bot()
while 0 == 0:
    try:
        bot.run()
    except:
        bot.parent().browser.close()
        bot = Bot()

print('finished :) Closing browser in 15s')
sleep(15)
bot.parent().browser.close()
