from os import environ
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# hack to override sqlite database filename
# see: https://help.morph.io/t/using-python-3-with-morph-scraperwiki-fork/148
environ['SCRAPERWIKI_DATABASE_NAME'] = 'sqlite:///data.sqlite'
import scraperwiki


# path to chromedriver
chromedriver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(
    executable_path=chromedriver_path,
    chrome_options=chrome_options)

base_url = 'https://www.iso.org/obp/ui/'
table_css = 'table[class="grs-grid"]'
officially_assigned_code_elements_css = 'td[class="grs-status1"]'

url = base_url + '#iso:pub:PUB500001:en'
browser.get(url)

while True:
    try:
        table = browser.find_element_by_css_selector(table_css)
        break
    except NoSuchElementException:
        print('Waiting for page to load ...')
        time.sleep(1)

print('Page has loaded!')

table_cells = table.find_elements_by_css_selector(
    officially_assigned_code_elements_css)

for cell in table_cells:
    row = {
        'code': cell.text,
        'name': cell.get_attribute('title'),
        'url': cell.find_element_by_tag_name('a').get_attribute('href'),
    }
    scraperwiki.sqlite.save(['code'], row, 'data')