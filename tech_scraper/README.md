# Table of contents
- [First setup](#first-setup)
- [Start from scratch](#start-scratch)
- [Scrape products](#scrape-products)
- [Adding products](#adding-products)
    - [Links to scrape from](#links-to-scrape-from)
    - [Optional arguments](#optional-arguments)
- [User settings](#user-settings)
- [Visualize data](#visualize-data)
    - [Command examples](#command-examples)
    - [Available flags](#available-flags)

<br/>

## First setup <a name="first-setup"></a>
Make sure you have the modules, run this in the terminal:
```
pip install -r requirements.txt
```

## Start from scratch <a name="start-scratch"></a>
If you want to start from scratch with no data in the records.json file, then just delete all the content in records.json apart from two curly brackets:
```
{}
```

Then delete the lines under the last if-statement in scraper.py. 

Then just add products like described [here](#add-products).

## Scrape products <a name="scrape-products"></a>
To scrape prices of products run this in the terminal:
```
python3 scrape_links.py
```

## Add products <a name="add-products"></a>
Before scraping a new product, run a similar line to this:
```
python3 add_product.py <category> <url>
```
e.g.
```
python3 add_product.py gpu https://www.komplett.dk/product/1135037/hardware/pc-komponenter/grafikkort/msi-geforce-rtx-2080-super-gaming-x-trio
```

This adds the category (if new) and the product to the records.json file, and adds a line at the end of the scraper.py file so the script can scrape price of the new product.

**OBS**: The category can only be one word, so add a underscore instead of a space if needed.<br/>
**OBS**: The url must have the "https://www." part.<br/>
**OBS**: When using Amazon links, delete everything after and including this "ref=sr".<br/>
For example the link: https://www.amazon.com/NVIDIA-GEFORCE-RTX-2080-Founders/dp/B07HWMDDMK/ref=sr_1_2?dchild=1&qid=1601488833&s=computers-intl-ship&sr=1-2<br/>
Should be: https://www.amazon.com/NVIDIA-GEFORCE-RTX-2080-Founders/dp/B07HWMDDMK/<br/>
**OBS**: When using eBay links, delete everything after and including this "?_trkparms="<br/>
For example the link: https://www.ebay.com/itm/Samsung-Galaxy-Note-20-Ultra-256GB-12GB-RAM-SM-N986B-DS-FACTORY-UNLOCKED-6-9/193625604205?_trkparms=aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D225074%26meid%3Dd6c93f1458884e65bcc434e38f6f303c%26pid%3D100970%26rk%3D8%26rkt%3D8%26mehot%3Dpp%26sd%3D402319206529%26itm%3D193625604205%26pmt%3D0%26noa%3D1%26pg%3D2380057%26brand%3DSamsung&_trksid=p2380057.c100970.m5481&_trkparms=pageci%3A6ffa204c-042b-11eb-baa4-3a1cc2bb9aea%7Cparentrq%3Ae60676341740a4d6b1579293fff1b710%7Ciid%3A1<br/>
Should be: https://www.ebay.com/itm/Samsung-Galaxy-Note-20-Ultra-256GB-12GB-RAM-SM-N986B-DS-FACTORY-UNLOCKED-6-9/193625604205

### Links to scrape from <a name="links-to-scrape-from"></a>
The tech scraper can scrape prices on products from:
- [Komplett.dk](https://www.komplett.dk/)
- [Proshop.dk](https://www.proshop.dk/)
- [Computersalg.dk](https://www.computersalg.dk/)
- [Elgiganten.dk](https://www.elgiganten.dk/)
- [AvXperten.dk](https://www.avxperten.dk/)
- [Av-Cables.dk](https://www.av-cables.dk/)
- [Amazon.com](https://www.amazon.com/)
- [eBay.com](https://www.ebay.com/)
- [Power.dk](https://www.power.dk/)
- [Expert.dk](https://www.expert.dk/)
- [MM-Vision.dk](https://www.mm-vision.dk/)
- [Coolshop.dk](https://www.coolshop.dk/)
- [Sharkgaming.dk](https://www.sharkgaming.dk/)

### Optional arguments <a name="optional-arguments"></a>
There is some optional arguments you can use when running add_product.py, these are:

-     --komplett

-     --proshop

-     --computersalg

-     --elgiganten

-     --avxperten

-     --avcables

-     --amazon

-     --ebay

-     --power

-     --expert

-     --mmvision

-     --coolshop

-     --sharkgaming

When using one or more of "domain" arguments, only the chosen domains gets added to records.json under the product name. 


## User settings <a name="user-settings"></a>
User settings can be added and changed in the file settings.ini.

Right now there is only one category of user settings, which is "ChangeName".  Under this category you can change how the script changes product names, so similar products will be placed in the same product in records.json file.

When adding a new setting under the category "ChangeName" in settings.ini, there must be a line with ```keywords<n>``` and a line with ```valuewords<n>```, where ```<n>``` is the "link" between keywords and valuewords. E.g. ```valuewords3``` is the value to ```keywords3```.

In ```keywords<n>``` you set the keywords (seperated by a comma) that the product name must have for to be changed to what ```valuewords<n>``` is equal to. Example if the user settings is the following:

```
[ChangeName]
keywords1 = asus,3080,rog,strix,oc
valuewords1 = asus geforce rtx 3080 rog strix oc
```

The script checks if a product name has all of the words in ```keywords1```, it gets changed to what ```valuewords1``` is.

## Visualize data <a name="visualize-data"></a>
To visualize your data run the "visualize_data.py" script with some arguments.

See all available flags [here](#available-flags).

By using the ```--all``` flag you will get graphs for all products in records.json.

By using the ```--partnum``` or ```-p``` and specify a partnumber you will only get the graph for the specified partnumber. You can specify multiple partnumbers just by adding multiple ```--partnum``` or ```-p``` flags.

By using the ```--category``` or ```-c``` you will get graphs for all the product in the specified category. You can specify multiple categories just by adding multiple ```--category``` or ```-c``` flags.


### Command examples <a name="command-examples"></a>
**Show graphs for all products**

To show graphs for all products, run the following command:
```
python3 visualize_data.py --all
```

**Show graph(s) for specific products**

To show a graph for only one product, run the following command where ```<partnumber>``` is the partnumber of the product you want a graph for:
```
python3 visualize_data.py --partnum <partnumber>
```

For multiple products, just add another flag, like so:
```
python3 visualize_data.py --partnum <partnumber> --partnum <partnumber>
```

You can also just use the short flag name, like so:
```
python3 visualize_data.py -p <partnumber>
```

**Show graphs for products in one or more categories**

To show graphs for all products in one category, run the following command where ```<category>``` is the category you want graph from:
```
python3 visualize_data.py --category <category>
```

For multiple categories, just add another flag, like so:
```
python3 visualize_data.py --category <category> --category <category> 
```

You can also just use the short flag name, like so:
```
python3 visualize_data.py -c <category>
```


### Available flags <a name="available-flags"></a>
When running visualize_data.py you must use atleast one flag, the available flags are:

-     --all

-     --partnum <partnum>

-     -p <partnum>

-     --category <category>

-     -c <category>
