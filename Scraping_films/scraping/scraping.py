import scraping.constants as const
from scraping.select_by_style import element_has_css_value
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraping(webdriver.Chrome):
    def __init__(self, executable_path=r"C:\Users\yffan\Documents\VScodeProject\Python\Selenium-project\chromedriver.exe"):
        self.teardown = False
        super(Scraping, self).__init__(executable_path)
        self.implicitly_wait(15)
        self.maximize_window()

    def land_page(self):
        self.get(const.BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def select_year(self):
        return self.find_elements(By.CLASS_NAME, 'year-link')

    def get_title(self, table:WebElement):
        Titles = []
        titles = table.find_element(By.TAG_NAME, "thead").find_elements(By.TAG_NAME, "th")
        for title in titles:
            Titles.append(title.get_attribute('innerHTML').strip())
        return Titles

    def get_body(self, table:WebElement):
        body = []
        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            arr = []
            for td in tds:
                arr.append(td.get_attribute('innerHTML').strip())
            body.append(arr)
        return body

    def get_table(self):
        try:
            element = WebDriverWait(self, 10).until(
                element_has_css_value((By.ID, "loading"), "display", "none")
            )
            assert(element)
            print('success')
            table = self.find_element(By.CLASS_NAME, "table")
            title = self.get_title(table)
            body = self.get_body(table)
            with open(os.getcwd()+'/films.csv', 'a', newline='', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(title)
                writer.writerows(body)
                f.close()

        except Exception as e:
            self.quit()

    def get_film_data(self):
        years = self.select_year()
        f = open(os.getcwd()+"/films.csv", "w")
        f.truncate()
        f.close()
        for year in years:
            year.click()
            self.get_table()

