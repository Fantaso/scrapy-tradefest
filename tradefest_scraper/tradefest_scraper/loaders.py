# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Identity

from .items import TradefestItem
from .utils.cleaner import *


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

    # media
    image_urls_in = Identity()
    image_urls_out = MapCompose()
    image_name_in = MapCompose(safe_filename)
