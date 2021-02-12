# car_scrapper

**ScrApp**

Simple scrapper using Python + Django + Selenium

The app has two main backend functions that can be call through the URL:

- BASEURL + 'scrap/'

- BASEURL + 'cars_list/?key=value&key2=value

First of two start the scrapper and search for Dodge, Ferrari, Lamborghini and Nissan used cars (with a given ZIP code).
Data is saved in database. No repeated cars admitted. 

Second endpoint returns a list of cars which can be filtered using the next parameters in the url:
- key 'brand': let you choose among the mentioned car makers.
- key 'model': ley you search only the mentioned models. Brand is not necessary, unless a model name is repeated from one manufacturer to another.
- keys 'start_year' and 'end_year' that let the user search for cars in a range.
- keys 'low_price' and 'high_price' that let the user choose a prince range to search for.
