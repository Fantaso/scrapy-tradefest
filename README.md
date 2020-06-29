<!-- logo -->
<a href="https://www.fantaso.de">
<img src="/readme/fantaso.png" align="right" />
</a>

<!-- header -->
<h1 style="text-align: left; margin-top:0px;">
  Convention & Expos Tradefest Scraper
</h1>

> Events scraper app with Scrapy and Selenium.


<!-- build -->
<!-- [![Build Status][travis-image]][travis-link] -->


Project consists to allow a user to scrape the "furniture" section of
tradefest.io (platform to find conventions & expos events) using Scrapy as a
framework to extract, transform and store data.

<br><br>

---
## Index:
- #### Usage: with Docker
    1. Getting and Running the docker image
    2. What data are we scraping and where is stored

- #### Information:
- #### Maintainer

<br><br>


---
## Usage: with Docker ![container][docker]
#### 1. Getting and Running the docker image

image is hosted in docker hub registry freely available [fantaso/scrapy_tradefest](https://hub.docker.com/repository/docker/fantaso/scrapy_tradefest)

Pulling image from Dockerhub
    
```sh
docker pull fantaso/scrapy_tradefest
```

or directly run it

```sh
mkdir -p output/logs \
&& docker run --rm -v "$(pwd)"/output:/home/app/output -t fantaso/scrapy_tradefest
```

- Here `-v "$(pwd)"/output:/home/app/output` we are just binding a volume to synchronize 
a folder `output/` in our computer and mapping it to a folder inside the docker
container `/home/app/output` where the data scraped will be stored. 
- Because of permissions and docker problems binding to sync the folder in the docker 
with our local machine. **we need to create first the folder with `mkdir -p output/logs`
to avoid problems running the docker**.

**NOTE:** This is what we get when we want to run a container binding a volume
to our local machine using a non root user to run the container.

---
#### 2.  What data are we scraping and where is stored

We want to store the data scraped in our machine. So, we are binding a folder inside
the docker container (`output/`) to a folder inside our local machine (PC were docker container runs).
    
Output folder contains:
    
- `feeds` contains all the scraped data in different formats (csv, xml, json)
- `logs`  contains the scraping log files
- `media` contains the images we wanted to scraped as well as automatically generated
          thumbnails from the images scraped in different sizes (small, medium).
          
**NOTE:** all data files generated for logs and feeds are named or formatted
with the current time when the docker image is run. `e.g: "2020-06-28 23:47:18.csv"```

Fields to be scraped from each event or expo:
- `url`: url of the detailed event
- `listed_name`: name of the event in the paginated list
- `detailed_name`: name of the event in the detailed event page
- `date`: date of the event
- `city`: city where the event is taken place
- `country`: country where the event is taken place
- `venue`: location or place where the event is taken place
- `duration`: time duration of the event
- `final_grade`: rating of the event (client naming requirement!)
- `total_reviews`: quantity of reviewers (related to the "final_grade")
- `attendees`: quantity of people that attended the event
- `exhibitors`: quantity of exhibitors that were part of the event
- `hashtags`: tags of the event
- `website`: official website of the event. 
- `description`: descriptions of the event
- `image_urls`: url for the logo (image) of the of the event


<br>

## Information:
| Technology Stack |  |  |
| :- | :-: | :- |
| Python                    | ![back-end][python]                   | Back-End |
| Scrapy                    | ![scraper framework][scrapy]          | Scraper Framework |
| Selenium                  | ![browser automation][selenium]       | Browser Automation |
| Docker                    | ![container][docker]                  | Container |

<br><br>


## Maintainer
Get in touch -–> [fantaso][fantaso]



<!-- Links -->
<!-- Profiles -->
[github-profile]: https://github.com/fantaso/
[linkedin-profile]: https://www.linkedin.com/
[fantaso]: https://github.com/fantaso/
<!-- Extra -->

<!-- Repos -->
[github-repo]: https://github.com/Fantaso/tradefest_scraper

<!-- Builds -->
[travis-link]: https://travis-ci.org/
[travis-image]: https://travis-ci.org/

<!-- images -->
[python]: readme/python.png
[scrapy]: readme/scrapy.png
[selenium]: readme/selenium.png
[docker]: readme/docker.png
