import sys
sys.path.append('..')
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import app

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
        self.broswer.get("http://localhost:5000/")
        ### Find if form element is present
        fetch_form_ele = self.broswer.find_elements(By.TAG_NAME, "form")
        self.assertTrue(fetch_form_ele)
        ### Find input keyword element is present
        keyword_ele = self.broswer.find_elements(By.NAME, 'keyword')
        self.assertTrue(keyword_ele)
        qty_ele = self.broswer.find_elements(By.NAME, 'qty')
        self.assertTrue(qty_ele)
        fetch_btn_ele = self.broswer.find_elements(By.CLASS_NAME, 'fetch')
        self.assertTrue(fetch_btn_ele)
 


    @classmethod
    def tearDownClass(cls):
        cls.broswer.quit()
        

if __name__ == "__main__":
    unittest.main()