


## Usage
### Docker

**Building image from repository**
```bash
docker build -t fantaso/scrapy_tradefest .
```
**Pulling image from Dockerhub**
```bash
docker pull fantaso/scrapy_tradefest .
```

**Running image**

_```--rm``` just tells docker to erase the container automatically when scraping is finished_
```bash
docker run --rm -t fantaso/scrapy_tradefest
```

**Running image with binding volume to your local computer**

_Used to sync the "feeds" and "media", which is where the scraper outputs the data and images being scrapped_

**NOTE:** use an absolute path for the folder you want to bind to the container inner `data/` directory. e.g. /home/juan/data:/home/app/data
```bash
docker run --rm -v /path/to/directory/you/want/to/store/the/data:/home/app/data -t fantaso/scrapy_tradefest
```


---
#Install Selenium
###Firefox
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
sudo tar -xvf geckodriver-v0.26.0-linux64.tar.gz

sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver
```

<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

---
#Logs
###Chrome
**Chrome installation did NOT work**

```bash
wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/google-chrome
sudo ln -s /usr/local/share/chromedriver /usr/bin/google-chrome
```

### Instaling Chrome
```bash
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
sudo apt-get install google-chrome-stable
```