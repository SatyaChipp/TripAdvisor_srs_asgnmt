import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    import unittest
    from Part1_Tours_Tickets import TOURSandTICKETS
    from unittest.mock import MagicMock, patch
import os.path
import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
logger.addHandler(handler)


class TestTOURSandTICKETS(unittest.TestCase):

    def setUp(self):
        self.tt = TOURSandTICKETS()
        self.ref_url = "https://www.tripadvisor.com"
        self.columns_ = ["scan_date", "city_id", "city", "listing_id", "listing_desc",
                    "url", "review_count", "by", "price_from", "strike_thru_price",
                    "is_special_offer"]


    def test_get_top20_one(self):
        self.assertEquals(self.tt.ref_base_url, self.ref_url)
        self.assertEquals(list(self.tt.details_dataframe.columns.values), self.columns_)


    @patch('urllib.request.urlopen')
    def test_get_body(self, mock_urllib_open):
        call_ = TOURSandTICKETS()
        mock_urllib_open.return_value.__enter__.return_value.read.return_value = 'mocked'
        body = call_.get_body("http://www.sample.com")
        mock_urllib_open.assert_called


    def test_capture_listings(self):
        tt = TOURSandTICKETS()
        cities_html = ['http://www.sample1/product1.html', 'http://www.sample1/product1.html']
        #check exception is not raised
        try:
            df = tt.capture_all_listings(cities_html, csv_filename='test_file.csv')
            self.assertEqual(len(df.index), 0)
            self.assertTrue(os.path.isfile('test_file.csv'))
            #above logs HTTP 404 error but does not raise exception
        except:
            self.fail("Encountered an Exception")


    def tearDown(self):
        self.tt = None


def TestSuites__():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestTOURSandTICKETS))
    return test_suite


if __name__ == '__main__':
    mySuite = TestSuites__()
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(mySuite)