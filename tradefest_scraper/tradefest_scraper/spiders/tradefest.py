# -*- coding: utf-8 -*-

import scrapy
from scrapy import Selector
from scrapy.http import Response
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

from ..items import TradefestEventItem

Response
def is_present_on_page(resp: Response, css_selector):
    if resp.css(css_selector).get():
        return True


def is_text_hidden(resp: Response, css_selector):
    if is_present_on_page(resp, css_selector):
        return True


def is_venue_formatted_as_link(resp: Response, css_selector):
    if is_present_on_page(resp, css_selector):
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
        events = response.css("#results .ng-star-inserted .result").getall()
        for event in events:
            selector = Selector(text=event)
            url = selector.css("a::attr(href)").get()
            ctx = {
                "listed_name": selector.css("strong::text").get(),
                "total_reviews": "".join(selector.css("span.smaller-g::text").getall()),
            }
            yield scrapy.Request(
                url=response.urljoin(url), callback=self.parse_event, cb_kwargs=ctx,
            )

    def parse_event(self, response, listed_name, total_reviews):
        loader = ItemLoader(item=TradefestEventItem(), response=response)

        SHOW_MORE_LINK = ".accent-link-g span"
        if is_text_hidden(response, SHOW_MORE_LINK):
            response_body = click_to_reveal_it(response.url, SHOW_MORE_LINK)
            selector = Selector(text=response_body)
            loader = ItemLoader(item=TradefestEventItem(), selector=selector)

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

        how_many = "".join(response.css(".tagline+ .ng-star-inserted").getall())
        loader.add_value("attendees", how_many)
        loader.add_value("exhibitors", how_many)

        where_when_how_long = "".join(response.css("div+span::text").getall())
        loader.add_value("city", where_when_how_long)
        loader.add_value("date", where_when_how_long)
        loader.add_value("duration", where_when_how_long)

        yield loader.load_item()
