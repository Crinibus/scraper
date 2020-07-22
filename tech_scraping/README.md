This program can scrape prices on products from Komplett.dk, Proshop.dk, Computersalg.dk and Elgiganten.dk

## First setup
Make sure you have the modules, run this in the terminal:

    pip install -r requirements.txt

## Scrape products
To scrape prices of products run this in the terminal:

    python scraping.py

## Adding products
Before scraping a new product, run:

     python add_product.py
and follow instructions.

Then add a line in this form in the last if-statement in scraping.py:

    {site}('{category}', '{link}')
e.g.

    Komplett('gpu', 'https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio')
OBS: make sure the category and product name has been created with add_product.py
