# **Twitter-Sentimental-Analysis**

## Project Description

IMDB provides a list of celebrities born on the current date. Below is the link: http://m.imdb.com/feature/bornondate

Get the list of these celebrities from this webpage using web scraping (the ones that are displayed i.e top 10). You have to extract the below information:

* Name of the celebrity
* Celebrity Image
* Profession
* Best Work

Once you have this list, run a sentiment analysis on twitter for each celebrity and finally the output should be in the below format

* Name of the celebrity:
* Celebrity Image:
* Profession:
* Best Work:
* Overall Sentiment on Twitter: Positive, Negative or Neutral

## Tools Used/Requirements

1. [Python >= 3.6.1 (64-bit)](https://www.python.org/downloads/)

2. [Beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - Python library for pulling data out of HTML and XML files.

3. [Tweepy](http://www.tweepy.org/) - OpenSource Twitter API for Python.

4. [Selenium](https://pypi.python.org/pypi/selenium) - The webdriver kit emulates a web-browser and executes JavaScripts to load the dynamic content.

5. [Textblob](https://textblob.readthedocs.io/en/dev/) - Python library using [nltk](https://www.nltk.org/) to find polarity of text/tweet.

6. [lxml](http://lxml.de/) - A fast html and xml parser for beautifulsoup4

7. [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/) - Web Browser to perform web scraping.

8. [Gecko Driver](https://github.com/mozilla/geckodriver/releases) - Driver for Selenium to invoke Firefox.

9. [API Keys for Twitter](https://developer.twitter.com/) has to be put in ```/data/twitter_api_keys.json``` (Refer [sample_twitter_api_keys.json](data/sample_twitter_api_keys.json) for format.)

## Running the application

1. Make sure you have all the requirements installed. See requirements.txt or run

   *```pip install -r requirements.txt --upgrade```*

2. Make sure you have the latest version of Mozilla Firefox installed and latest version of geckodriver in utils folder.

**Run the application using:**
  
  **```python App.py```**

## Author
Maneesh D - maneeshd77@gmail.com
