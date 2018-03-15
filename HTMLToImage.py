from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_binary_data_from_url(driver, url):
    driver.get(url)
    return driver.get_screenshot_as_png()
    
def save_html_into_image(driver, url, filename):
    driver.get(url)
    driver.fullscreen_window()
    screenshot = driver.save_screenshot(filename)
 

def open_driver():
    DRIVER = 'chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--disable-overlay-scrollbar")
    driver = webdriver.Chrome(chrome_options=chrome_options)    
    return driver

def quit_driver(driver):
    driver.quit()
    
