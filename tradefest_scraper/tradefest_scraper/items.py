# -*- coding: utf-8 -*-
import scrapy
from scrapy import Item


class TradefestItem(Item):
    url = scrapy.Field()
    listed_name = scrapy.Field()
    website = scrapy.Field()
    detailed_name = scrapy.Field()
    venue = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    duration = scrapy.Field()
    hashtags = scrapy.Field()
    attendees = scrapy.Field()
    exhibitors = scrapy.Field()
    final_grade = scrapy.Field()  # client requirement - equivalent to a "rating"
    total_reviews = scrapy.Field()

    # media
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()
