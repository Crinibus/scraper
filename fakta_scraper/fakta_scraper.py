from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


# Setup headless browser
firefox_options = Options()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(options=firefox_options)
# driver = webdriver.Firefox()

URL = 'https://fakta.coop.dk/tilbudsavis/'

wait = WebDriverWait(driver, 20)

# Go to URL
driver.get(URL)

# Find "Tillad alle"-button on pop-up with cookies
accept_cookies_button = driver.find_element_by_id('acceptAllButton')
# Press "Tillad alle"-button on pop-up with cookies
accept_cookies_button.send_keys(Keys.RETURN)

# Wait until the page is loaded
wait.until(presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[2]/div/div[1]')))

print(driver.title)
print(driver.current_url)

# Find all the products on discount
products = driver.find_elements_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div')


# Discounts to look for
discount_words = ['lays', 'majskolber', 'kellogg']

# Find the products that match the ones to look for
found_discounts = []
for product in products:
    # print(f'{product.text}\n')
    for word in discount_words:
        if word in product.text.lower():
            found_discounts.append(product.text)


# Find the time period the discounts is valid for
time_periode = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[1]/div/p')
print(time_periode.text)


# Seperate products and prices
new_list = []
for product in found_discounts:
    indi_product = product.split('\n')
    for indi in indi_product:
        new_list.append(indi)


# Combine a product with it's price
num = 0
seperate_products = []
for product in new_list:
    num += 1
    if num%2 != 0:
        seperate_products.append(product)
    else:
        seperate_products[-1] += ' '+product

# Get rid of duplicates
check_products = []
for product in seperate_products:
    if not product in check_products:
        check_products.append(product)


# Print discounts
print('\nTilbud:')
for discount in check_products:
    print(f'{discount}\n')


# input("enter to quit")
driver.quit()
