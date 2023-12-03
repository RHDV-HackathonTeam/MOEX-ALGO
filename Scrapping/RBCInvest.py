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

            return self.quotes

        except Exception as e:
            return e

        # finally:
        #     self.close_parser()

    # tags div MuiGrid-root MuiGrid-item MuiGrid-grid-xs-auto quote-style-h9c4jn
    # textdiv div MuiGrid-root MuiGrid-container MuiGrid-item MuiGrid-grid-xs-12 quote-style-obit8q
    def parse_news(self, url: str):
        try:
            self.driver.get(url=url)

            wait = WebDriverWait(self.driver, 10)
            textdiv = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 '//div[@class="MuiGrid-root quote-style-1birln0"]')))

            all_paragraphs = textdiv.find_elements(By.TAG_NAME, 'p')

            for p in all_paragraphs:
                print(p.text)

        except Exception as e:
            return e


if __name__ == "__main__":
    p = RBCParser()
    # p.parse_hrefs()
    p.parse_news(url="https://quote.ru/news/article/656999869a79478b7bb3ca6c")
