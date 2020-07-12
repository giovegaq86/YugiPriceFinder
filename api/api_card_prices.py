from flask import Flask, request
from flask_restful import Api

from utils.helper import tyt_get_prices

app = Flask(__name__)
api = Api(app)


@app.route('/api/get_price', methods=['GET'])
def get():
    try:
        bar = request.args.to_dict()
        keywords = ''
        edition = ''
        condition = ''
        language = 'English'

        if 'keywords' in bar:
            keywords = str(bar['keywords']).upper()
        else:
            raise Exception('Keywords were not provided!')
        if 'edition' in bar:
            edition = bar['edition']
        if 'condition' in bar:
            condition = bar['condition']
        if 'language' in bar:
            language = bar['language']

        card_list = tyt_get_prices(keywords=keywords, edition=edition, condition=condition, language=language)
        return card_list
    except Exception as e:
        return e


if __name__ == '__main__':
    app.run(port='5002')
