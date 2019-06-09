"""
@author: Gautam K
"""

from sqlite3 import connect, Error
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from traceback import print_exc
from os import path
from datetime import datetime


DIR_PATH = path.dirname(path.abspath(__file__))


class ImdbScraper:
    """
    Scrape IMDb for Celebrity Data.
    """
    def __init__(self, url="http://m.imdb.com/feature/bornondate"):
        """
        Constructor
        :param url: URL for the IMDb page.
        """
        self.__url = url
        self.__celeb_list = list()

    def __dump_into_db(self):
        """
        Dump the data into db.
        :return: None
        """
        try:
            with connect("celebData.db") as con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS CELEB_DATA;")
                cur.execute("CREATE TABLE CELEB_DATA("
                            "NAME TEXT, "
                            "PHOTO TEXT, "
                            "PROFESSION TEXT, "
                            "BEST_WORK TEXT, "
                            "SENTIMENT TEXT DEFAULT '');")
                con.commit()

                for celeb in self.__celeb_list:
                    cur.execute("INSERT INTO CELEB_DATA(NAME,"
                                "PHOTO,"
                                "PROFESSION,"
                                "BEST_WORK) "
                                "VALUES(?, ?, ?, ?);",
                                (celeb.get("Name"),
                                 celeb.get("Photo"),
                                 celeb.get("Profession"),
                                 celeb.get("Best Work"),))
                con.commit()
        except Error as err:
            print("!!! SQLITE3 ERROR: %s !!!" % err)
            exit(1)

    def scrape_imdb(self):
        """
        Scrapes the IMDB born_on_date page to collect the top 10
        celebrity data.After collecting the data stores it in a sqlite3 db.
        :return: None
        """
        try:
            # Initialize the chrome driver.
            driver = Chrome()

            # Run the dynamic content on the webpage.
            driver.get(self.__url)
            driver.implicitly_wait(30)

            # Get the loaded webpage source.
            page_source = driver.page_source

            # Close the driver.
            driver.close()

            # Create a beautifulsoup crawler and load the page data.
            try:
                crawler = BeautifulSoup(page_source, "lxml")
            except Exception:
                print("[INFO] lxml parser not found. Using html parser...")
                crawler = BeautifulSoup(page_source, "html.parser")

            # Get the required details from the page
            born_on_date = datetime.now().strftime("%B %d")
            print("Getting Data for celebrities born on %s.." % born_on_date)

            # Get the celeb details from HTML and put it in the celeb list
            count = 0
            for div in crawler.find_all("div", class_="lister-item mode-detail"):
                if count >= 10:
                    break

                celeb = dict()

                # Parse  celeb name
                name = div.find("div", "lister-item-content").find("h3", "lister-item-header").find("a").text.strip()

                # parse celeb pic
                img = div.find("div", "lister-item-image").find("a").img["src"].strip()

                # get profession and best_work
                profession, best_work = div.find("div", "lister-item-content").find("p", "text-muted text-small").text.split("|")
                profession = profession.strip()
                best_work = best_work.strip()

                # Form a dict for the celeb and push it into celeb list.
                celeb["Name"] = name
                celeb["Photo"] = img
                celeb["Profession"] = profession
                celeb["Best Work"] = best_work
                self.__celeb_list.append(celeb)
                count += 1

            # Dump the data into sqlite3 db
            self.__dump_into_db()

            print("Data Successfully Scraped and dumped into db...")
        except Exception as exp:
            print_exc()
            print("Exception: %s" % exp)
            exit(1)
