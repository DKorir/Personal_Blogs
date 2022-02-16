import unittest
from app.models import Quote_api

class Quote_apiTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Quote_api class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_quote_api = Quote_api(1234,'Python Must Be Crazy','A thrilling new Python Series','/khsjha27hbs',8.5,129993)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote_api,Quote_api))