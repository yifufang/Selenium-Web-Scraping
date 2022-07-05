from pydoc import classname
import scraping.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import csv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraping(webdriver.Chrome):
    def __init__(self, driver_path = r"C:\Users\yffan\Documents\VScodeProject\Python\Selenium-project\chromedriver.exe", teardown = False):
        self.teardown = teardown
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        super(Scraping, self).__init__(self.driver_path, options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def land_page(self):
        self.get(const.BASE_URL)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
    
    def get_page(self, pagination:WebElement, page_num):
        pagination = self.find_element(By.CLASS_NAME, "pagination")
        page = pagination.find_elements(By.TAG_NAME, "a")[page_num]
        page.click()
    def get_title(self):
        table = self.find_elements(By.CLASS_NAME,"table")
        titles = table[0].find_elements(By.TAG_NAME, "th")  
        
        row=[]
        for title in titles:
            row.append(title.get_attribute('innerHTML').strip())
        return row
        
    def get_team_info(self):
        Table = []
        table = self.find_elements(By.CLASS_NAME,"table")
        teams = table[0].find_elements(By.CLASS_NAME, "team")

        for team in teams:
            td = team.find_elements(By.TAG_NAME, "td")
            row = []
            for i in td:
                row.append(i.get_attribute('innerHTML').strip())
            Table.append(row)
        return Table
    
    def get_all_tables(self):
        pagination = self.find_element(By.CLASS_NAME, "pagination")
        pages = pagination.find_elements(By.TAG_NAME, "a")

        with open(os.getcwd()+'/table.csv', 'w', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(self.get_title())
            for i in range(len(pages)):
                self.get_page(pagination, i)
                writer.writerows(self.get_team_info())
        
        
            
            

        
        