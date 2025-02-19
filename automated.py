from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gmail import format

driver = webdriver.Chrome()

driver.get("https://sankeymatic.com/build/")
driver.maximize_window()
element = driver.find_element(By.ID, "load_example_job_search")
element.click()
text_area = driver.find_element(By.ID, "flows_in")

formatted = format()

if formatted:
    text_area.clear()
    text_area.send_keys(formatted)

slider = driver.find_element(By.ID, "node_h")
driver.execute_script("arguments[0].value = '37'; arguments[0].dispatchEvent(new Event('input'));", slider)

#checkbox = driver.find_element(By.ID,"meta_mentionsankeymatic")
#checkbox.click()
button = driver.find_element(By.ID,"save_as_png_2x")
button.click()

input("Press Enter to exit...")


