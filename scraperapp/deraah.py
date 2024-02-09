from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import Product
import logging
import time
import re


logger = logging.getLogger(__name__)

def deraah_scrape(url, products_number, repetition_interval, caty):
    print("hii")
    
    try :
        logger.error("open drive")

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

        # Open the webpage
        driver.get(url)

        logger.error(f"i get : {url}")
        
        try:
            element = driver.find_element(By.CLASS_NAME, "b-cookie-message__footer")
            # Click on the element
            element.click()
            logger.error("accept cookies clicked")
        except:
            logger.error("no button of accepte cookies")

        number_product = products_number
        prodact_per_page = 12
        num_scrolls = number_product//prodact_per_page

        product_info = []

        temp = 0
        while len(product_info) < products_number and temp<=num_scrolls :
            n=1
            scroll_step = 1300  # Adjust this value to control the scrolling distance
            
            n_scroll = 1
            for _ in range(num_scrolls+2):
                # Scroll down by the specified step
                time.sleep(2)
                print(f"scroll {n_scroll}")
                driver.execute_script(f"window.scrollBy(0, {scroll_step});")
                n_scroll+=1


            # Get the HTML content after loading all products
            html_content = driver.page_source
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            alll = soup.find_all('div', class_='product-grid__tile')
            print(len(alll))


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
                
                
                
                if discount_rate != None and state=="avaliable":
                    n+=1
                    logger.error(f"product : {n}")

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
            print(len(product_info))
            p+=1
        # Close the WebDriver after scraping
        driver.quit()

    except Exception as e:
        logger.error(f"Error in scrape_products: {e}")
        print(e)
        raise
    logger.info("Scraping completed successfully")


