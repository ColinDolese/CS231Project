from selenium import webdriver

def get_binary_data_from_url(driver, url):
    driver.get(url)
    return driver.get_screenshot_as_png()
    
def save_html_into_image(driver, url, filename):
    driver.get(url)
    driver.fullscreen_window()
    screenshot = driver.save_screenshot(filename)
 

def open_driver():
    DRIVER = 'chromedriver'
    driver = webdriver.Chrome()
##    driver = webdriver.maximize_window()
##    driver.set_window_size(1024,768)
    return driver

def quit_driver(driver):
    driver.quit()
    
