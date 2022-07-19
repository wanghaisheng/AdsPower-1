import json
import time
import requests
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import selenium.common.exceptions
import random


class WrongTwitter(Exception):
    def __init__(self, message='Problems with Twitter'):
        super(WrongTwitter, self).__init__(message)


class WrongDiscord(Exception):
    def __init__(self, message='Problems with Discord'):
        super(WrongDiscord, self).__init__(message)


class Selenium:
    def __init__(self, key, mnemo):
        self.debug_ip = None
        self.webdriver = None
        self.driver = None
        self.key = key
        self.mnemo = mnemo
        self.link = 'https://www.premint.xyz/yakuzzi-free-mint/'
        self.twitter_link = 'https://twitter.com/yakuzziofficial'

    def start(self):
        url = 'http://local.adspower.com:50325/api/v1/browser/start'
        prms = {'user_id': self.key}
        r = requests.get(url, params=prms).json()
        self.debug_ip = r['data']['ws']['selenium']
        self.webdriver = r['data']['webdriver'].split('webdriver_')[-1].split('\\chromedriver.exe')[0]

    def connect(self):
        options = webdriver.ChromeOptions()
        options.debugger_address = self.debug_ip
        options.headless = True
        self.driver = uc.Chrome(version_main=self.webdriver, options=options)

    def close(self):
        url = 'http://local.adspower.com:50325/api/v1/browser/stop'
        prms = {'user_id': self.key}
        requests.get(url, params=prms)

    def hum_write(self, text, elem):
        for buk in text:
            elem.send_keys(buk)
            sleep = round(random.uniform(0.5, 0.10), 2)
            time.sleep(sleep)

    def close_all_tabs(self):
        n_tabs = len(self.driver.window_handles) - 1
        for n in range(n_tabs):
            window = self.driver.window_handles[0]
            self.driver.switch_to.window(window)
            self.driver.close()
        window = self.driver.window_handles[0]
        self.driver.switch_to.window(window)

    def check_metamask(self):
        self.driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, '//button')))
        if 'Connecting you to Ethereum and the Decentralized Web.' in self.driver.page_source:
            self.log_to_metamask()
        if 'Welcome Back!' in self.driver.page_source:
            wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@id='password']"))).send_keys('11111111')
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Unlock']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Send']")))
            if "What's new" in self.driver.page_source:
                wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Close']"))).click()

    def log_to_metamask(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Get Started']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Import wallet']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='No Thanks']"))).click()
        for number, word in enumerate(self.mnemo.split()):
            wait.until(
                EC.presence_of_element_located((By.XPATH, f"//input[@id='import-srp__srp-word-{number}']"))).send_keys(
                word)

        wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@id='password']"))).send_keys('11111111')
        wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@id='confirm-password']"))).send_keys('11111111')
        wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@class='check-box far fa-square']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Import']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='All Done']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Send']")))
        if "What's new" in self.driver.page_source:
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Close']"))).click()
        if len(self.driver.window_handles) == 2:
            self.driver.close()
            window = self.driver.window_handles[0]
            self.driver.switch_to.window(window)

    def wallet_connect(self):
        wait = WebDriverWait(self.driver, 4)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Connect']"))).click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//*[@class='btn btn-styled btn-base-1 btn-block btn-circle']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Connect to your MetaMask Wallet']"))).click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Next']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Connect']"))).click()
        except:
            pass
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Sign']"))).click()
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[text()="Click here if you\'d like to connect a new wallet to your account"]')))

    def connect_twitter(self):
        wait = WebDriverWait(self.driver, 4)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='step-twitter']//a"))).click()
        time.sleep(2)
        if 'This social account is connected to another one of your wallets. To fix: https://premint.xyz/disconnect/' in self.driver.page_source:
            self.driver.switch_to.new_window()
            self.driver.get('https://premint.xyz/disconnect/')
            self.driver.switch_to.window(self.driver.window_handles[-1])
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "// *[ @ id = 'st-container'] // a[contains(@href, 'twitter')]"))).click()
            time.sleep(2)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='step-twitter']//a"))).click()
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@class='btn btn-styled btn-base-1 btn-block btn-circle']"))).click()
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='Connect to your MetaMask Wallet']"))).click()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Sign']"))).click()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(self.link)
            wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='step-twitter']//a"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-dismiss='alert']")))
        else:
            wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='allow']"))).click()

    def register(self):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[text()='Good Luck! Share on twitter to double your chances!']")))

    def follow_twitter(self):
        wait = WebDriverWait(self.driver, 6)
        self.driver.switch_to.new_window()
        self.driver.get(self.twitter_link)
        wait.until(EC.presence_of_element_located((By.XPATH, "// span[text() = 'Follow']"))).click()
        time.sleep(1)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def register_premint(self):
        self.driver.get(self.link)
        self.wallet_connect()
        self.follow_twitter()
        self.connect_twitter()
        self.register()

    def check_discord(self):
        wait = WebDriverWait(self.driver, 5)
        home_button = None
        self.driver.get('https://discord.com/channels/@me')
        # discord home icon
        try:
            home_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' homeIcon')]")))
        except selenium.common.exceptions.TimeoutException:
            pass
        if home_button is None:
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))).send_keys('Haha')
            self.hum_write('AShjdjqkkwjqeqwe', email_input)


    def check_twitter(self):
        wait = WebDriverWait(self.driver, 3)
        self.driver.get('https://twitter.com/home')
        time.sleep(2)
        try:
            like = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='like']/div/div")))
            like.click()
        except selenium.common.exceptions.TimeoutException:
            pass
        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[text()='Your account is suspended and is not permitted to perform this action.']")))
            raise WrongTwitter()
        except selenium.common.exceptions.TimeoutException:
            pass
        try:
            self.driver.find_element(By.XPATH,
                                     "//span[text()=\"This request looks like it might be automated. To protect our users from spam and other malicious activity, we can’t complete this action right now. Please try again later.\"]")
            raise WrongTwitter()
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def browser_preparation(self):
        self.close_all_tabs()
        self.check_twitter()
        self.check_metamask()

    def code_input(self):
        while True:
            try:
                a = input()
                if a == "stop":
                    break
                exec(a)
            except Exception as e:
                print(e)
                continue
            print('SUCCES')

    def main(self):
        self.start()
        self.connect()
        self.browser_preparation()
        self.register_premint()
        self.close()


class Worker:
    def __init__(self):
        with open('datas.json') as file:
            self.base = json.load(file)
        self.nums = [58]

    def refresh(self):
        with open('results.json') as file:
            content = json.load(file)
        for el in content:
            if el['Result'] != 'Fail':
                self.nums.append(el['Name'])

    def save(self, dic):
        with open('results1.json') as file:
            content = json.load(file)
        content.append(dic)
        with open('results1.json', 'w') as file_w:
            json.dump(content, file_w, indent=4)

    def main(self):
        # self.refresh()
        for el in self.base:
            if el['name'] in self.nums:
                try:
                    selen = Selenium(el['id'], el['mnemo'])
                    selen.main()
                    self.save({'Name': el['name'], 'Result': 'Success'})
                except WrongTwitter:
                    self.save({'Name': el['name'], 'Result': 'BadTwitter'})
                    selen.close()
                except Exception:
                    self.save({'Name': el['name'], 'Result': 'Fail'})
                    selen.close()


if __name__ == '__main__':
    # x = Worker()
    # x.main()
    x = Selenium('j329vl3', 'x')
    x.start()
    x.connect()
    x.code_input()
    x.close()
