from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scrapping.WebParser import Parser
import time


class RBCParser(Parser):
    def __init__(self):
        Parser.__init__(self, resource="rbc")
        self.quotes = list()
        self.break_status = False

    def parse_hrefs(self):
        try:
            self.driver.get(url="https://quote.ru/category/all")
            i = 0
            while i < 2:
                wait = WebDriverWait(self.driver, 10)
                quotes_hrefs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone quote-style-d24tsf"]')))
                hrefs = list(map(lambda x: x.get_attribute('href'), quotes_hrefs))

                for href in hrefs:
                    self.quotes.append(href)

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                i += 1
                print(i)

            print(self.quotes)
            return self.quotes

        except Exception as e:
            return e

        # finally:
        #     self.close_parser()


    # tags div MuiGrid-root MuiGrid-item MuiGrid-grid-xs-auto quote-style-h9c4jn
    def parse_news(self, url: str):
        try:
            pass
        except Exception as e:
            return e


if __name__ == "__main__":
    p = RBCParser()
    p.parse_hrefs()

