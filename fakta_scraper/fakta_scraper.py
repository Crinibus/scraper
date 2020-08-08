from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


# firefox_options = Options()
# firefox_options.add_argument('--headless')

# driver = webdriver.Firefox(
#     options=firefox_options
#     )

driver = webdriver.Firefox()

URL = 'https://fakta.coop.dk/tilbudsavis/'

wait = WebDriverWait(driver, 20)

driver.get(URL)

accept_cookies_button = driver.find_element_by_id('acceptAllButton')
accept_cookies_button.send_keys(Keys.RETURN)

wait.until(presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]')))

print(driver.title)
print(driver.current_url)


products = driver.find_elements_by_xpath(f'/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div')


word_tilbud = ['lays', 'majskolber', 'kellogg']


tilbud_søgning = []
for product in products:
    print(f'{product.text}\n')

    for word in word_tilbud:
        if word in product.text.lower():
            tilbud_søgning.append(product.text)


tidsperiode = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[1]/div/p')
print(tidsperiode.text)

print('\n\n\nTilbud:')
for tilbud in tilbud_søgning:
    print(f'{tilbud}\n')

input("enter to quit")
driver.quit()
