from scraper.domains import (
    AmazonHandler,
    AvCablesHandler,
    AvXpertenHandler,
    ComputerSalgHandler,
    CoolshopHandler,
    EbayHandler,
    ElgigantenHandler,
    ExpertHandler,
    KomplettHandler,
    MMVisionHandler,
    NeweggHandler,
    PowerHandler,
    ProshopHandler,
    SharkGamingHandler,
)
from scraper.format import Info


komplett_handler = KomplettHandler("https://www.komplett.dk/product/1168438")
komplett_soup = komplett_handler._request_product_data()
komplett_handler._get_common_data(komplett_soup)

proshop_handler = ProshopHandler("https://www.proshop.dk/Hovedtelefonerheadset/Sony-WH-1000XM4/2883832")
proshop_soup = proshop_handler._request_product_data()
proshop_handler._get_common_data(proshop_soup)

computersalg_handler = ComputerSalgHandler(
    "https://www.computersalg.dk/i/6647865/sony-wh-1000xm4-hovedtelefoner-med-mik-fuld-st%c3%b8rrelse-bluetooth-tr%c3%a5dl%c3%b8s-kabling-nfc-aktiv-st%c3%b8jfjerning-3-5-mm-jackstik-sort"
)
computersalg_soup = computersalg_handler._request_product_data()
computersalg_handler._get_common_data(computersalg_soup)

elgiganten_handler = ElgigantenHandler(
    "https://www.elgiganten.dk/product/tv-lyd-smart-home/horetelefoner-tilbehor/horetelefoner/sony-tradlose-around-ear-horetelefoner-wh-1000xm4-sort/200693"
)
elgiganten_soup = elgiganten_handler._request_product_data()
elgiganten_handler._get_common_data(elgiganten_soup)

avxperten_handler = AvXpertenHandler(
    "https://www.avxperten.dk/noise-cancelling-head-set/sony-wh-1000xm4-bluetooth-hovedtelefoner-anc-sort.asp"
)
avxperten_soup = avxperten_handler._request_product_data()
avxperten_handler._get_common_data(avxperten_soup)

avcables_handler = AvCablesHandler(
    "https://www.av-cables.dk/bluetooth-hoeretelefoner/sony-wh-1000xm4-over-ear-bluetooth-headset-sort.html"
)
avcables_soup = avcables_handler._request_product_data()
avcables_handler._get_common_data(avcables_soup)

amazon_handler = AmazonHandler(
    "https://www.amazon.com/Sony-WH-1000XM4-Wireless-Canceling-Headphones/dp/B08HDKHSSN/ref=sr_1_3?crid=2QKY9WQGCV809&keywords=sony+xm4&qid=1660593858&sprefix=sony+xm%2Caps%2C171&sr=8-3"
)
amazon_soup = amazon_handler._request_product_data()
amazon_handler._get_common_data(amazon_soup)

# ebay_handler_one = EbayHandler("FIND URL WITH 'itm' IN URL")
# ebay_soup_one = ebay_handler_one._request_product_data()
# ebay_handler_one._get_common_data(ebay_soup_one)

# ebay_handler_two = EbayHandler("FIND URL WITHOUT 'itm' IN URL")
# ebay_soup_two = ebay_handler_two._request_product_data()
# ebay_handler_two._get_common_data(ebay_soup_two)

expert_handler = ExpertHandler(
    "https://www.expert.dk/hoejtalere-og-lyd/hovedtelefoner/traadloese-hovedtelefoner/sony-wh-1000xm4-traadloese-stoejdaempende-hovedtelefoner-sort/p-1106907/"
)
expert_soup = expert_handler._request_product_data()
expert_handler._get_common_data(expert_soup)

power_handler = PowerHandler(
    "https://www.power.dk/tv-og-lyd/hovedtelefoner/traadloese-hovedtelefoner/sony-wh-1000xm4-traadloese-stoejdaempende-hovedtelefoner-blaa/p-1185731/"
)
power_soup = power_handler._request_product_data()
power_handler._get_common_data(power_soup)

mmvision_handler = MMVisionHandler("https://www.mm-vision.dk/asus-zenbook-duo-14-ux482eg-pure9x-baerbar")
mmvision_soup = mmvision_handler._request_product_data()
mmvision_handler._get_common_data(mmvision_soup)

coolshop_handler = CoolshopHandler("https://www.coolshop.dk/produkt/pokemon-brilliant-diamond/238G6U/")
coolshop_soup = coolshop_handler._request_product_data()
coolshop_handler._get_common_data(coolshop_soup)

