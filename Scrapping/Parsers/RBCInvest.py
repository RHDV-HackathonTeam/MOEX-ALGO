from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Scrapping.Parsers.WebParser import Parser
from selenium.common.exceptions import StaleElementReferenceException
import asyncio


class RBCParser(Parser):
    def __init__(self):
        super().__init__(resource="rbc")
        self.quotes = list()
        self.break_status = True

    async def parse_hrefs(self, target_news_url):
        try:
            self.driver.get(url="https://quote.ru/category/all")
            while self.break_status:
                wait = WebDriverWait(self.driver, 10)
                quotes_hrefs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone quote-style-d24tsf"]')))
                hrefs = list(map(lambda x: x.get_attribute('href'), quotes_hrefs))

                for href in hrefs:
                    self.quotes.append(href)
                    if href == target_news_url:
                        self.break_status = False
                        break

                if not self.break_status:
                    break

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            return self.quotes

        except Exception as e:
            return e

# MuiGrid-root MuiGrid-item MuiGrid-grid-xs-auto quote-style-h9c4jn
    async def parse_news(self, url: str):
        try:
            self.driver.get(url=url)

            wait = WebDriverWait(self.driver, 10)
            textdiv = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 '//div[@class="MuiGrid-root quote-style-1birln0"]')))

            await asyncio.sleep(0.2)
            ticker_tag_div = self.driver.find_elements(By.XPATH,
                                                       '//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-auto quote-style-h9c4jn"]')

            all_paragraphs = textdiv.find_elements(By.TAG_NAME, 'p')

            news_text = [p.text for p in all_paragraphs]
            text_as_string = '\n'.join(news_text)

            tags = list()

            for tag in ticker_tag_div:
                try:
                    tag_text = tag.text
                    tags.append(tag_text)
                    print("Tag: ", tag_text)
                except StaleElementReferenceException:
                    print("Stale Element Exception occurred.")

            return [text_as_string, tags]

        except Exception as e:
            return e
