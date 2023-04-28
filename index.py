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

fut = module.Fut()
fut.complete_login_by_gmx(fut_username, fut_password, gmx_username, gmx_password)

print('Your coins: ' + fut.coin_count())
print('Players on Transferlist: ' + fut.transfer_list_total_count())

fut.delete_old_transfers('transfers.csv')
sleep(1)
fut.nav_tab('home').click()
sleep(1)
fut.relist_transfers()
sleep(1)
fut.nav_tab('home').click()
sleep(1)

#for i in range(0,5):
'''while num == 0:
    fut.resell_player_by_name(player_name, player_rating, buy_price, sell_price, amount, csv_doc)
    sleep(1)
    fut.nav_tab('home').click()
    sleep(1)
    print('Players on Transferlist: ' + fut.transfer_list_total_count())'''

starttime = int(datetime.datetime.now().strftime('%H%M%S'))

while num == 0:
    sleep(1)
    if int(fut.transfer_list_total_count()) == 100:
        print('TRANSFERLIST IS FULL!!')
        fut.delete_old_transfers('transfers.csv')
        sleep(1)
        fut.nav_tab('home').click()
        sleep(1)
        fut.relist_transfers()
        sleep(1)
        fut.nav_tab('home').click()
        sleep(1)
    else:
        if int(fut.transfer_list_total_count()) > 80:
            amount_re = 100 - int(fut.transfer_list_total_count())
        else: amount_re = amount
        print('transferlist is NOT full!')
        print('players to buy per search are:', amount_re)
        fut.resell_player_by_name(player_name, player_rating, buy_price, sell_price, amount_re, csv_doc)
        sleep(1)
        fut.nav_tab('home').click()
        sleep(1)
        print('Players on Transferlist: ' + fut.transfer_list_total_count())

    controltime = int(datetime.datetime.now().strftime('%H%M%S'))
    print(starttime)
    print(controltime)
    if controltime > (starttime + 10000) or controltime < (starttime - 225000):
        print('OVER 1 HOUR PASSED')
        fut.delete_old_transfers('transfers.csv')
        sleep(1)
        fut.nav_tab('home').click()
        sleep(1)
        fut.relist_transfers()
        sleep(1)
        fut.nav_tab('home').click()
        sleep(1)
        starttime = int(datetime.datetime.now().strftime('%H%M%S'))


print('finished :) Closing browser in 15s')
sleep(15)
fut.browser.close()
