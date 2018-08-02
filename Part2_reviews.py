"""
**Part 2**: Use the captured listings URL and capture the reviews with their review timestamps
+ Use the captured listings’ URL as a queue and visit the individual listing pages
+ Capture all the reviews available on the site for the listing. i.e. page through the reviews
+ Capture the city_id | city | listing_id | listing_desc | url | product_code |  review_id | user_alias |  user_location | review_rating | review_timestamp
https://www.tripadvisor.com/AttractionProductDetail-g294317-d11483317-Machu_Picchu_Private_Guided_Tour_from_Aguas_Calientes-Sacred_Valley_Cusco_Region.html
*Review section*
There are cases where the review count from Part 1 does not match the number of reviews available in Part 2, because TripAdvisor is including reviews from Viator in Part 1.  See the "Read 45 more reviews on Viator" link.  Capturing Viator related reviews is outside the scope of this exercise.
![Reviews](https://s3.amazonaws.com/srs-interview/tripattraction/reviews.png)
Product code is located at the bottom of the right sidebar.
![Questions](https://s3.amazonaws.com/srs-interview/tripattraction/questions.png)
"""

class EmptyDataFrame(Exception):
    pass

import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    from dateutil.parser import parse
    from urllib.request import urlopen
    import pandas as pd
    from bs4 import BeautifulSoup
    import re
    import logging
    import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s"))
logger.addHandler(handler)


class PRODUCTSandREVIEWS(object):
    def __init__(self):
        self.ref_base_url = "https://www.tripadvisor.com"
        self.reviews_details = pd.DataFrame(columns=["city_id", "city", "listing_id", "listing_desc",
                                                       "url", "product_code", "review_id", "user_alias", "user_location",
                                                       "review_rating", "review_timestamp"])
    def get_review_details(self, csv_file=None):
        if not csv_file:
            csv_file = 'listing_tours.csv'
        df = pd.read_csv(csv_file, sep=',')

        if len(df.index) == 0:
            raise EmptyDataFrame("Dataframe is empty, check csv file")

        for index, row in df.iterrows():
            try:
                if str(row['url']) != self.ref_base_url:
                    logger.info("Reviews from : {}".format(str(row['url'])))
                    body_ = urlopen(str(row['url'])).read()
                    soup = BeautifulSoup(body_, 'html.parser')
                    data = soup.findAll('div', attrs={'class': 'review-container'})
                    product_code = soup.findAll('span', attrs={'class': 'prodCode'})[0].text ##gets random text -- corrupt?

                    for i in data:
                        rating_date__ = i.findAll('span', attrs={'class': 'ratingDate relativeDate'})
                        rating_date = parse(re.findall('title="(.*?)"', str(rating_date__), re.DOTALL)[0]).strftime('%d/%m/%Y')

                        review_rating__ = i.findAll('div', attrs={'class': 'rating reviewItemInline'})
                        review_rating  = float(re.findall('class="ui_bubble_rating (.*?)"', str(review_rating__[0].find('span')), re.DOTALL)[0]
                                               .split('_')[1])//10 if len(review_rating__)!=0 and review_rating__[0].find('span') else 'NA'

                        user_alias__ = i.findAll('div', attrs={'class': 'username mo'})
                        user_alias = user_alias__[0].find('span').text if len(user_alias__)!=0 else 'NA'

                        find_reviewID__ = re.findall('data-reviewid="(.*?)"', str(i), re.DOTALL)
                        find_reviewID = find_reviewID__[0] if len(find_reviewID__)!=0 else 'NA'

                        location__ = i.findAll('div', attrs={'class': 'location'})
                        location = location__[0].find('span').text if len(location__)!=0 else 'NA'

                        self.reviews_details.loc[self.reviews_details.shape[0]] = [row['city_id'], row['city'], row['listing_id'], row['listing_desc'], row['url'], product_code,
                                                                                       find_reviewID, user_alias, location, review_rating, rating_date]
                else:
                    logger.info("Missing information for url: {}".format(str(row['url'])))
                    self.reviews_details.loc[self.reviews_details.shape[0]] = [row['city_id'], row['city'],
                                                                               row['listing_id'], row['listing_desc'],
                                                                               row['url'], 'NA',
                                                                               'NA', 'NA', 'NA',
                                                                               'NA', 'NA']
            except Exception as er:
                logger.error("Error in one the elements: {}".format(er))

        self.reviews_details.to_csv('listing_reviews.csv', index=False, sep=',', header=True)


if __name__ == '__main__':
    pdd = PRODUCTSandREVIEWS()
    toCSV = pdd.get_review_details()
    import timeit
    from timit_codes import code2, imports2

    print("Time: %s" % timeit.timeit(setup=imports2,
                                       stmt=code2,
                                       number=1000000))
