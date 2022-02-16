import urllib.request,json
from .models import Quote_api

#Quote=quote.quote
# Getting the movie base url

api_key = None
base_url = None
def configure_request(app):
    global api_key,base_url
    base_url = app.config['QUOTES_API_BASE_URL']


def get_quotes_api(category):
    '''
    Function that gets the json response to our url request
    '''
    get_quotes_api_url = base_url.format(category,api_key)

    with urllib.request.urlopen(get_quotes_api_url) as url:
        get_quotes_api_data = url.read()
        get_quotes_api_response = json.loads(get_quotes_api_data)

        quote_api_results = None

        if get_quotes_api_response['results']:
            quote_api_results_list = get_quotes_api_response['results']
            quote_api_results = quote_api_results(quote_api_results_list)


    return quote_api_results

def process_results(quote_api_list):
    '''
    Function  that processes the movie result and transform them to a list of Objects

    Args:
        movie_list: A list of dictionaries that contain movie details

    Returns :
        movie_results: A list of movie objects
    '''
    quote_api_results = []
    for quote_api_item in quote_api_list:
        id = quote_api_item.get('id')
        author = quote_api_item.get('author')
        permalink = quote_api_item.get('permalink')
        quote = quote_api_item.get('quote')
        

        if quote:
            quote_api_object = Quote_api(id,author,permalink,quote)
            quote_api_results.append(quote_api_object)

    return quote_api_results