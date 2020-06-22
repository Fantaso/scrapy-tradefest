# -*- coding: utf-8 -*-
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

from .items import TradefestItem


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


class TradefestLoader(ItemLoader):
    HASHTAG_DELIMITER = ", "
    default_item_class = TradefestItem
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    website_in = MapCompose(str.strip, split_ref)
    date_in = MapCompose(split_open_parenthesis, str.strip)
    description_in = MapCompose(str.strip, remove_new_lines)
    city_in = MapCompose(split_comma_and_get_penultimate, str.strip)
    country_in = MapCompose(str.strip, remove_first_2_chars)
    duration_in = MapCompose(extract_data_between_parenthesis)
    hashtags_in = MapCompose(str.strip, remove_hashtags, remove_empty_spaces)
    hashtags_out = Join(separator=HASHTAG_DELIMITER)
    attendees_in = MapCompose(str.strip, remove_html_tags, split_space_and_get_second)
    exhibitors_in = MapCompose(str.strip, remove_html_tags, split_space_and_get_fourth)
    total_reviews_in = MapCompose(str.strip, extract_data_between_parenthesis, split_space)
