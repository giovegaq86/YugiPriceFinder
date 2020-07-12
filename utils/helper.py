import requests
from bs4 import BeautifulSoup
from card_info import CardInfo


def get_condition(text):
    condition = ''

    if 'Played' in text:
        condition = 'Played'
    elif 'Near' in text:
        condition = 'Near Mint'

    return condition


def print_card_list(card_list, tipo_cambio):
    for card in card_list:
        print(f'Card name: {card.card_name}')
        print(f'Card key: {card.card_key}')
        print(f'Rarity: {card.rarity}')
        print(f'Condition: {card.condition}')
        print(f'Edition: {card.edition}')
        print(f'Quantity: {card.quantity}')
        print(f'Price: ₡{format(float(card.price) * tipo_cambio, ",.0f")}')
        print('\n')

    print(f'It was found {len(card_list)} results.')


def get_card_info(card_key, edition, condition, source):
    if source == 't&t':
        base_url = 'https://www.trollandtoad.com'

        if edition == 'Unlimited':
            search_words = card_key
        else:
            search_words = f'{card_key}+{edition.replace(" ", "+")}'

        url = f'{base_url}/category.php?hide-oos=on&' \
              f'min-price=&' \
              f'max-price=&' \
              f'items-pp=240&' \
              f'item-condition={condition}&' \
              f'search-words={search_words}&' \
              f'selected-cat=4736&' \
              f'sort-order=L-H&' \
              f'page-no=1&' \
              f'view=list&' \
              f'subproduct=0'

        html = requests.get(url=url).text
        parsed_html = BeautifulSoup(html, 'html.parser')
        cards = parsed_html.find_all("div", class_="card h-100 p-3")

        return cards


def get_best_prices(card_list, keywords):
    filtered_card_list = []
    fupp = 99999
    upp = 99999
    nmp = 99999
    fnmp = 99999
    ump = 99999
    lmp = 99999

    for card in card_list:
        if card.edition == '1st Edition' and card.condition == 'Played' and fupp > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            fupp = card.price
        elif card.edition == 'Unlimited' and card.condition == 'Played' and upp > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            upp = card.price
        elif card.edition == 'Limited Edition' and card.condition == 'Played' and nmp > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            nmp = card.price
        elif card.edition == '1st Edition' and card.condition == 'Near Mint' and fnmp > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            fnmp = card.price
        elif card.edition == 'Unlimited' and card.condition == 'Near Mint' and ump > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            ump = card.price
        elif card.edition == 'Limited Edition' and card.condition == 'Near Mint' and lmp > card.price:
            filtered_card_list.append(card.get_dict_card_info())
            lmp = card.price

    filtered_card_list.sort(key=myFunc)

    return {keywords: filtered_card_list}


def myFunc(e):
    return e['price']


def tyt_get_prices(keywords, edition, condition, language):
    # Get card info
    cards = get_card_info(card_key=keywords, edition=edition, condition=condition, source='t&t')
    card_list = []
    tipo_cambio = 585

    if len(cards) > 0:
        for card in cards:
            card_info = card.find_all("a", class_="card-text")[0].text

            if language == 'English' and 'Asian' in card_info or 'Spanish' in card_info:
                break
            elif edition == '1st Edition' and 'Unlimited' in card_info:
                break
            elif edition == 'Unlimited' and '1st' in card_info:
                break

            if '1st Edition' in card_info:
                edition_ = '1st Edition'
            elif 'Unlimited' in card_info:
                edition_ = 'Unlimited'
            elif 'Limited Edition' in card_info:
                edition_ = 'Limited Edition'

            rarity = card_info.split(' - ')[-1].replace(f' {edition_}', '')
            card_key = card_info.replace(f' - {rarity} {edition_}', '').split(' - ')[-1]
            card_name = card_info.replace(f' - {card_key} - {rarity} {edition_}', '')
            items = card.find_all("div", class_="row position-relative align-center py-2 m-auto")
            expansion = card.find_all("a")[2].text.replace(f' [{card_key.split("-")[0]}]', '')\
                .replace(f' {edition_}', '').replace(f' Singles', '')
            image = card.find_all("img")[0].attrs['data-src']
            for item in items:
                c = get_condition(item.find_all("div", class_="col-3 text-center p-1")[1].text)

                p = float(
                    item.find_all("div", class_="col-2 text-center p-1")[0].text.replace('$', '').replace(',', ''))
                pc = f'₡{format(float(p) * tipo_cambio, ",.0f")}'
                quantity = int(item.find_all("option")[len(item.find_all("option")) - 1].attrs['value'])
                card1 = CardInfo(card_name=card_name, card_key=card_key, condition=c,
                                 price=p, pricec=pc, edition=edition_, rarity=rarity, quantity=quantity,
                                 expansion=expansion, image=image)
                card_list.append(card1)

        card_list = get_best_prices(card_list=card_list, keywords=keywords)
        return card_list
    else:
        print(f'La carta "{keywords}" {edition} {condition} "NO" tiene stock!')
