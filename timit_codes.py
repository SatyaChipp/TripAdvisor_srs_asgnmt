imports1 = """
import warnings
from dateutil.parser import parse
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import re
import logging
import sys
"""

code1 = """
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
                self.reviews_details.loc[self.reviews_details.shape[0]] = [row['city_id'], row['city'],
                                                                           row['listing_id'], row['listing_desc'],
                                                                           row['url'], 'NA',
                                                                           'NA', 'NA', 'NA',
                                                                           'NA', 'NA']
        except Exception as er:
            logger.error("Error in one the elements: {}".format(er))

    self.reviews_details.to_csv('listing_reviews.csv', index=False, sep=',', header=True)
"""

code2 = """
def __init__(self):
    self.ref_base_url = "https://www.tripadvisor.com"
    self.details_dataframe = pd.DataFrame(columns=["scan_date", "city_id", "city", "listing_id", "listing_desc",
                                                   "url", "review_count", "by", "price_from", "strike_thru_price", "is_special_offer"])

def get_body(self, url):
    body_ = urlopen(str(url))
    return body_.read()

def get_top20(self, url__):
    try:
        top_20 = []
        logger.info("Base URL: {}".format(url__))
        soup = BeautifulSoup(self.get_body(url__), 'html.parser')
        data = soup.findAll('div', attrs={'class': 'geo_name'})
        for div in data:
            links = div.findAll('a')
            for a in links:
                top_20.append([self.ref_base_url + a['href'], a['href'].split('-')[1], a.text.replace(' Attractions', '')])
    except Exception as er:
        logger.error("Error url {}: {}".format(url__, er))
        raise er
    return top_20

def capture_all_listings(self, cities_html, csv_filename=None):
    try:
        for city in cities_html: #for each city in top 20 cities
            body_ = urlopen(self.ref_base_url + '/Attraction_Products-' + city[1] + '-' + city[0].split('-')[-1]).read()
            logger.info("Getting from URL: {}".format(self.ref_base_url + '/Attraction_Products-' + city[1] + '-' + city[0].split('-')[-1]))
            soup = BeautifulSoup(body_, 'html.parser')
            data = soup.findAll('div', attrs={'class': 'listing_details'})
            city_id__ = city[1]
            city_name__ = city[2]
            for link in data:
                self.___get_attraction_details_page(link, city_name__, city_id__)
            data_pages = soup.findAll('div', attrs={'class': 'pageNumbers'})

            for a in data_pages:
                body_ = urlopen(self.ref_base_url + a.find('a')['href']).read()
                soup = BeautifulSoup(body_, 'html.parser')
                data = soup.findAll('div', attrs={'class': 'listing_details'})
                for link in data:
                    self.___get_attraction_details_page(link, city_name__, city_id__)
    except Exception as er:
        logger.error('Error while capturing listings: {}'.format(er))
    if not csv_filename:
        csv_filename = 'listing_tours.csv'
    self.details_dataframe.to_csv(csv_filename, index=False, sep=',', header=True)
    return self.details_dataframe

def ___get_attraction_details_page(self, link, city_name__, city_id__):
    try:
        listing_by__ = link.find('div', attrs={'class': 'listing_duration'})
        listing_by = listing_by__.find('a').text if listing_by__ else 'NA'
        listing = link.find('div', attrs={'class': 'clickable_listing'})
        listing_desc__ = listing.find('div', attrs={'class': 'listing_description'}).find_all('span')
        listing_desc = listing_desc__[0].text if len(listing_desc__) != 0 else 'NA'
        if len(listing_desc__) != 0:
            listing_url__ = self.ref_base_url + (
            [item for item in re.findall(r"'(.*?)'", str(listing_desc__[1]), re.DOTALL)
             if len(listing_desc__)!=0 and item.startswith('/AttractionProductDetail')][0])
        else:
            listing_url__ = self.ref_base_url #default url - redirect to homepage
        listing_id__ = listing_url__.split('-')[2] if listing_url__ != self.ref_base_url else 'NA'
        review__ = [span.text for span in listing.find_all('span', attrs={'class': 'more'})]
        review_count = int(review__[0].split(' ')[0].replace(',', '')) if len(review__) != 0 else 0
        pdt_price_info__ = link.find('div', attrs={'class': 'product_price_info'}) \
            .find('div', attrs={'class': 'price_test'})
        product_info_from__ = float(pdt_price_info__.find('div', attrs={'class': 'from'}) \
                                    .find('span').text.replace('$', '').replace('*', '').replace(',',
                                                                                                 '')) if pdt_price_info__.find(
            'div', attrs={'class': 'from'}) else 0
        product_info_strikethru__ = pdt_price_info__.find('div', attrs={'class': 'savings'})
        pdt_info_strikethru = float(
            product_info_strikethru__.find('span').text.replace('$', '').replace('*', '').replace(',',
                                                                                                  '')) if product_info_strikethru__ is not None else 0
        spl_offer__ = link.find('div', attrs={'class': 'product_price_info'}).find('div',
                                                                                   attrs={'class': 'tag_container'})
        spl_offer = spl_offer__.span.text if spl_offer__ else ' '
        self.details_dataframe.loc[self.details_dataframe.shape[0]] = [datetime.now().date(), city_id__, city_name__, listing_id__,
                                                                       listing_desc, listing_url__, review_count,
                                                                       listing_by,
                                                                       product_info_from__, pdt_info_strikethru,
                                                                       spl_offer]
        self.details_dataframe['listing_desc'] = self.details_dataframe['listing_desc'].apply(
            lambda x: x.replace('\\n', '<br>'))
    except Exception as er:
        logger.error("Error while getting information: {}".format(er))
"""

imports2 = """
import warnings
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pprint import pprint
import pandas as pd
from datetime import datetime
import re
import logging
import sys
"""