sharkgaming_handler = SharkGamingHandler("https://sharkgaming.dk/asus-gladius-ii-origin-gaming-mouse")
sharkgaming_soup = sharkgaming_handler._request_product_data()
sharkgaming_handler._get_common_data(sharkgaming_soup)

newegg_handler = NeweggHandler(
    "https://www.newegg.com/sony-wh1000xm4b-bluetooth-headset-black/p/0G6-001C-00614?Description=sony%20xm4&cm_re=sony_xm4-_-0G6-001C-00614-_-Product&quicklink=true"
)
newegg_soup = newegg_handler._request_product_data()
newegg_handler._get_common_data(newegg_soup)


class TestKomplettHandler:
    def test_get_product_info(self):
        actual = komplett_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = komplett_handler._get_product_name(komplett_soup).lower()
        expected = "ASUS GeForce RTX 3090 ROG Strix OC".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = komplett_handler._get_product_price(komplett_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = komplett_handler._get_product_currency(komplett_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = komplett_handler._get_product_id(komplett_soup)
        assert isinstance(id, str)
        assert id == "1168438"


class TestProshopHandler:
    def test_get_product_info(self):
        actual = proshop_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = proshop_handler._get_product_name(proshop_soup).lower()
        expected = "Sony WH-1000XM4".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = proshop_handler._get_product_price(proshop_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = proshop_handler._get_product_currency(proshop_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = proshop_handler._get_product_id(proshop_soup)
        assert isinstance(id, str)
        assert id == "2883832"


class TestComputersalgHandler:
    def test_get_product_info(self):
        actual = computersalg_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = computersalg_handler._get_product_name(computersalg_soup).lower()
        expected = "Sony WH-1000XM4 - Hovedtelefoner med mik. - fuld størrelse - Bluetooth - trådløs, kabling - NFC - aktiv støjfjerning - 3,5 mm jackstik - sort".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = computersalg_handler._get_product_price(computersalg_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = computersalg_handler._get_product_currency(computersalg_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = computersalg_handler._get_product_id(computersalg_soup)
        assert isinstance(id, str)
        assert id == "6647865"


class TestElgigantenHandler:
    def test_get_product_info(self):
        actual = elgiganten_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = elgiganten_handler._get_product_name(elgiganten_soup).lower()
        expected = "Sony trådløse around-ear høretelefoner WH-1000XM4 (sort)".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = elgiganten_handler._get_product_price(elgiganten_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = elgiganten_handler._get_product_currency(elgiganten_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = elgiganten_handler._get_product_id(elgiganten_soup)
        assert isinstance(id, str)
        assert id == "200693"


class TestAvXpertenHandler:
    def test_get_product_info(self):
        actual = avxperten_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = avxperten_handler._get_product_name(avxperten_soup).lower()
        expected = "Sony WH-1000XM4 Bluetooth hovedtelefoner (m/ANC) Sort".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = avxperten_handler._get_product_price(avxperten_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = avxperten_handler._get_product_currency(avxperten_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = avxperten_handler._get_product_id(avxperten_soup)
        assert isinstance(id, str)
        assert id == "33590"


class TestAvCablesHandler:
    def test_get_product_info(self):
        actual = avcables_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = avcables_handler._get_product_name(avcables_soup).lower()
        expected = "Sony WH-1000XM4 Over-Ear Bluetooth Headset - Sort".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = avcables_handler._get_product_price(avcables_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = avcables_handler._get_product_currency(avcables_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = avcables_handler._get_product_id(avcables_soup)
        assert isinstance(id, str)
        assert id == "833015"


class TestAmazonHandler:
    def test_get_product_info(self):
        actual = amazon_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = amazon_handler._get_product_name(amazon_soup).lower()
        expected = "Sony WH-1000XM4 Wireless Noise Canceling Overhead Headphones - Black (Renewed)".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = amazon_handler._get_product_price(amazon_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = amazon_handler._get_product_currency(amazon_soup)
        assert isinstance(currency, str)
        assert currency == "USD"

    def test_get_id(self):
        id = amazon_handler._get_product_id(amazon_soup)
        assert isinstance(id, str)
        assert id == "B08HDKHSSN"


# # OBS: There is two Ebay versions - WITH 'itm' IN URL
# class TestEbayHandlerVersionOne:
#     def test_get_product_info(self):
#         actual = ebay_handler_one.get_product_info()
#         assert isinstance(actual, Info)
#         assert actual.valid == True

#     def test_get_name(self):
#         actual = ebay_handler_one._get_product_name(ebay_soup_one).lower()
#         expected = "SET TITLE".lower()
#         assert isinstance(actual, str)
#         assert actual == expected

#     def test_get_price(self):
#         price = ebay_handler_one._get_product_price(ebay_soup_one)
#         assert isinstance(price, float)

#     def test_get_currency(self):
#         currency = ebay_handler_one._get_product_currency(ebay_soup_one)
#         assert isinstance(currency, str)
#         assert currency == "USD"

#     def test_get_id(self):
#         id = ebay_handler_one._get_product_id(ebay_soup_one)
#         assert isinstance(id, str)
#         assert id == "SET ID"


# # OBS: There is two Ebay versions - WITHOUT 'itm' IN URL
# class TestEbayHandlerVersionTwo:
#     def test_get_product_info(self):
#         actual = ebay_handler_two.get_product_info()
#         assert isinstance(actual, Info)
#         assert actual.valid == True

#     def test_get_name(self):
#         actual = ebay_handler_two._get_product_name(ebay_soup_two).lower()
#         expected = "SET TITLE".lower()
#         assert isinstance(actual, str)
#         assert actual == expected

#     def test_get_price(self):
#         price = ebay_handler_two._get_product_price(ebay_soup_two)
#         assert isinstance(price, float)

#     def test_get_currency(self):
#         currency = ebay_handler_two._get_product_currency(ebay_soup_two)
#         assert isinstance(currency, str)
#         assert currency == "USD"

#     def test_get_id(self):
#         id = ebay_handler_two._get_product_id(ebay_soup_two)
#         assert isinstance(id, str)
#         assert id == "SET ID"


class TestPowerHandler:
    def test_get_product_info(self):
        actual = power_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = power_handler._get_product_name(power_soup).lower()
        expected = "SONY WH-1000XM4 TRÅDLØSE STØJDÆMPENDE HOVEDTELEFONER BLÅ".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = power_handler._get_product_price(power_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = power_handler._get_product_currency(power_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = power_handler._get_product_id(power_soup)
        assert isinstance(id, str)
        assert id == "1185731"


class TestExpertHandler:
    def test_get_product_info(self):
        actual = expert_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = expert_handler._get_product_name(expert_soup).lower()
        expected = "SONY WH-1000XM4 TRÅDLØSE STØJDÆMPENDE HOVEDTELEFONER SORT".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = expert_handler._get_product_price(expert_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = expert_handler._get_product_currency(expert_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = expert_handler._get_product_id(expert_soup)
        assert isinstance(id, str)
        assert id == "1106907"


class TestMMVisionHandler:
    def test_get_product_info(self):
        actual = mmvision_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = mmvision_handler._get_product_name(mmvision_soup).lower()
        expected = "Asus ZenBook Duo 14 UX482".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = mmvision_handler._get_product_price(mmvision_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = mmvision_handler._get_product_currency(mmvision_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = mmvision_handler._get_product_id(mmvision_soup)
        assert isinstance(id, str)
        assert id == "6987132"


class TestCoolshopHandler:
    def test_get_product_info(self):
        actual = coolshop_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = coolshop_handler._get_product_name(coolshop_soup).lower()
        expected = "Pokemon Brilliant Diamond - Nintendo Switch".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = coolshop_handler._get_product_price(coolshop_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = coolshop_handler._get_product_currency(coolshop_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = coolshop_handler._get_product_id(coolshop_soup)
        assert isinstance(id, str)
        assert id == "1177871"


class TestSharkGamingHandler:
    def test_get_product_info(self):
        actual = sharkgaming_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = sharkgaming_handler._get_product_name(sharkgaming_soup).lower()
        expected = "ASUS Gladius II Origin gaming mouse".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = sharkgaming_handler._get_product_price(sharkgaming_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = sharkgaming_handler._get_product_currency(sharkgaming_soup)
        assert isinstance(currency, str)
        assert currency == "DKK"

    def test_get_id(self):
        id = sharkgaming_handler._get_product_id(sharkgaming_soup)
        assert isinstance(id, str)
        assert id == "90MP00U1-B0UA00"


class TestNeweggHandler:
    def test_get_product_info(self):
        actual = newegg_handler.get_product_info()
        assert isinstance(actual, Info)
        assert actual.valid == True

    def test_get_name(self):
        actual = newegg_handler._get_product_name(newegg_soup).lower()
        expected = "Sony WH-1000XM4 Wireless Noise-Cancelling Over-Ear Headphones (Black)".lower()
        assert isinstance(actual, str)
        assert actual == expected

    def test_get_price(self):
        price = newegg_handler._get_product_price(newegg_soup)
        assert isinstance(price, float)

    def test_get_currency(self):
        currency = newegg_handler._get_product_currency(newegg_soup)
        assert isinstance(currency, str)
        assert currency == "USD"

    def test_get_id(self):
        id = newegg_handler._get_product_id(newegg_soup)
        assert isinstance(id, str)
        assert id == "0G6-001C-00614"
