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
products = driver.find_elements_by_xpath(f'/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div')

# Discounts to look for
discount_words = ['lays', 'majskolber', 'kellogg']

found_discounts = []

# Find the products that match the ones to look for
for product in products:
    # print(f'{product.text}\n')
    for word in discount_words:
        if word in product.text.lower():
            found_discounts.append(product.text)

# Find the time period the discounts is valid for
time_periode = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[1]/div/p')
print(time_periode.text)





#num = 0
#new_list = []
#for product in found_discounts:
#    new_word = ''
#    for letter in product:
#        if letter == 'n':
#            if last_letter == '\\':
#                if num%2 == 0:
#                    letter = ' '
#        if letter == '\\':
#            if num%2 == 0:
#                letter = ''
#            num += 1
#        last_letter = letter
#        new_word += letter
#    new_list.append(new_word)


new_list = []
for product in found_discounts:
    indi_product = product.split('\n')
    for indi in indi_product:
        new_list.append(indi)

num = 0
new_list_1 = []
for product in new_list:
    if num%2 != 0:
        new_list_1.append(product)
    if num != 1:
        if num%2 == 0:
            num_1 = int(num/2)
            print(new_list_1[num_1])
            new_list_1[num_1] += ' '+product
    num += 1





# Print found discounts
print('\n\n\nTilbud:')
for discount in found_discounts:
    print(f'{discount}\n')

print(found_discounts)

print(new_list)

# input("enter to quit")
driver.quit()
