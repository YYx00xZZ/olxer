
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://zamundatv.com/stolichani-v-poveche-1x1/'

browser = webdriver.Chrome()  # or webdriver.Firefox(), or webdriver.PhantomJS() or etc.
wait = WebDriverWait(browser, 30)

browser.get('https://zamundatv.com/stolichani-v-poveche-1x1/')

# waiting for the frame to become present
frame = wait.until(EC.presence_of_element_located((By(XPATH('//*[@id="vplayer"]/div/div[1]/video')))))
browser.switch_to.frame(frame)


# get video url
url = browser.find_element_by_tag_name("video").get_attribute("src")
print(url)

browser.close()