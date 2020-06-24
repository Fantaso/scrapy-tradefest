# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy import Selector
from scrapy.http import Response
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from ..loaders import TradefestLoader


def text_on_page(resp: Response, css_selector):
    if resp.css(css_selector).get():
        return True


def click_to_reveal_it(url, css_selector) -> webdriver.Firefox.page_source:
    """
    Uses selenium to render request in a browser
    locate a link, move mouse pointer to the link
    and clicks it.
    """

    BROWSER_ZOOM_SETTING = "layout.css.devPixelsPerPx"
    ZOOM_FACTOR = "0.4"
    TIME_SECS = 5

    options = Options()
    options.add_argument("-headless")
    profile = FirefoxProfile()
    profile.set_preference(BROWSER_ZOOM_SETTING, ZOOM_FACTOR)
    browser = webdriver.Firefox(options=options, firefox_profile=profile)
    browser.maximize_window()
    browser.implicitly_wait(TIME_SECS)
    browser.get(url)
    try:
        # TODO: add wait implementation (research: staleness_of)
        link = browser.find_element_by_css_selector(css_selector)
        webdriver.ActionChains(browser).move_to_element(link).click(link).perform()
        return browser.page_source

    except NoSuchElementException:
        return browser.page_source
    finally:
        browser.quit()


def render_javascript_page(url, wait_secs) -> webdriver.Firefox.page_source:
    """
    Uses selenium to render the javascript in the browser.
    """
    options = Options()
    options.add_argument("-headless")
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    time.sleep(wait_secs)
    page_source = browser.page_source
    browser.quit()
    return page_source


class TradefestSpider(scrapy.Spider):
    name = "tradefest"
    allowed_domains = ["tradefest.io"]

    def start_requests(self):
        """
        The start urls were set manually since there client only required
        these specific events that were in 6 paginated pages.
        For future use: use LinkExtractor with CrawlSpider to make it
        more dynamic.
        """
        start_urls = [
            scrapy.Request(
                url=f"https://tradefest.io/en/tag/furniture?page={page_num}",
                callback=self.parse_events,
            )
            for page_num in range(1, 7)
        ]
        return start_urls

    def parse_events(self, response):
        """
        Going through the lists of furniture events in a paginated manner
        and sending the request to parse the details of the event.
        """
        response_body = render_javascript_page(response.url, wait_secs=2)
        selector = Selector(text=response_body)
        events = selector.css("#results .ng-star-inserted .result")
        for event in events:
            url = event.css("a::attr(href)").get()
            image_url = event.css('.event-logo .ng-star-inserted::attr(src)').get()
            ctx = {
                "listed_name": event.css("strong::text").get(),
                "total_reviews": "".join(event.css("span.smaller-g::text").getall()),
                'image_urls': image_url
            }
            yield scrapy.Request(
                url=response.urljoin(url), callback=self.parse_event, cb_kwargs=ctx,
            )

    def parse_event(self, response, listed_name, total_reviews, image_urls):
        loader = TradefestLoader(response=response)

        show_more_text = ".accent-link-g span"
        if text_on_page(response, show_more_text):
            self.logger.info(f'Event description hidden: {response.url}, {listed_name}')
            response_body = click_to_reveal_it(response.url, show_more_text)
            selector = Selector(text=response_body)
            loader = TradefestLoader(selector=selector)

        loader.add_value("listed_name", listed_name)
        loader.add_value("total_reviews", total_reviews)
        loader.add_value("url", response.url)
        loader.add_css("country", ".header-top .accent-link-g::text")
        loader.add_css("description", "p.description.ng-star-inserted::text")
        loader.add_css("detailed_name", "h1.title::text")
        loader.add_css("final_grade", ".big-number::text")
        loader.add_css("hashtags", "a.tag-link::text")
        loader.add_css("venue", "p.ng-star-inserted :last-child::text")
        loader.add_css("website", ".description+ .accent-link-g::attr(href)")

        # "how_many" and "where_when_how_long":
        #   the html structure is not constant, so the cleaning process
        #   is handle by the ItemLoader'a input & output processor.
        how_many = "".join(response.css(".tagline+ .ng-star-inserted").getall())
        loader.add_value("attendees", how_many)
        loader.add_value("exhibitors", how_many)

        where_when_how_long = "".join(response.css("div+span::text").getall())
        loader.add_value("city", where_when_how_long)
        loader.add_value("date", where_when_how_long)
        loader.add_value("duration", where_when_how_long)

        # images
        loader.add_value('image_urls', image_urls)
        loader.add_value('image_name', listed_name)

        yield loader.load_item()
