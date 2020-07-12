from card_info import CardInfo
from utils.helper import get_condition, get_card_info, get_best_prices, print_card_list

keyworks = 'IOC-025'
edition = '1st Edition'
condition = ''
language = 'English'
tipo_cambio = 581

# Get card info
cards = get_card_info(card_key=keyworks, edition=edition, condition=condition)
card_list = []

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
        for item in items:
            c = get_condition(item.find_all("div", class_="col-3 text-center p-1")[1].text)

            p = float(item.find_all("div", class_="col-2 text-center p-1")[0].text.replace('$', '').replace(',', ''))
            quantity = int(item.find_all("option")[len(item.find_all("option")) - 1].attrs['value'])
            card1 = CardInfo(card_name=card_name, card_key=card_key, condition=c,
                             price=p, edition=edition_, rarity=rarity, quantity=quantity)
            card_list.append(card1)

    card_list = get_best_prices(card_list=card_list)
    print_card_list(card_list=card_list, tipo_cambio=tipo_cambio)

else:
    print(f'La carta "{keyworks}" {edition} {condition} "NO" tiene stock!')
