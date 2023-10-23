from selenium.webdriver.common.by import By


class MainPageLocators:
    LOG_IN_BUTTON = (By.CSS_SELECTOR, 'a[href="/login/"]')
    LOG_OUT_BUTTON = (By.CSS_SELECTOR, 'a[href="/logout/"]')


class LogInLocators:
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'form button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.errorlist.nonfield li')