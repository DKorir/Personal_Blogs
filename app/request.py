import urllib.request,json
from .models import Quote_api

#Quote=quote.quote
# Getting the movie base url


def get_quotes_api():
    '''
    Function that gets the json response to our url request
    '''
    get_quotes_api_url = 'http://quotes.stormconsultancy.co.uk/random.json'

    with urllib.request.urlopen(get_quotes_api_url) as url:
        get_quotes_api_data = url.read()
        quotes_api_response = json.loads(get_quotes_api_data)

        quote_api_results = None

    if quotes_api_response:
        id = quotes_api_response.get('id')
        author = quotes_api_response.get('author')
        quote = quotes_api_response.get('quote')
        permalink =quotes_api_response.get('permalink')
            
        quote_api_results = Quote_api(id, author, quote, permalink)
    print(quote_api_results)
    return quote_api_results