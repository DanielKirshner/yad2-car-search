from selenium import webdriver

DIRECTORY = 'reports'

CARS_MODELS = {
   'KIA': 'RIO',
   'SUZUKI': 'SWIFT',
   'TOYOTA': 'YARIS',
   'HYUNDAI': 'I20'
}

CARS_SN = {
    'AUDI': '1',
    'OPAL': '5',
    'ALPHA-ROMEO': '6',
    'BMW': '7',
    'HONDA': '14',
    'TOYOTA': '16',
    'HYUNDAI': '19',
    'MAZDA': '22',
    'MITSUBISHI': '23',
    'MERCEDES': '24',
    'NISAN': '25',
    'SUBARU': '27',
    'SUZUKI': '28',
    'SIAT': '29',
    'SKODA': '31',
    'FIAT': '38',
    'KIA': '40'
}
MODELS_SN = {
    'RIO': '362',
    'SWIFT': '254',
    'YARIS': '1470',
    'I20': '1594'
}

AREA_SN = {
    'CENTER': '2',
    'SHARON': '19',
    'NORTH': '25',
    'SHFELA': '41',
    'SOUTH': '43',
    'JEHUDA': '75',
    'JERUSALEM': '100',
    'HEDERA': '101'
}
GEAR_SN = {
    'MANUAL': '0',
    'AUTO': '1',
    'ROBOTIC': '9'
}

MIN_PRICE = '30000'
MAX_PRICE = '50000'
MIN_YEAR = '2014'
MAX_YEAR = '2020'
FILTERS = {
    'price': {
        min: MIN_PRICE,
        max: MAX_PRICE
    },
    'year': {
        min: MIN_YEAR,
        max: MAX_YEAR
    },
    'area': ['CENTER', 'JERUSALEM'],
    'gear': ['AUTO']
}
BASE_URL = "https://www.yad2.co.il/vehicles/private-cars"

def get_chrome_web_driver(options):
    return webdriver.Chrome(options)


def get_web_driver_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-usb-devices")
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--no-sandbox") 
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\"")
    return options


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')

def get_years(year):
    return f'year={year[min]}-{year[max]}'

def get_model(model):
    return MODELS_SN[model]

def get_models(models):
    return ','.join(list(map(get_model, models)))

def get_car(car):
    return CARS_SN[car]

def get_cars(cars):
    return ','.join(list(map(get_car, cars)))

def get_area(area):
    return AREA_SN[area]

def get_areas(areas):
    a = ','.join(list(map(get_area, areas)))
    return f'topArea={a}'

def get_gear(gear):
    return GEAR_SN[gear]

def get_gears(gears):
    a = ','.join(list(map(get_gear, gears)))
    return f'gearBox={a}'

def get_car_url(cars_models):
    return f'manufacturer={get_cars(cars_models.keys())}&model={get_models(cars_models.values())}'

def get_price(price):
    return f'price={price[min]}-{price[max]}'

def get_with_image(image):
    if image:
        return 'imgOnly=1'
    else:
        return ''

def get_with_price(price):
    if price:
        return 'priceOnly=1'
    else:
        return ''

def build_url(base_url, price, year, cars_models, areas, gears, image, with_price):
    return f'{base_url}?{get_price(price)}&{get_years(year)}&{get_car_url(cars_models)}&{get_with_image(image)}&{get_with_price(price)}&{get_areas(areas)}&{get_gears(gears)}'