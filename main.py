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
import os
# from selenium.webdriver.common.keys import Keys


class WrongTwitter(Exception):
    def __init__(self, message='Problems with Twitter'):
        super(WrongTwitter, self).__init__(message)


class WrongDiscord(Exception):
    def __init__(self, message='Problems with Discord'):
        super(WrongDiscord, self).__init__(message)


class Selenium:
    def __init__(self, n):
        self.debug_ip = None
        self.webdriver = None
        self.driver = None
        self.n = n
        self.key = None
        self.mnemo = None
        self.dis_token = None
        self.proxy = None
        self.load_credentials()
        self.link = 'https://www.premint.xyz/pillosophers-nft/'
        self.twitter_link = 'https://twitter.com/pillosophers'
        self.discord_link = 'https://discord.gg/ApVzYUSVkB'

    def load_credentials(self):
        with open('datas.json') as file:
            content = json.load(file)
        for el in content:
            if el['name'] == self.n:
                self.key = el['id']
                self.mnemo = el['mnemo']
                self.dis_token = el['token']
                self.proxy = el['proxy']

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
            sleep = round(random.uniform(0.2, 0.5), 2)
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
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Welcome to the Pillhub 💊']")))

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

    # def check_discord(self):
    #     wait = WebDriverWait(self.driver, 5)
    #     home_button = None
    #     self.driver.get('https://discord.com/channels/@me')
    #     # discord home icon
    #     try:
    #         home_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' homeIcon')]")))
    #     except selenium.common.exceptions.TimeoutException:
    #         pass
    #     if home_button is None:
    #         login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
    #         email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
    #         self.hum_write('AShjdjqkkwjqeqwe', email_input)
    #         pass_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    #         self.hum_write('asdqq', pass_input)
    #         pass_input.send_keys(Keys.ENTER)

    def discord_token(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            home_button = None
            self.driver.get('https://discord.com/channels/@me')
            try:
                home_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' homeIcon')]")))
                time.sleep(2)
                wait = WebDriverWait(self.driver, 3)
                time.sleep(2)
                s = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' closeIcon')]")))
                if len(s) == 3:
                    s[2].click()
            except selenium.common.exceptions.TimeoutException:
                pass
            if home_button is None:
                self.driver.execute_script("function login(token) { setInterval(() => { document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `\"${token}\"` }, 50); setTimeout(() => { location.reload(); }, 2500); } login('%s');" % self.dis_token)
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' homeIcon')]")))
                wait = WebDriverWait(self.driver, 3)
                time.sleep(2)
                s = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' closeIcon')]")))
                if len(s) == 3:
                    s[2].click()
        except Exception:
            raise WrongDiscord

    def discord_invite(self):
        try:
            wait = WebDriverWait(self.driver, 3)
            s = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), ' closeIcon')]")))
            if len(s) == 3:
                s[2].click()
        except:
            pass
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-list-item-id='guildsnav___create-join-button']"))).click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), 'footerButton')]"))).click()
        time.sleep(1)
        els = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@type="text"]')))
        els[-1].send_keys(self.discord_link)
        time.sleep(1)
        els = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), 'contents')]")))
        time.sleep(1)
        els[-2].click()
        time.sleep(1)
        els = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), 'closeIcon')]")))
        time.sleep(2)
        els[-1].click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/channels/948547948386603018/948600048390901780"]'))).click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='HappyPill']"))).click()
        time.sleep(1)
        els = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(concat(' ', @class, ' '), 'checkbox')]")))
        time.sleep(1)
        els[-1].click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.XPATH, "//img[@alt='HappyPill']"))).click()
        time.sleep(1)


    # def discord_invite(self, link):
    #     s = requests.Session()
    #     selenium_user_agent = self.driver.execute_script("return navigator.userAgent;")
    #     s.headers.update({"user-agent": selenium_user_agent})
    #     s.headers.update({'authorization': self.dis_token})
    #     s.proxies.update({'http': f'http://{self.proxy}'})
    #     for cookie in self.driver.get_cookies():
    #         s.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    #     response = s.post(f"https://discord.com/api/v9/invites/{link}")
    #     print(response)
    #     print(response.content)
    #     input()
    #     r = s.post("https://discord.com/api/v9/channels/948600048390901780/messages/960284799329767514/reactions/HappyPill:958983259109331014/@me?location=Message")
    #     print(r)
    #     print(r.content)

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

    def connect_discord(self):
        wait = WebDriverWait(self.driver, 4)
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="/accounts/discord/login/?process=connect&next=%2Fpillosophers-nft%2F&scope=guilds.members.read"]'))).click()
        els = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(concat(' ', @class, ' '), 'contents')]")))
        els[-1].click()
        time.sleep(1)

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

    def Youtube_create_acs(self):
        wait = WebDriverWait(self.driver, 5)
        self.driver.get('https://www.youtube.com/')
        wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Avatar image']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Create a channel']"))).click()
        with open('names.txt', encoding='utf8') as file:
            con = json.load(file)
            rng_name = random.choice(con).strip()
        name_inp = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@class="style-scope tp-yt-paper-input"]')))
        name_inp.clear()
        self.hum_write(rng_name, name_inp)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='CREATE CHANNEL']"))).click()
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='title' and @class='header-title style-scope ytd-channel-owner-empty-state-renderer']"), 'Upload a video to get started'))
        random_img = f'{os.getcwd()}\\Аватарки\\{random.choice(os.listdir("Аватарки"))}'
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="yt-simple-endpoint style-scope ytd-channel-avatar-editor"]/parent::*'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Continue"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Close"]'))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text()="Close"]'))).click()
        inputs = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input")))
        inputs[1].send_keys(random_img)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='done-button']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Publish']"))).click()
        wait.until(EC.element_attribute_to_include((By.XPATH, "//*[@id='publish-button']"), 'disabled'))
        os.remove(random_img)
        time.sleep(15)


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
        with open('results_twitter.json') as file:
            content = json.load(file)
        for el in content:
            if el['Result'] != 'Fail':
                self.nums.append(el['Name'])

    def save(self, dic):
        with open('res_you.json') as file:
            content = json.load(file)
        content.append(dic)
        with open('res_you.json', 'w') as file_w:
            json.dump(content, file_w, indent=4)

    def main(self):
        for el in self.base:
            if el['name'] not in [1, 3, 4]:
                try:
                    selen = Selenium(el['name'])
                    selen.start()
                    selen.connect()
                    selen.close_all_tabs()
                    selen.Youtube_create_acs()
                    selen.close()
                    self.save({'Name': el['name'], 'Result': 'Success'})
                except Exception:
                    self.save({'Name': el['name'], 'Result': 'Fail'})
                    selen.close()
                time.sleep(35)


if __name__ == '__main__':
    x = Worker()
    x.main()
    # x = Selenium(4)
    # x.start()
    # x.connect()
    # x.code_input()
    # x.close()
