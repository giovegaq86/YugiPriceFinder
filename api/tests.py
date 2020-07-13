from helper.tcgplayer_utils import TCGPlayerUtils

tcg = TCGPlayerUtils(exchange_rate=585)

RESULTS = tcg.get_prices(set_code='IOC-000')