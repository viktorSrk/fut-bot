from time import sleep
from types import NoneType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import csv
from datetime import date

class Webpage:
    def __init__(self, website_url):
        self.browser = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
        self.browser.implicitly_wait(5)
        self.browser.get(website_url)
        print(str(self) + ': opening ' + website_url + ' ...')

class Gmx(Webpage):
    def __init__(self):
        website_url = 'https://www.gmx.net'
        super().__init__(website_url)
        self.browser.get(website_url)

    def login(self, username, password):
        self.browser.find_element(By.NAME,  "username").send_keys(username)
        print(str(self) + ': entering email...')
        self.browser.find_element(By.NAME,  "password").send_keys(password)
        print(str(self) + ': entering password...')
        self.browser.find_element(By.XPATH, "//button[text()='Login']").click()
        print(str(self) + ': logging in...')

        sleep(5)
    
    def open_inbox(self, num):
        inbox_url = self.browser.find_element(By.ID, 'thirdPartyFrame_mail').get_attribute('src')
        self.browser.get(inbox_url)
        print(str(self) + ': opening inbox tab...')

        sleep(2)

        self.browser.find_element(By.ID, 'idb').click()
        print(str(self) + ': refreshing inbox...')

        sleep(2)

        try:
            ActionChains(self.browser).move_to_element(self.browser.find_element(By.XPATH, '//tr[' + str(num) + ']')).perform()
            self.browser.find_element(By.XPATH, "//li[@data-oao-hover='open']/a").click()
            print(str(self) + ': opening mail number ' + str(num) + ' ...')
        except:
            ActionChains(self.browser).move_to_element(self.browser.find_element(By.XPATH, '//tr[' + str(num+1) + ']')).perform()
            self.browser.find_element(By.XPATH, "//li[@data-oao-hover='open']/a").click()

    def get_ea_security_code(self):
        self.browser.switch_to.frame(self.browser.find_element(By.ID, 'mail-detail'))
        texts = self.browser.find_elements(By.XPATH, "//span[@style='color: rgb(0,0,0);']/b")
        code = texts[1].text
        self.browser.switch_to.default_content()
        print(str(self) + ': retrieved EA security code...')
        return code

