

class CardInfo:
    def __init__(self, card_name, card_key, price=0, pricec="", condition="", edition="", rarity="", quantity=0):
        self.card_name = card_name
        self.card_key = card_key
        self.price = price
        self.pricec = pricec
        self.condition = condition
        self.edition = edition
        self.rarity = rarity
        self.quantity = quantity

    def get_dict_card_info(self):
        dict_card_info = {
                            "card_name": self.card_name,
                            "card_key": self.card_key,
                            "price": self.price,
                            "pricec": self.pricec,
                            "condition": self.condition,
                            "edition": self.edition,
                            "rarity": self.rarity,
                            "quantity": self.quantity
                          }
        return dict_card_info


