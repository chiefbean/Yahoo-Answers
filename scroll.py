import selenium.webdriver
import time

def scrollPage(url, times_to_scroll, sleep_time):
    print('Loading questions page...')
    driver = selenium.webdriver.Chrome()
    driver.get(url)

    for i in range(1, times_to_scroll):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(sleep_time)

    return driver.page_source