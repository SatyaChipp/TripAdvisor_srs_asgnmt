import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    import unittest
    from Part2_reviews import PRODUCTSandREVIEWS, EmptyDataFrame
    from unittest.mock import MagicMock, patch
    import pandas as pd

import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
logger.addHandler(handler)

class TestPRODUCTSandREVIEWS(unittest.TestCase):

    def setUp(self):
        self.tt = PRODUCTSandREVIEWS()
        self.ref_url = "https://www.tripadvisor.com"
        self.columns_ = ["city_id", "city", "listing_id", "listing_desc",
                       "url", "product_code", "review_id", "user_alias", "user_location",
                       "review_rating", "review_timestamp"]

    def test_products_reviews_one(self):
        self.assertEquals(self.tt.ref_base_url, self.ref_url)
        self.assertEquals(list(self.tt.reviews_details.columns.values), self.columns_)

    @patch('pandas.read_csv')
    def test_get_review_details(self, mock_read_csv):
        pp = PRODUCTSandREVIEWS()
        with self.assertRaises(EmptyDataFrame):
            pp.get_review_details(csv_file='test_listing_tours.csv')
            self.assertTrue(mock_read_csv.called)

    @patch('pandas.read_csv')
    def test_get_review_details(self, mock_read_csv):
        pp = PRODUCTSandREVIEWS()
        data = """scan_date,city_id,city,listing_id,listing_desc,url,review_count,by,price_from,strike_thru_price,is_special_offer\n2018-07-29,g312741,Buenos Aires,d11446055,"Buenos Aires’ neighborhoods each have a distinctive character from the historic barrios of San Telmo and La Boca, to the beautiful parks and plazas of Palermo and Recoleta, and the modern skyscrapers of Puerto... ",https://www.tripadvisor.com/AttractionProductDetail-g312741-d11446055-Small_Group_City_Tour_of_Buenos_Aires-Buenos_Aires_Capital_Federal_District.html,276,Signature Tours,29.5,0\n2018-07-29,g312741,Buenos Aires,d11451016,"Buenos Aires is famous as the birthplace of the tango, and attending a live show is an unforgettable experience for visitors to the city. This tour includes hotel pickup and drop-off, so you don’t have to worry... ",https://www.tripadvisor.com/AttractionProductDetail-g312741-d11451016-Piazzolla_Tango_Show_and_Dinner_in_Buenos_Aires-Buenos_Aires_Capital_Federal_District.html,98,NA,40.46,0\n2018-07-29,g312741,Buenos Aires,d11452356,"There’s so much to see and do in Buenos Aires, and this city sightseeing tour helps first-time visitors get their bearings with visits to all the top sights. Drive through atmospheric neighborhoods including... ",https://www.tripadvisor.com/AttractionProductDetail-g312741-d11452356-Buenos_Aires_Sightseeing_Tour-Buenos_Aires_Capital_Federal_District.html,385,Tangol,16.23,0\n2018-07-29,g312741,Buenos Aires,d11452421,"No visit to Buenos Aires is complete without seeing a tango show. Guarantee your ticket at the often sold-out La Ventana, one of the city’s most prestigious dance venues. Convenient hotel pickup and drop-off means... ",https://www.tripadvisor.com/AttractionProductDetail-g312741-d11452421-La_Ventana_Tango_Show_with_Optional_Dinner_in_Buenos_Aires-Buenos_Aires_Capital_Federal_District.html,55,Tangol,80.0,0\n"""
        with open('test_listing_tours.csv', 'w', encoding='utf-8') as fi:
            logging.disable(logging.CRITICAL)
            for line in data.split('\n'):
                fi.write(str(line) + '\n')
            mock_read_csv.return_value = pd.DataFrame(data.split('\n'))
            mock_read_csv.return_value.index.return_value = len(data.split('\n'))-1
            dd = pp.get_review_details(csv_file='test_listing_tours.csv')
            self.assertTrue(mock_read_csv.called)


    def tearDown(self):
        self.tt = None

def TestSuites__():
    test_suite = unittest.TestSuite()
    return test_suite


if __name__ == '__main__':
    mySuite = TestSuites__()
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(mySuite)