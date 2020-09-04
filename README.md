**The tech scraper can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk, Elgiganten.dk, AvXperten.dk and Av-Cables.dk**<br/>
**The Fakta scraper can scrape discounts from this week discounts.**

# Table of contents
- [First setup](#first-setup)
- [Tech scraper](#tech-scraper)
    - [Scrape products](#scrape-products)
    - [Start from scratch](#start-scratch)
    - [Adding products](#adding-products)
        - [Optional arguments](#optional-arguments)
- [Fakta scraper](#fakta-scraper)
    - [Scrape discounts](#scrape-discounts)

<br/>

## First setup <a name="first-setup"></a>
First make sure you have the modules, run this in the terminal:

    pip install -r requirements.txt

<br/>

# Tech scraper <a name="tech-scraper"></a>
The tech scraper can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk, Elgiganten.dk, AvXperten.dk and Av-Cables.dk

## Scrape products <a name="scrape-products"></a>
To scrape prices of products run this in the terminal:

    python3 scraping.py

## Start from scratch <a name="start-scratch"></a>
If you want to start from scratch with no data in the records.json file, then just delete all the content in records.json apart from two curly brackets:

    {}
Then just add products like described [here](#add-products)

## Add products <a name="add-products"></a>
Before scraping a new product, run a similar line to this:

    python3 add_product.py <category> <url>
e.g.

    python3 add_product.py gpu https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio
**OBS: The category can only be one word, so add a underscore instead of a space if needed.**<br/>
**OBS: The url must have the "www." part.**

<br/>

This adds the category (if new) and the product to the records.json file, and adds a line at the end of the scraping.py file so the script can scrape price of the new product.

### Optional arguments <a name="optional-arguments"></a>
There is some optional arguments you can use when running add_product.py, these are:

-     --komplett

-     --proshop

-     --computersalg

-     --elgiganten

-     --avxperten

-     --avcables

When using one or more of "domain" arguments, only the chosen domains gets added to records.json under the product name. 

<br/>

# Fakta scraper <a name="fakta-scraper"></a>
The Fakta scraper can scrape discounts from this week discounts. <br/>
**OBS: Fakta scraper can not run in Linux as it uses the Firefox webdriver which is a .exe file.**

## Scrape discounts <a name="scrape-discounts"></a>
For now you can only search for keywords and get the discounts that match the keywords.
To scrape for discounts about for example Kellogg products, you only have to add the keyword "Kellogg" as a argument when running the fakta_scraper.py script:

    python3 fakta_scraper.py kellogg

You can search for multiple keyword by just adding them as arguments, as such:

    python fakta_scraper.py <keyword_1> <keyword_2> <keyword_3>

The discounts is printed in the terminal.
