**This program can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk, Elgiganten.dk and AvXperten.dk**

# Table of contents
- [First setup](#first-setup)
- [Start from scratch](#start-scratch)
- [Scrape products](#scrape-products)
- [Adding products](#adding-products)
    - [Optional arguments](#optional-arguments)

<br/>

## First setup <a name="first-setup"></a>
Make sure you have the modules, run this in the terminal:

    pip install -r requirements.txt

## Start from scratch <a name="start-scratch"></a>
If you want to start from scratch with no data in the records.json file, then just delete all the content in records.json apart from two curly brackets:

    {}
Then just add products like described [here](#add-products)

## Scrape products <a name="scrape-products"></a>
To scrape prices of products run this in the terminal:

    python3 scraping.py

## Add products <a name="add-products"></a>
Before scraping a new product, run a similar line to this:

    python3 add_product.py <category> <url>
e.g.

    python3 add_product.py gpu https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio
**OBS: the category can only be one word, so add a underscore instead of a space if needed.**

This adds the category (if new) and the product to the records.json file, and adds a line at the end of the scraping.py file so the script can scrape price of the new product.

### Optional arguments <a name="optional-arguments"></a>
There is some optional arguments you can use when running add_product.py, these are:

-     --komplett

-     --proshop

-     --computersalg

-     --elgiganten

When using one or more of "domain" arguments, only the chosen domains gets added to records.json under the product name. 
