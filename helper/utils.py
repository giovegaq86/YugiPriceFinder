import json

import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession
from bs4 import BeautifulSoup


class Utils:
    def get_condition(self, text):
        text = text.upper()
        condition = ''

        if 'DAMAGED' in text:
            condition = 'Damaged'
        elif 'HEAVILY' in text:
            condition = 'Heavily Played'
        elif 'LIGHTLY' in text:
            condition = 'Lightly Played'
        elif 'MODERATELY' in text:
            condition = 'Moderately Played'
        elif 'NEAR' in text:
            condition = 'Near Mint'
        elif 'PLAYED' in text:
            condition = 'Played'
        elif 'SEE IMAGE FOR CONDITION' in text:
            condition = 'See Image For Condition'

        return condition

    def convert_condition(self, condition):
        condition = condition.upper()
        if condition == 'NM':
            condition = 'Near Mint'
        elif condition == 'LM':
            condition = 'Lightly Played'
        elif condition == 'MP':
            condition = 'Moderately Played'
        elif condition == 'PL':
            condition = 'Played'
        elif condition == 'HP':
            condition = 'Heavily Played'
        elif condition == 'D':
            condition = 'Damaged'

        return condition

    def get_edition(self, text):
        text = text.upper()
        edition = ''

        if '1ST' in text:
            edition = '1st Edition'
        elif 'UNLIMITED' in text:
            edition = 'Unlimited'
        elif 'LIMITED' in text:
            edition = 'Limited Edition'
        else:
            edition = 'Unlimited'

        return edition

    def myFunc(self, e):
        return e['price']

    def create_web_driver(self, headless=True):
        print('Creating web driver')
        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        print('Webdriver was created correctly')
        return driver

    def get_parsed_html(self, url, use_selenium=False):
        if use_selenium:
            driver = self.create_web_driver()
            driver.get(url)
            html = driver.page_source
            parsed_html = BeautifulSoup(html, 'html.parser')
            driver.close()
        else:
            session = HTMLSession()
            html = session.get(url).content
            parsed_html = BeautifulSoup(html, 'html.parser')

        return parsed_html

    def filter_list(self, card_list):
        new_card_list = []
        fe = None
        ue = None
        le = None
        for card in card_list:
            if card['edition'] == '1st Edition':
                if not fe:
                    fe = card
                elif fe['price'] > card['price']:
                    fe = card
            elif card['edition'] == 'Unlimited':
                if not ue:
                    ue = card
                elif ue['price'] > card['price']:
                    ue = card
            elif card['edition'] == 'Limited Edition':
                if not le:
                    le = card
                elif le['price'] > card['price']:
                    le = card

        if fe:
            new_card_list.append(fe)
        if ue:
            new_card_list.append(ue)
        if le:
            new_card_list.append(le)

        if new_card_list:
            new_card_list.sort(key=self.myFunc)

        return new_card_list

    def get_prices_by_condition(self, card_list):
        damaged_list = []
        heavily_list = []
        lightly_list = []
        played_list = []
        moderately_list = []
        mint_list = []
        unknown_list = []
        for card in card_list:
            if card['condition'] == 'Damaged':
                damaged_list.append(card)
            if card['condition'] == 'Heavily Played':
                heavily_list.append(card)
            if card['condition'] == 'Moderately Played':
                moderately_list.append(card)
            if card['condition'] == 'Lightly Played':
                lightly_list.append(card)
            if card['condition'] == 'Played':
                played_list.append(card)
            if card['condition'] == 'Near Mint':
                mint_list.append(card)
            if 'See Image For Condition' in card['condition']:
                unknown_list.append(card)

        damaged_list = self.filter_list(card_list=damaged_list)
        heavily_list = self.filter_list(card_list=heavily_list)
        moderately_list = self.filter_list(card_list=moderately_list)
        lightly_list = self.filter_list(card_list=lightly_list)
        played_list = self.filter_list(card_list=played_list)
        mint_list = self.filter_list(card_list=mint_list)
        unknown_list = self.filter_list(card_list=unknown_list)

        return {
            'Damaged': damaged_list,
            'HeavilyPlayed': heavily_list,
            'ModeratelyPlayed': moderately_list,
            'LightlyPlayed': lightly_list,
            'Played': played_list,
            'NearMint': mint_list,
            'SeeImageForCondition': unknown_list
        }

    def get_prices_by_condition2(self, card_list):
        damaged_list = []
        heavily_list = []
        lightly_list = []
        played_list = []
        moderately_list = []
        mint_list = []
        unknown_list = []
        for card in card_list:
            if card['condition'] == 'Damaged':
                damaged_list.append(card)
            if card['condition'] == 'Heavily Played':
                heavily_list.append(card)
            if card['condition'] == 'Moderately Played':
                moderately_list.append(card)
            if card['condition'] == 'Lightly Played':
                lightly_list.append(card)
            if card['condition'] == 'Played':
                played_list.append(card)
            if card['condition'] == 'Near Mint':
                mint_list.append(card)
            if 'See Image For Condition' in card['condition']:
                unknown_list.append(card)

        damaged_list = self.filter_list(card_list=damaged_list)
        heavily_list = self.filter_list(card_list=heavily_list)
        moderately_list = self.filter_list(card_list=moderately_list)
        lightly_list = self.filter_list(card_list=lightly_list)
        played_list = self.filter_list(card_list=played_list)
        mint_list = self.filter_list(card_list=mint_list)
        unknown_list = self.filter_list(card_list=unknown_list)

        return damaged_list+heavily_list+moderately_list+lightly_list+played_list+mint_list+unknown_list

    def get_prices_by_edition(self, card_list):
        first_edition_list = []
        unlimited_list = []
        limited_list = []

        count = 0
        card_key = ""
        card_name = ""
        expansion = ""
        image = ""

        for card in card_list:
            if count == 0:
                card_key = card['card_key']
                card_name = card['card_name']
                expansion = card['expansion']
                image = card['image']

            if card['edition'] == '1st Edition':
                first_edition_list.append(card)
            if card['edition'] == 'Unlimited':
                unlimited_list.append(card)
            if card['edition'] == 'Limited Edition':
                limited_list.append(card)
            count += 1

        card_list = self.get_prices_by_condition2(first_edition_list) + self.get_prices_by_condition2\
            (unlimited_list) + self.get_prices_by_condition2(limited_list)

        return {
            "card_key": card_key,
            "card_name": card_name,
            "expansion": expansion,
            "image": image,
            "card_list": card_list
        }

    def get_best_prices(self, card_list):
        damaged_list = []
        heavily_list = []
        lightly_list = []
        played_list = []
        moderately_list = []
        mint_list = []
        unknown_list = []
        for card in card_list:
            if card['condition'] == 'Damaged':
                damaged_list.append(card)
            if card['condition'] == 'Heavily Played':
                heavily_list.append(card)
            if card['condition'] == 'Moderately Played':
                moderately_list.append(card)
            if card['condition'] == 'Lightly Played':
                lightly_list.append(card)
            if card['condition'] == 'Played':
                played_list.append(card)
            if card['condition'] == 'Near Mint':
                mint_list.append(card)
            if 'See Image For Condition' in card['condition']:
                unknown_list.append(card)

        damaged_list = self.filter_list(card_list=damaged_list)
        heavily_list = self.filter_list(card_list=heavily_list)
        moderately_list = self.filter_list(card_list=moderately_list)
        lightly_list = self.filter_list(card_list=lightly_list)
        played_list = self.filter_list(card_list=played_list)
        mint_list = self.filter_list(card_list=mint_list)
        unknown_list = self.filter_list(card_list=unknown_list)

        return damaged_list + heavily_list + moderately_list + lightly_list + played_list + mint_list + unknown_list


    def get_exchange_rate(self):
        url='https://tipodecambio.paginasweb.cr/api'
        results = requests.get(url=url)
        exchange_rate = float(json.loads(results.content)['venta'])

        return exchange_rate