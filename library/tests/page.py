from locator import *
from element import *


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class UsernameElement(BasePageElement):
    locator = 'username'


class PasswordElement(BasePageElement):
    locator = 'password'


class MainPage(BasePage):
    def is_title_matches(self):
        return 'Main page' in self.driver.title

    def is_login_made(self):
        element = self.driver.find_element(*MainPageLocators.LOG_OUT_BUTTON)
        return element.is_displayed()

    def is_log_out_made(self):
        element = self.driver.find_element(*MainPageLocators.LOG_IN_BUTTON)
        return element.is_displayed()

    def click_log_in_button(self):
        element = self.driver.find_element(*MainPageLocators.LOG_IN_BUTTON)
        element.click()

    def click_log_out_button(self):
        element = self.driver.find_element(*MainPageLocators.LOG_OUT_BUTTON)
        element.click()


class LogInPage(BasePage):
    username_element = UsernameElement()
    password_element = PasswordElement()

    def is_title_matches(self):
        return 'Log In' in self.driver.title

    def is_login_not_made(self):
        element = self.driver.find_element(*LogInLocators.ERROR_MESSAGE)
        return element.text == 'Please enter a correct email and password. Note that both fields may be case-sensitive.'

    def click_submit_button(self):
        element = self.driver.find_element(*LogInLocators.SUBMIT_BUTTON)
        element.click()



