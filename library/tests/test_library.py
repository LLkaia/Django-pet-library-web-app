import time
import unittest
from selenium import webdriver
import page


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()
        self.driver.get('http://127.0.0.1:8000/')

    def test_log_in_valid(self):
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches())
        time.sleep(2)
        main_page.click_log_in_button()

        log_in_page = page.LogInPage(self.driver)
        self.assertTrue(log_in_page.is_title_matches())
        log_in_page.username_element = 'popova@gmail.com'
        log_in_page.password_element = 'adminadmin'
        time.sleep(2)
        log_in_page.click_submit_button()

        time.sleep(2)
        self.assertTrue(main_page.is_login_made())

    def test_log_out(self):
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches())
        time.sleep(2)
        main_page.click_log_in_button()

        log_in_page = page.LogInPage(self.driver)
        self.assertTrue(log_in_page.is_title_matches())
        log_in_page.username_element = 'popova@gmail.com'
        log_in_page.password_element = 'adminadmin'
        time.sleep(2)
        log_in_page.click_submit_button()

        time.sleep(2)
        self.assertTrue(main_page.is_login_made())
        main_page.click_log_out_button()
        self.assertTrue(main_page.is_log_out_made())
        time.sleep(2)

    def test_log_in_invalid(self):
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches())
        time.sleep(2)
        main_page.click_log_in_button()

        log_in_page = page.LogInPage(self.driver)
        self.assertTrue(log_in_page.is_title_matches())
        log_in_page.username_element = 'popova@gmail.com'
        log_in_page.password_element = 'invalidpass'
        time.sleep(2)
        log_in_page.click_submit_button()

        time.sleep(2)
        self.assertTrue(log_in_page.is_login_not_made())

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()