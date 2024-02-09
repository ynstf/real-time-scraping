from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from .models import Product,AliexpressAction
from django.http import JsonResponse
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import logging
import re

logger = logging.getLogger(__name__)


def deraah_scrape(url, products_number, repetition_interval, caty):
    
    """options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run the browser in headless mode
    options.add_argument("--window-size=1920,1080")  # Set the window size
    driver = webdriver.Firefox(options=options)"""


    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

    # Open the webpage
    driver.get(url)
    number_product= products_number
    prodact_per_page = 12

    try:
        element = driver.find_element(By.CLASS_NAME, "b-cookie-message__footer")
        # Click on the element
        element.click()
    except:
        print("no button of accepte cookies")
    
    scroll_step = 1300  # Adjust this value to control the scrolling distance

    # Get the current scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Define the number of scrolls you want
    num_scrolls = number_product//prodact_per_page
    print(num_scrolls)
    # Scroll down incrementally
    n_scroll = 1
    for _ in range(num_scrolls+2):
        # Scroll down by the specified step
        time.sleep(2)
        print(f"scroll {n_scroll}")
        driver.execute_script(f"window.scrollBy(0, {scroll_step});")
        # Get the HTML content after loading all products
        html_content = driver.page_source
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        alll = soup.find_all('div', class_='product-grid__tile')
        n_scroll+=1

    # Get the HTML content after loading all products
    html_content = driver.page_source
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    alll = soup.find_all('div', class_='product-grid__tile')
    print(len(alll))

    product_info = []

    for i in range(len(alll)):
        title = alll[i].find('div', class_='tile-body__title')
        try:
            image_url = alll[i].find('img', class_='js-picture-img product-tile__image').get('src')
        except:
            image_url = None
            
        brand = alll[i].find('div', class_='tile-body__brand')
        
        old_price = alll[i].find('span', class_='b-price__value value')
        
        new_price = alll[i].find('span', class_='value b-price-value')
        
        state= alll[i].find('button', class_='quickview btn btn-secondary m-fullwidth').get('disabled')
        state = "avaliable" if state == None else "out of stock"
        
        
        
        try:
            old_price_str = old_price.text
            new_price_str = new_price.text
            # Extract numeric values using regular expression
            old_price_match = re.search(r'\d+', old_price_str)
            new_price_match = re.search(r'\d+', new_price_str)
            # Convert the matched strings to numeric values
            old = float(old_price_match.group())
            new = float(new_price_match.group())
            # Calculate the discount rate
            discount_rate = f"{((old - new) / old) * 100:.2f}%"
        except:
            discount_rate = None
        
        try:
            product_url = alll[i].find('a', class_='tile-body').get('href')
            product_url = "https://www.deraahstore.com"+product_url
        except:
            product_url = None
        
        print(title.text.strip())
        print(image_url)
        print(brand.text.strip())
        print(old_price.text.split('Price reduced from')[1].split('to')[0].strip())
        print(new_price.text.strip())
        print(state)
        print(discount_rate)
        print(product_url)
        
        
        print()
        
        
        if discount_rate != None and state=="avaliable":
            
            product_info.append({
                'Title': title.text.strip(),
                'Image_URL': image_url,
                'Price': new_price.text.strip(),
                'Discount': discount_rate,
                'original_price':old_price.text.split('Price reduced from')[1].split('to')[0].strip(),
                'Status': state,
                'Brand': brand.text.strip(),
                'Product_URL':product_url
            })
            product = Product(
                title= title.text.strip(),
                image_url=image_url,
                price=new_price.text.strip(),
                discount=discount_rate,
                original_price=old_price.text.split('Price reduced from')[1].split('to')[0].strip(),
                product_url=product_url,
                catygorie=caty,
                scraped_from=url.replace('/', 'y')
            )
            product.save()
    
    # Close the WebDriver after scraping
    driver.quit()


