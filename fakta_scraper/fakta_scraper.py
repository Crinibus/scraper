from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import sys


def setup_driver():
    '''Setup driver for headless Firefox browser.'''
    # Setup headless browser
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(options=firefox_options)
    # driver = webdriver.Firefox()
    return driver


def main(driver):

    URL = 'https://fakta.coop.dk/tilbudsavis/'
    URL_domain = URL.split('/')[2]

    # Go to URL
    driver.get(URL)

    # Find "Tillad alle"-button on pop-up with cookies
    accept_cookies_button = driver.find_element_by_id('acceptAllButton')
    # Press "Tillad alle"-button on pop-up with cookies
    accept_cookies_button.send_keys(Keys.RETURN)


    # # Wait until the page is loaded
    # wait = WebDriverWait(driver, 30)
    # wait.until(presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[25]/div/div[4]')))
    products, time_periode = find_products(URL_domain, driver)

    print(driver.title)
    print(driver.current_url)

    # # Find all the products on discount
    # products = driver.find_elements_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div')

    # # Find the time period the discounts is valid for
    # time_periode = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[1]/div/p')
    print(f'\n{time_periode.text}')


    # Get discounts to look for from arguments
    discount_words = []
    for x in range(1, len(sys.argv)):
        discount_words.append(sys.argv[x])

    # Discounts to look for
    #discount_words = ['lays', 'majskolber', 'kellogg']

    discounts = manipulate_product_list(products, discount_words)

    # input("enter to quit")
    driver.quit()

    print_discounts(discounts)


def find_products(URL_domain, driver):
    '''Find products and time periode depending on the url domain.'''
    wait = WebDriverWait(driver, 30)

    if URL_domain == 'fakta.coop.dk':
        # Wait until the page is loaded
        wait.until(presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[25]/div/div[4]')))
        # Find all the products on discount
        products = driver.find_elements_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div')
        # Find the time period the discounts is valid for
        time_periode = driver.find_element_by_xpath('/html/body/main/div[2]/div/div/div[3]/div/div/div[2]/div/div[1]/div/p')

    return products, time_periode


def manipulate_product_list(products, discount_words):
    '''Pass a list with products, return a list with only the products that match "discount_words"-list.'''
    # Find the products that match the ones to look for
    found_discounts = []
    for product in products:
        # print(f'{product.text}\n')
        for word in discount_words:
            if word in product.text.lower():
                found_discounts.append(product.text)

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
            seperate_products[-1] += f' {product}'

    # Get rid of duplicates
    discounts = []
    for product in seperate_products:
        if not product in discounts:
            discounts.append(product)

    return discounts


def print_discounts(discounts):
    '''Print discounts line by line.'''
    # Print discounts
    print('\nTilbud:')
    for discount in discounts:
        print(f'{discount}\n')


if __name__ == '__main__':
    driver = setup_driver()
    if len(sys.argv) > 1:
        main(driver)
    else:
        print('Please add your seach terms as arguments')
