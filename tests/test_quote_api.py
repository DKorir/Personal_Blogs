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
        self.new_quote_api = Quote_api(1234,'N.J. Rubenking','Writing the first 90 percent of a computer program takes 90 percent of the time. The remaining ten percent also takes 90 percent of the time and the final touches also take 90 percent of the time.',12.10.2012')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote_api,Quote_api))