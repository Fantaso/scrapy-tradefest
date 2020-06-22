# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


# Removes
def remove_new_lines(value: str):
    return value.replace("\n", "")


def remove_hashtags(value):
    return value.replace("#", "")


def remove_first_2_chars(value: str):
    return value[2:]


def remove_empty_spaces(value):
    return value.replace(" ", "")


def remove_html_tags(value):
    return re.sub(r"<[^>]*>", " ", value).strip()


# Splits
def split_ref(value):
    return value.split("?ref")


def split_space(value):
    return value.split(" ")


def split_space_and_remove_empty_values(value):
    return [v for v in value.split(" ") if v]


def split_space_and_get_second(value):
    return split_space_and_remove_empty_values(value)[1]


def split_space_and_get_fourth(value):
    return split_space_and_remove_empty_values(value)[3]


def split_comma_and_get_penultimate(value):
    return value.split(",")[-2]


def split_open_parenthesis(value):
    return value.split("(")


def extract_data_between_parenthesis(value):
    start = value.find("(") + 1
    end = value.find(")")
    return value[start:end]


class TradefestEventItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    listed_name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    website = scrapy.Field(
        input_processor=MapCompose(str.strip, split_ref, ), output_processor=TakeFirst()
    )
    detailed_name = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    venue = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )
    date = scrapy.Field(
        input_processor=MapCompose(split_open_parenthesis, str.strip, ),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_new_lines),
        output_processor=TakeFirst(),
    )
    city = scrapy.Field(
        input_processor=MapCompose(split_comma_and_get_penultimate, str.strip, ),
        output_processor=TakeFirst(),
    )
    country = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_first_2_chars),
        output_processor=TakeFirst(),
    )
    duration = scrapy.Field(
        input_processor=MapCompose(extract_data_between_parenthesis),
        output_processor=TakeFirst(),
    )
    hashtags = scrapy.Field(
        input_processor=MapCompose(str.strip, remove_hashtags, remove_empty_spaces, ),
        output_processor=Join(separator=", "),
    )
    attendees = scrapy.Field(
        input_processor=MapCompose(
            str.strip, remove_html_tags, split_space_and_get_second, context=3
        ),
        output_processor=TakeFirst(),
    )
    exhibitors = scrapy.Field(
        input_processor=MapCompose(
            str.strip, remove_html_tags, split_space_and_get_fourth,
        ),
        output_processor=TakeFirst(),
    )
    # rating (client wanted the name "final_grade")
    final_grade = scrapy.Field(
        input_processor=MapCompose(str.strip), output_processor=TakeFirst()
    )

    total_reviews = scrapy.Field(
        input_processor=MapCompose(
            str.strip, extract_data_between_parenthesis, split_space,
        ),
        output_processor=TakeFirst(),
    )

# Implicit wait at 5 secs
# 2020-06-19 19:00:45 [scrapy.utils.log] INFO: Scrapy 2.1.0 started (bot: tradefest_scraper)
# 2020-06-19 19:11:38 [scrapy.core.engine] INFO: Spider closed (finished)
# 111 items
#  "Show more" links


# Implicit wait at 5 secs OLD
# 2020-06-19 11:50:15 [scrapy.utils.log] INFO: Scrapy 2.1.0 started (bot: tradefest_scraper)
# 2020-06-19 12:02:01 [scrapy.core.engine] INFO: Spider closed (finished)
# 111 items
# 0 "Show more" links

# Implicit wait at 3 secs
# 2020-06-19 18:22:00 [scrapy.utils.log] INFO: Scrapy 2.1.0 started (bot: tradefest_scraper)
# 2020-06-19 18:32:54 [scrapy.core.engine] INFO: Spider closed (finished)
# 111 items
# some "Show more" links

# Implicit wait at 4 secs
# 2020-06-19 18:47:45 [scrapy.utils.log] INFO: Scrapy 2.1.0 started (bot: tradefest_scraper)
# 2020-06-19 18:58:54 [scrapy.core.engine] INFO: Spider closed (finished)
# 111 items
# some "Show more" links


# Implicit wait at 2 secs
# 2020-06-19 13:21:15 [scrapy.utils.log] INFO: Scrapy 2.1.0 started(bot: tradefest_scraper)
# 2020-06-19 13:32:24 [scrapy.core.engine] INFO: Spider closed (finished)
# 111 items
# some "Show more" links
