### Interview – Tripadvisor Attraction Reviews


*Abstract*

We are interested in tracking TripAdvisor’s attraction counts and their review count over time. For this exercise, you should focus on Top 20 cities in South America, and only on "Tours and Tickets." (See links below)


*Details*

**Part 1**: Capture all the individual "Tours and Tickets" listings in the Top 20 cities

+ Go through and save all HTML pages
+ Parse and capture all listings (note: there are 30 listings per page.  In the case of Buenos Aires, there are ~309 listings).
+ Record scan_date | city_id | city | listing_id | listing_desc | url | review_count | by | price_from | strike_thru_price | is_special_offer


Top cities link in South America:

https://www.tripadvisor.com/Attractions-g13-Activities-South_America.html

![Things to Do](https://s3.amazonaws.com/srs-interview/tripattraction/things_to_do.jpg)


Sample "Tours and Attractions" link:

https://www.tripadvisor.com/Attraction_Products-g312741-Buenos_Aires_Capital_Federal_District.html

![Tours and Tickets](https://s3.amazonaws.com/srs-interview/tripattraction/tours_and_tickets.jpg)


**Part 2**: Use the captured listings URL and capture the reviews with their review timestamps

+ Use the captured listings’ URL as a queue and visit the individual listing pages
+ Capture all the reviews available on the site for the listing. i.e. page through the reviews
+ Capture the city_id | city | listing_id | listing_desc | url | product_code |  review_id | user_alias |  user_location | review_rating | review_timestamp

https://www.tripadvisor.com/AttractionProductDetail-g294317-d11483317-Machu_Picchu_Private_Guided_Tour_from_Aguas_Calientes-Sacred_Valley_Cusco_Region.html

 
*Review section*

There are cases where the review count from Part 1 does not match the number of reviews available in Part 2, because TripAdvisor is including reviews from Viator in Part 1.  See the "Read 45 more reviews on Viator" link.  Capturing Viator related reviews is outside the scope of this exercise.


Product code is located at the bottom of the right sidebar.


