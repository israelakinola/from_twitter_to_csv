import sys
sys.path.append('..')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import app
import os 


# browser= webdriver.Chrome()
# browser.get("http://www.google.com")
# print(browser.title)
class TestApp(unittest.TestCase):
    """ This class run the tests for the App Module """
    broswer = webdriver.Chrome()

    def test_validate_qty(self):
        """ This method runs the test  for the validate_qty function in the App Module """
        self.assertEqual(app.validate_qty("100"), 100)
        self.assertEqual(app.validate_qty("-1"), 10)
        self.assertEqual(app.validate_qty("d"), 10)

    def test_validate_keyword(self):
        """ This method runs the test for the validate_keyword function in the App Module """
        self.assertFalse(app.validate_keyword(''))
        self.assertTrue(app.validate_keyword('donald'))


    def test_index_view(self):
        """ This method test the homepage view """
         # Navigate to url
        self.broswer.get("http://localhost:5000/")
        # Find if form element is present
        fetch_form_ele = self.broswer.find_element(By.TAG_NAME, "form")
        self.assertTrue(fetch_form_ele)
        # Find input element by the name keyword and check if its present
        keyword_ele = self.broswer.find_element(By.NAME, 'keyword')
        self.assertTrue(keyword_ele)
        # Find input element by the name qty and check if its present
        qty_ele = self.broswer.find_element(By.NAME, 'qty')
        self.assertTrue(qty_ele)
        # Find fetch button button web element and check if its present
        fetch_btn_ele = self.broswer.find_element(By.ID, 'fetch_btn')
        self.assertTrue(fetch_btn_ele)
    
   

    def test_fetch_form(self):
        """ This method test the fetch form, check if the csv file is in the downloads folder and its downloadable on the browser """
        # Navigate to url
        self.broswer.get("http://localhost:5000/")
       # Wait until browser element is clickable, find input element by the name keyword and send keys to it 
        keys_value = 'hello'
        download_file_path = f'{os.path.normpath(os.getcwd() + os.sep + os.pardir)}/downloads'
        WebDriverWait(self.broswer, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='keyword']"))).send_keys(keys_value)
        # Find fetch button button web element and click it
        self.broswer.find_element(By.ID, 'fetch_btn').click()
        # Find button element by the name download and check if its present
        btn_ele = self.broswer.find_elements(By.ID, 'download_btn')
        self.assertTrue(btn_ele)
        # Check if there is a csv file with the keyword name in the downloads directory
        csv_file = open(f"{download_file_path}/{keys_value}.csv")
        self.assertTrue(csv_file)
 


    @classmethod
    def tearDownClass(cls):
        cls.broswer.quit()
        

if __name__ == "__main__":
    unittest.main()