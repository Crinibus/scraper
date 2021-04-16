# Table of contents
- [Intro](#intro)
- [Contributing](#contributing)
- [First setup](#first-setup)
- [Start from scratch](#start-scratch)
- [Scrape products](#scrape-products)
- [Add products](#add-products)
    - [Websites to scrape from](#websites-to-scrape-from)
- [User settings](#user-settings)
- [Clean up data](#clean-up-data)
- [Visualize data](#visualize-data)
    - [Command examples](#command-examples)

<br/>


## Intro <a name="intro"></a>
With this program you can easily scrape and track prices on product at multiple [websites](#websites-to-scrape-from). <br/>
This program can also visualize price over time of the products being tracked. That can be helpful if you want to buy a product in the future and wants to know if a discount might be around the corner.

<br/>


## Contributing <a name="contributing"></a>
Feel free to fork the project and create a pull request with new features or refactoring of the code. Also feel free to make issues with problems or suggestions to new features.

<br/>


## UPDATE TO HOW DATA IS STORED IN V1.1
In version v1.1, I have changed how data is stored in "records.json". "dates" under each product have been changed to "datapoints" and now a list containing dicts with "date" and "price" keys. <br/>
If you want to update your data to be compatible with version v1.1, then open a interactive python session where this repository is located and run the following commands:
```
>>> from scraper.format import Format
>>> Format.format_old_records_to_new()
```

<br/>

## First setup <a name="first-setup"></a>
Clone this repository and move into the repository:
```
git clone https://github.com/Crinibus/scraper.git
```
```
cd scraper
```

Then make sure you have the modules, run this in the terminal:
```
pip3 install -r requirements.txt
```

<br/>


## Start from scratch <a name="start-scratch"></a>
If you want to start from scratch with no data in the records.json and products.csv files, then just run the following command:
```
python3 main.py --hard-reset
```

Then just add products like described [here](#add-products).

<br/>

If you just want to reset your data for each product, just delete all data-points inside each product, then run this command:
```
python3 main.py --reset
```
This deletes all the data inside each product, such as id, url and all datapoints.

<br/>


## Scrape products <a name="scrape-products"></a>
To scrape prices of products run this in the terminal:
```
python3 main.py -s
```
To scrape with threads run the same command but with the ```--threads``` argument:
```
python3 main.py -s --threads
```

<br/>


## Add products <a name="add-products"></a>
To add a single product, use the following command, where you replace ````<category>``` and ```<url>``` with your category and url:
```
python3 main.py -a -c <category> -u <url>
```

e.g.
```
python3 main.py -a -c vr -u https://www.komplett.dk/product/1168594/gaming/spiludstyr/vr/vr-briller/oculus-quest-2-vr-briller
```

This adds the category (if new) and the product to the records.json file, and adds a line at the end of the products.csv file so the script can scrape price of the new product.

<br/>

To add multiple products at once, just add specify another category and url with ```-c <category>``` and ```-u <url>```. E.g. with the following command I add two products:
```
python3 main.py -a -c <category> -u <url> -c <category2> -u <url2>
``` 

**OBS**: The category can only be one word, so add a underscore instead of a space if needed.<br/>
**OBS**: The url must have the "https://" part.<br/>
**OBS**: If an error occures when adding a product, then the error might happen because the url has a "&" in it, when this happens then just put quotation marks around the url. This should solve the problem. If this doesn't solve the problem then summit a issue.<br/>

<br/>


### Websites to scrape from <a name="websites-to-scrape-from"></a>
This scraper can (so far) scrape prices on products from:
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

<br/>


## User settings <a name="user-settings"></a>
User settings can be added and changed in the file settings.ini.

Right now there is only one category of user settings, which is "ChangeName".  Under this category you can change how the script changes product names, so similar products will be placed in the same product in records.json file.

When adding a new setting under the category "ChangeName" in settings.ini, there must be a line with ```key<n>``` and a line with ```value<n>```, where ```<n>``` is the "link" between keywords and valuewords. E.g. ```value3``` is the value to ```key3```.

In ```key<n>``` you set the keywords (seperated by a comma) that the product name must have for to be changed to what ```value<n>``` is equal to. Example if the user settings is the following:

```
[ChangeName]
key1 = asus,3080,rog,strix,oc
value1 = asus geforce rtx 3080 rog strix oc
```

The script checks if a product name has all of the words in ```key1```, it gets changed to what ```value1``` is.

<br/>


## Clean up data <a name="clean-up-data"></a>
If you want to clean up your data, meaning you want to remove unnecessary datapoints (datapoints that have the same price as the datapoint before and after it), then run the following command:
```
python3 main.py --clean-data
```
<br/>


## Visualize data <a name="visualize-data"></a>
To visualize your data, just run main.py with the ```-v``` or ```--visualize``` argument and then specify which products you want to be visualized. These are your options for how you want to visualize your products:

- ```-va``` or ```--visualize-all``` to visualize all your products
- ```-vc [<category> [<category> ...]]``` or ```--visualize-category [<category> [<category> ...]]``` to visualize all products in one or more categories
- ```-id [<id> [<id> ...]]``` or ```--visualize-id [<id> [<id> ...]]``` to visualize one or more products with the specified id(s)
- ```-vn [<name> [<name> ...]]``` or ```--visualize-name [<name> ...]]``` to visualize one or more products with the specified name(s)


### Command examples <a name="command-examples"></a>
**Show graphs for all products**

To show graphs for all products, run the following command:
```
python3 main.py -v -va
```

**Show graph(s) for specific products**

To show a graph for only one product, run the following command where ```<id>``` is the id of the product you want a graph for:
```
python3 main.py -v -id <id>
```

For multiple products, just add another id, like so:
```
python3 main.py -v -id <id> <id>
```


**Show graphs for products in one or more categories**

To show graphs for all products in one category, run the following command where ```<category>``` is the category you want graph from:
```
python3 main.py -v -vc <category>
```

For multiple categories, just add another category, like so:
```
python3 main.py -v -vc <category> <category>
```


**Show graps for products with a specific name**

To show graphs for product(s) with a specific name, run the following command where ```<name>``` is the name of the product(s) you want graphs for:
```
python3 main.py -v -vn <name>
```

For multiple products with different names, just add another name, like so:
```
python3 main.py -v -vn <name> <name2>
```

If the name of a product has multiple words in it, then just add quotation marks around the name.
