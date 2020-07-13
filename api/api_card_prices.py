from multiprocessing.pool import ThreadPool

from flask import Flask, request
from flask_restful import Api

from helper.tcgplayer_utils import TCGPlayerUtils
from helper.tyt_utils import TYTUtils
from helper.utils import Utils

app = Flask(__name__)
api = Api(app)
utils = Utils()
exchange_rate = utils.get_exchange_rate()
tcgp = TCGPlayerUtils(exchange_rate=exchange_rate)
tyt = TYTUtils(exchange_rate=exchange_rate)


@app.route('/api/get_price_by_category', methods=['GET'])
def get_price_by_category():
    try:
        bar = request.args.to_dict()
        keywords = ''
        edition = ''
        condition = ''
        language = 'English'
        website = 'both'
        hide_oos = False

        if 'set_code' in bar:
            set_code = str(bar['set_code']).upper()
        else:
            raise Exception('Keywords were not provided!')
        if 'edition' in bar:
            edition = bar['edition']
        if 'condition' in bar:
            condition = bar['condition']
        if 'language' in bar:
            language = bar['language']
        if 'website' in bar:
            website = bar['website']
        if 'hideoos' in bar:
            hide_oos = eval(bar['hideoos'].title())

        tcgp_card_list = []
        tyt_card_list = []

        pool = ThreadPool(processes=2)
        if website == 'both':
            t1 = pool.apply_async(tcgp.get_prices, (set_code, edition, condition))
            t2 = pool.apply_async(tyt.get_prices, (set_code, edition, condition, language, hide_oos))

            tcgp_card_list = t1.get()
            tyt_card_list = t2.get()
        elif website == 'TYT':
            tyt_card_list = tyt.get_prices(set_code=set_code, edition=edition, condition=condition, language=language,
                                           hide_oos=hide_oos)
        elif website == 'TCGP':
            tcgp_card_list = tcgp.get_prices(set_code=set_code, edition=edition, condition=condition)

        card_list = tcgp_card_list + tyt_card_list
        card_list = utils.get_prices_by_condition(card_list=card_list)

        return {'results': card_list}

    except Exception as e:
        return e

@app.route('/api/get_price_by_edition', methods=['GET'])
def get_price_by_edition():
    try:
        bar = request.args.to_dict()
        keywords = ''
        edition = ''
        condition = ''
        language = 'English'
        website = 'both'
        hide_oos = False

        if 'set_code' in bar:
            set_code = str(bar['set_code']).upper()
        else:
            raise Exception('Keywords were not provided!')
        if 'edition' in bar:
            edition = bar['edition']
        if 'condition' in bar:
            condition = bar['condition']
        if 'language' in bar:
            language = bar['language']
        if 'website' in bar:
            website = bar['website']
        if 'hideoos' in bar:
            hide_oos = eval(bar['hideoos'].title())

        tcgp_card_list = []
        tyt_card_list = []

        pool = ThreadPool(processes=2)
        if website == 'both':
            t1 = pool.apply_async(tcgp.get_prices, (set_code, edition, condition))
            t2 = pool.apply_async(tyt.get_prices, (set_code, edition, condition, language, hide_oos))

            tcgp_card_list = t1.get()
            tyt_card_list = t2.get()
        elif website == 'TYT':
            tyt_card_list = tyt.get_prices(set_code=set_code, edition=edition, condition=condition, language=language,
                                           hide_oos=hide_oos)
        elif website == 'TCGP':
            tcgp_card_list = tcgp.get_prices(set_code=set_code, edition=edition, condition=condition)

        card_list = tcgp_card_list + tyt_card_list
        results = utils.get_prices_by_edition(card_list=card_list)

        return {"results": results}

    except Exception as e:
        return e


@app.route('/api/get_price', methods=['GET'])
def get_price():
    try:
        bar = request.args.to_dict()
        keywords = ''
        edition = ''
        condition = ''
        language = 'English'
        website = 'both'
        hide_oos = False

        if 'set_code' in bar:
            set_code = str(bar['set_code']).upper()
        else:
            raise Exception('Keywords were not provided!')
        if 'edition' in bar:
            edition = bar['edition']
        if 'condition' in bar:
            condition = bar['condition']
        if 'language' in bar:
            language = bar['language']
        if 'website' in bar:
            website = bar['website']
        if 'hideoos' in bar:
            hide_oos = eval(bar['hideoos'].title())

        tcgp_card_list = []
        tyt_card_list = []

        pool = ThreadPool(processes=2)
        if website == 'both':
            t1 = pool.apply_async(tcgp.get_prices, (set_code, edition, condition))
            t2 = pool.apply_async(tyt.get_prices, (set_code, edition, condition, language, hide_oos))

            tcgp_card_list = t1.get()
            tyt_card_list = t2.get()
        elif website == 'TYT':
            tyt_card_list = tyt.get_prices(set_code=set_code, edition=edition, condition=condition, language=language,
                                           hide_oos=hide_oos)
        elif website == 'TCGP':
            tcgp_card_list = tcgp.get_prices(set_code=set_code, edition=edition, condition=condition)

        card_list = tcgp_card_list + tyt_card_list
        card_list = utils.get_best_prices(card_list=card_list)

        return {'results': card_list}

    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(port='1234', host='0.0.0.0', debug=True)