class Fut(Webpage):
    def __init__(self):
        self.website_url = 'https://www.ea.com/fifa/ultimate-team/web-app/'
        super().__init__(self.website_url)
    
    def login(self, username, password):
        sleep(3)
        ActionChains(self.browser).move_to_element(self.browser.find_element(By.XPATH, "//button[text()='Login']")).perform()
        sleep(3)
        ActionChains(self.browser).click(self.browser.find_element(By.XPATH, "//button[text()='Login']")).perform()
        print(str(self) + ': opened login screen...')
            
        sleep(5)

        self.browser.find_element(By.ID, 'email').send_keys(username)
        print(str(self) + ': entering username...')
        self.browser.find_element(By.ID, 'password').send_keys(password)
        print(str(self) + ': entering password...')
        self.browser.find_element(By.ID, 'logInBtn').click()
        print(str(self) + ': logging in...')
        sleep(2)
    
    def send_security_code_by_email(self):
        self.browser.find_element(By.ID, 'btnSendCode').click()
        print(str(self) + ': asking for security code to be send via email...')
    
    def enter_security_code(self, code):
        self.browser.find_element(By.NAME, 'oneTimeCode').send_keys(code)
        print(str(self) + ': entering EA security code...')
        self.browser.find_element(By.ID, 'btnSubmit').click()
        print(str(self) + ': submitting EA security code...')
    
    def complete_login_by_gmx(self, fut_username, fut_password, gmx_username, gmx_password):
        self.login(fut_username, fut_password)
        self.send_security_code_by_email()

        mail_gmx = Gmx()
        mail_gmx.login(gmx_username, gmx_password)
        mail_gmx.open_inbox(0)
        code = mail_gmx.get_ea_security_code()
        mail_gmx.browser.close()

        self.enter_security_code(code)

        while self.nav_tab('sbc') == 0:
            print(str(self) + ": waiting 'til homescreen loads...")
            sleep(1)
        sleep(2)
        print(str(self) + ': homescreen loaded!')

    #-----------------------------------------------------------------------

    def nav_tab(self, tab): 
        #possible tabs are: ['home', 'squad', 'transfer', 'store', 
        #                   'club', 'sbc', 'stadium', 'leaderboards', 'settings']
        try:
            nav_tab = self.browser.find_element(By.XPATH, "//nav[@class='ut-tab-bar']/button[@class='ut-tab-bar-item icon-" + tab + "']")
            return nav_tab
        except:
            return 0
    
    def coin_count(self):
        coin_element = self.browser.find_element(By.XPATH, "//*[@class='view-navbar-currency-coins']")
        coin_count = coin_element.text
        print(str(self) + ': retrieving coins count...')
        return coin_count

    def transfer_list_total_count(self):
        #self.nav_tab('transfer').click()
        element = self.browser.find_element(By.XPATH, "//*[@class='total-transfers']/*[@class='value']")
        count = element.text
        return count

    def open_transferlist(self):
        self.nav_tab('transfer').click()
        sleep(2)
        element = self.browser.find_element(By.XPATH, "//*[@class='tile col-1-2 ut-tile-transfer-list']")
        element.click()
        print(str(self) + ': openning transfers list...')

    def open_tranfermarket(self):
        self.nav_tab('transfer').click()
        sleep(2)
        element = self.browser.find_element(By.XPATH, "//*[@class='tile col-1-1 ut-tile-transfer-market']")
        element.click()
        print(str(self) + ': openning transfermarket...')

    def search_player_by_name(self, player_name, player_rating, max_price):
        self.open_tranfermarket()
        sleep(2)

        search_bar = self.browser.find_element(By.XPATH, "//input[@placeholder='Type Player Name']")
        search_bar.send_keys(player_name)
        print(str(self) + ': entering player name...')
        
        player_select = self.browser.find_element(By.XPATH, "//*[@class='btn-subtext' and text()='" + str(player_rating) + "']")
        player_select = player_select.find_element(By.XPATH, '..')
        player_select.click()
        print(str(self) + ': choosing player from search list...')

        try: 
            max_price_input = self.browser.find_element(By.XPATH, "//*[@class='search-prices']/div[6]//input[@class='numericInput']")
            max_price_input.send_keys(str(max_price))
        except: 
            max_price_input = self.browser.find_element(By.XPATH, "//*[@class='search-prices']/div[6]//input[@class='numericInput filled']")
            for i in range(0, len(str(max_price))+1): max_price_input.send_keys(Keys.BACKSPACE)
            #sleep(2)
            max_price_input.send_keys(str(max_price))
        print(str(self) + ': entering max quick_buy price...')

        search_button = self.browser.find_element(By.XPATH, "//button[text()='Search']")
        search_button.click()
        print(str(self) + ': searching transfermarket...')
        sleep(2)

    def relist_transfers(self):
        self.open_transferlist()
        try:
            relist_button = self.browser.find_element(By.XPATH, "//button[text()='Re-list All']")
            print(str(self) + ': relisting all expired items...')
            relist_button.click()
            confirm_button = self.browser.find_element(By.XPATH, "//section[@class='ea-dialog-view ea-dialog-view-type--message']/div/div/button[2]")
            print(str(self) + ': confirming relist...')
            confirm_button.click()
        except ElementNotInteractableException:
            print(str(self) + ': no items to relist...')

    def delete_old_transfers(self, csv_document):
        self.open_transferlist()

        try:
            sold_player_list = self.browser.find_elements(By.XPATH, "//*[@class='ut-transfer-list-view ui-layout-left']/section[1]/ul/li")

            if len(sold_player_list) > 0:
                today = date.today()
                print(today)
                with open(csv_document, 'a', newline='') as c:
                    writer = csv.writer(c)
                    writer.writerow([today, None, None, None])

            for sold_player in sold_player_list:
                player_name_container = sold_player.find_element(By.XPATH, "div/div[@class='entityContainer']/div[@class='name']")
                player_name = player_name_container.text
                sell_price_container = sold_player.find_element(By.XPATH, "div/div[@class='auction']/div[@class='auctionValue']/span[@class='currency-coins value']")
                sell_price = sell_price_container.text

                sell_profit = int(sell_price.replace(',', '')) * 0.95

                player_data = [player_name, None, None, sell_profit]
                print('sold:', player_data)
                with open(csv_document, 'a') as c:
                    writer = csv.writer(c)
                    writer.writerow(player_data)

            clear_button = self.browser.find_element(By.XPATH, "//button[text()='Clear Sold']")
            clear_button.click()

        except: print(self, 'No players are sold!')

    def buy_player_by_name(self, player_name, player_rating, max_price, amount, csv_document): # TODO: add scrolling through pages, if amount>20
        self.search_player_by_name(player_name, player_rating, max_price)

        #TODO make date only write, when players are actually bought
        today = date.today()
        print(today)
        with open(csv_document, 'a', newline='') as c:
            writer = csv.writer(c)
            writer.writerow([today, None, None, None])

        player_list = self.browser.find_elements(By.XPATH, "//*[@class='paginated-item-list ut-pinned-list']//li/div[@class='rowContent has-tap-callback']")
        list_count = 0

        for player in player_list:
            if 'expired' not in player.get_attribute('class'):
                player.click()
                self.browser.find_element(By.XPATH, "//button[@class='btn-standard buyButton currency-coins']").click()
                self.browser.find_element(By.XPATH, "//button/span[text()='Ok']").find_element(By.XPATH, '..').click()

                with open(csv_document, 'a') as c:
                    writer = csv.writer(c)
                    writer.writerow([player_name, max_price, None, None])

                list_count += 1
            if list_count == amount:
                break
            sleep(2)

    def resell_player_by_name(self, player_name, player_rating, max_buy_price, sell_price, amount, csv_document): # TODO: add scrolling through pages, if amount>20
        self.search_player_by_name(player_name, player_rating, max_buy_price)

        '''today = date.today()
        print(today)
        with open(csv_document, 'a', newline='') as c:
            writer = csv.writer(c)
            writer.writerow([today, None, None, None])'''

        player_list = self.browser.find_elements(By.XPATH, "//*[@class='paginated-item-list ut-pinned-list']//li/div[@class='rowContent has-tap-callback']")

        if len(player_list) > 0:
            today = date.today()
            print(today)
            with open(csv_document, 'a', newline='') as c:
                writer = csv.writer(c)
                writer.writerow([today, None, None, None])

        list_count = 0

        for player in player_list:
            if 'expired' not in player.get_attribute('class'):
                player.click()
                print(self, ': buying player nr. ', list_count+1, '...')

                self.browser.find_element(By.XPATH, "//button[@class='btn-standard buyButton currency-coins']").click()
                self.browser.find_element(By.XPATH, "//button/span[text()='Ok']").find_element(By.XPATH, '..').click()
                print(self, ': bought player nr. ', list_count+1, '...')

                try:
                    self.browser.find_element(By.XPATH, "//button/*[text()='List on Transfer Market']").find_element(By.XPATH, '..').click()
                    print(self, ': listinng player nr. ', list_count+1, '...')
                    sleep(1)

                    all_input = self.browser.find_elements(By.XPATH, "//input")
                    bid_input = all_input[0]
                    sell_input = all_input[1]
                    submit_button = self.browser.find_element(By.XPATH, "//button[text()='List for Transfer']")

                    bid_input.send_keys('99999999999)')
                    sleep(1)
                    sell_input.send_keys(Keys.BACKSPACE)
                    sleep(1)
                    sell_input.send_keys(str(sell_price))
                    #sleep(1)

                    for i in range(0, 3): submit_button.send_keys(Keys.ARROW_DOWN)
                    submit_button.click()

                    print(self, ': listed player nr. ', list_count+1, '...')

                    with open(csv_document, 'a') as c:
                        writer = csv.writer(c)
                        writer.writerow([player_name, max_buy_price, sell_price*0.95, None])

                    list_count += 1
                    sleep(0.5)
                except:
                    list_count += 1
            if list_count == amount:
                break
            sleep(1)

    #DEF: buy_pack

    #DEF: open_pack



'''class FutBin(Webpage): #XXX: FutBin
    def __init__(self):
        self.website_url = 'https://www.futbin.com'
        super().__init__(self.website_url)
        sleep(2)
        self.browser.find_element(By.XPATH, "//*[text()='AGREE']").click()
        self.browser.find_element(By.XPATH, "//*[text()='Got it!']").click()
        cookies = 
        self.browser.add_cookie()
    
    def open_index100(self):
        nav_tab_market = self.browser.find_element(By.XPATH, "//a[@id='navbarDropdownMarketLink']")
        ActionChains(self.browser).move_to_element(nav_tab_market).perform()
        dropdown_li_index100 = self.browser.find_element(By.XPATH, "//ul[@aria-labelledby='navbarDropdownMarketLink']/li[2]/a")
        dropdown_li_index100.click()
'''