from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time

from bs4 import BeautifulSoup
import requests

class StoreTracker:
    def __init__(self):
        self.GEM_STORE_URL = "https://thatshaman.com/tools/gemstore/"
        self.WIKI_URL = "https://wiki.guildwars2.com/wiki/"

        self.TODAY_STR = datetime.today().date().strftime("%b %d %Y")
        self.TODAY_YEAR = str(datetime.today().year)
        self.TODAY = datetime.strptime(self.TODAY_STR, "%b %d %Y").date()

    def get_gem_store(self, wishlist):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        # Accessing Gem Store
        driver = webdriver.Chrome()
        driver.get(self.GEM_STORE_URL)
        driver.maximize_window()
        time.sleep(1)

        # Checking current  Gem Store items
        schedule = driver.find_elements(By.CLASS_NAME, value="gemstoreEntry")
        shop_results = self.find_items(wishlist, schedule)
        driver.quit()
        return shop_results

    def check_price(self, name):
        keep_searching = True
        statuette = ""
        gems = ""
        voucher = ""
        answer = f"**Price:** "

        query = name.replace(" ", "_")
        gem_text = "Gem_Store"

        # BeautifulSoup
        response = requests.get(f"{self.WIKI_URL}{query}").text
        soup = BeautifulSoup(response, "html.parser")

        # Extracting price
        elements = soup.select("[style*='text-align:right']")
        for element in elements:
            if element.find(name="a", title="Black Lion Statuette") is not None:
                statuette = f"{element.get_text().strip()} Black Lion Statuettes | "
                answer += statuette
            elif element.find(name="a", title="Black Lion Outfit Voucher") is not None:
                voucher = f"{element.get_text().strip()} Black Lion Outfit Voucher | "
                answer += voucher
            else:
                while keep_searching:
                    gems = f"{element.get_text().strip()} Gems."
                    answer += gems
                    keep_searching = False
        return answer


    def find_items(self, user_wishlist, data):
        coming_soon_dates = []
        coming_soon_names = []
        in_stock_end_dates = []
        in_stock_names = []
        search_results = []
        return_text = ""

        # Extracting HTML and checking shop availability dates
        for item in data:
            # Extracting item names
            raw = item.text.replace(f"\n", " ").split()
            raw_item = raw[6:len(raw) - 1]
            item_name = " ".join(raw_item)

            # Extracting start and end availability of items
            start = f"{raw[1]} {raw[2]} {self.TODAY_YEAR}"
            next_year_start = f"{raw[1]} {raw[2]}"
            start_date = datetime.strptime(start, "%b %d %Y").date()
            end = f"{raw[4]} {raw[5]} {self.TODAY_YEAR}"
            end_date = datetime.strptime(end, "%b %d %Y").date()

            if user_wishlist[0] == "All":
                if start_date <= self.TODAY <= end_date:
                    search_results.append(item_name)

            else:
                # Updating positive matches
                if end_date >= self.TODAY >= start_date and item_name in user_wishlist:
                    in_stock_end_dates.append(end)
                    in_stock_names.append(item_name)
                    search_results.append(f"**{item_name}:** Currently in the Gem Store.\n{self.check_price(item_name)}\n")

                # Updating matches that are coming soon
                elif start_date > self.TODAY and item_name in user_wishlist:
                    coming_soon_dates.append(start)
                    coming_soon_names.append(item_name)
                    search_results.append(f"**{item_name}:** Will arrive {start}.\n")
                # Updating matches that are coming next year
                elif item_name in user_wishlist:
                    search_results.append(f"**{item_name}:** Will be available next year on {next_year_start}.\n")

        for i in search_results:
            return_text += f"{i}\n"
        return return_text
