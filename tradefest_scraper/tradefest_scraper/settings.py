# -*- coding: utf-8 -*-
import os
import pathlib
from datetime import datetime

# BASE PATH
BASE = '/home/carlos/github/toronto_tradefest_scraper'
# BASE = '/home/app/output'

BOT_NAME = "tradefest_scraper"

SPIDER_MODULES = ["tradefest_scraper.spiders"]
NEWSPIDER_MODULE = "tradefest_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'tradefest_scraper.middlewares.TradefestScraperSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'tradefest_scraper.middlewares.TradefestScraperDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }


#######################
###  AUTO THROTTLE  ###
#######################
# DOWNLOAD_DELAY = 0.25
# CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 64
# - The dynamic delay calculated will never:
#       go less than DOWNLOAD_DELAY
#       or more than AUTOTHROTTLE_MAX_DELAY
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 15
AUTOTHROTTLE_TARGET_CONCURRENCY = 16
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

######################
###  HTTP CACHING  ###
######################
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


################################################
### GENERAL SETTINGS FOR  LOGGING AND FEEDS  ###
################################################
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FILENAME_PATTERN = datetime.now().strftime(DATETIME_FORMAT)

LOG_PATH = f'{BASE}/logs/{FILENAME_PATTERN}.txt'
FEEDS_CSV_PATH = f'{BASE}/feeds/csv/{FILENAME_PATTERN}.csv'
FEEDS_JSON_PATH = f'{BASE}/feeds/json/{FILENAME_PATTERN}.json'
FEEDS_XML_PATH = f'{BASE}/feeds/xml/{FILENAME_PATTERN}.xml'
IMAGES_PATH = f'{BASE}/media/'

CSV_FIELDS_TO_PERSIST = [
    # fields in the CSV file are printed in the order specified in the list
    'url',
    'listed_name',
    'detailed_name',
    'date',
    'city',
    'country',
    'venue',
    'duration',
    'final_grade',
    'total_reviews',
    'attendees',
    'exhibitors',
    'hashtags',
    'website',
    'description',
    'image_urls',
]

###  LOGGING  ###
LOG_ENABLED = True  # this True only and it will display in stdout
LOG_TO_FILE = True  # if True: writes to logfile. if False: writes to stdout
if LOG_TO_FILE:
    LOG_FILE = LOG_PATH
    LOG_ENCODING = 'utf-8'
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
    LOG_DATEFORMAT = DATETIME_FORMAT
    # If True, all stdout & stderr of your process will be redirected to the log.
    # example: if you print('hello') it will appear in the scrapy log.
    LOG_STDOUT = True  # default
    # If True, the logs will just contain the root path.
    # If False, it displays the component responsible for the log output.
    # LOG_SHORT_NAMES = False

###  FEEDS  ###
FEEDS = {
    # CSV
    pathlib.Path(FEEDS_CSV_PATH): {
        'format': 'csv',
        'encoding': 'utf-8',
        'store_empty': True,
        'fields': CSV_FIELDS_TO_PERSIST,
    },
    # JSON
    FEEDS_JSON_PATH: {
        'format': 'json',
        'encoding': 'utf-8',
        'store_empty': False,
        'fields': CSV_FIELDS_TO_PERSIST,
        'indent': 4,
    },
    # XML
    FEEDS_XML_PATH: {
        'format': 'xml',
        'encoding': 'latin1',
        'fields': CSV_FIELDS_TO_PERSIST,
        'indent': 8,
    },
}

FEED_STORAGES_BASE = {
    '': 'scrapy.extensions.feedexport.FileFeedStorage',
    'file': 'scrapy.extensions.feedexport.FileFeedStorage',
    'stdout': 'scrapy.extensions.feedexport.StdoutFeedStorage',
    's3': 'scrapy.extensions.feedexport.S3FeedStorage',
    'ftp': 'scrapy.extensions.feedexport.FTPFeedStorage',
}

FEED_EXPORTERS_BASE = {
    'json': 'scrapy.exporters.JsonItemExporter',
    'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
    'jl': 'scrapy.exporters.JsonLinesItemExporter',
    'csv': 'scrapy.exporters.CsvItemExporter',
    'xml': 'scrapy.exporters.XmlItemExporter',
    'marshal': 'scrapy.exporters.MarshalItemExporter',
    'pickle': 'scrapy.exporters.PickleItemExporter',
}

########################
###  Media & Images  ###
########################
DOWNLOAD_TIMEOUT = 30
# if implementing more pipelines for specific spiders
#   consider moving config values into the spider itself
IMAGES_STORE = IMAGES_PATH
ITEM_PIPELINES = {
    'tradefest_scraper.pipelines.TradefestImagesPipeline': 2,
}

###  SKIP IMAGES  ###
# filter out images smaller than the minimum here stated
# IMAGES_MIN_HEIGHT = 110
# IMAGES_MIN_WIDTH = 110

# IMAGES_EXPIRES = 5  # days
MEDIA_ALLOW_REDIRECTS = True

###  THUMBNAILS  ###
IMAGES_THUMBS = {
    'small': (50, 50),
    'medium': (68, 68),
}
