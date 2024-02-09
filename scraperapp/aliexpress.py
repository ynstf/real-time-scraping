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


logger = logging.getLogger(__name__)


def scrape(url, products_number, repetition_interval, caty):
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


        """change the region and currency"""
        try:
            # Find the element by class name
            element = driver.find_element(By.CLASS_NAME, "ship-to--menuItem--WdBDsYl")
            # Click on the element
            element.click()
            time.sleep(1)
            # Find the element by class name
            element = driver.find_element(By.CLASS_NAME, "select--text--1b85oDo")
            # Click on the element
            element.click()
            time.sleep(1)
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.country-flag-y2023.SA'))
            )
            # Click on the element
            element.click()
            time.sleep(1)
            show_more_button = WebDriverWait(driver, 6).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "USD ( الدولار الأمريكي )")]'))
                        )
            show_more_button.click()
            time.sleep(1)
            show_more_button = WebDriverWait(driver, 6).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "SAR ( ريال سعودي )")]'))
                        )
            show_more_button.click()
            time.sleep(1)
            # Find the element by class name
            element = driver.find_element(By.CLASS_NAME, "es--saveBtn--w8EuBuy")
            # Click on the element
            element.click()


            logger.error("language and currency changed to saudi")
        except:
            logger.error("Error in change to saudi task")
        
        time.sleep(3)
        driver.get(url)
        logger.error("redirect to the url")

        product_info = []
        while len(product_info) < products_number:
            n=1
            p=1
            #current_url = f"{url}&page={p}"
            #current_url=f"https://ar.aliexpress.com/w/wholesale-%D9%82%D8%A8%D8%B9%D8%A9-%D9%85%D8%B6%D8%AD%D9%83%D8%A9.html?isFromCategory=y&categoryUrlParams=%7B%22q%22%3A%22%D9%82%D8%A8%D8%B9%D8%A9+%D9%85%D8%B6%D8%AD%D9%83%D8%A9%22%2C%22s%22%3A%22qp_nw%22%2C%22osf%22%3A%22categoryNagivateOld%22%2C%22sg_search_params%22%3A%22on___%2528%2520prism_tag_id%253A%25271000342180%2527%2520%2529%22%2C%22guide_trace%22%3A%2216aeb945-7528-4faa-8ed1-79406b7d038b%22%2C%22scene_id%22%3A%2230630%22%2C%22searchBizScene%22%3A%22openSearch%22%2C%22recog_lang%22%3A%22ar%22%2C%22bizScene%22%3A%22categoryNagivateOld%22%2C%22guideModule%22%3A%22unknown%22%2C%22postCatIds%22%3A%22200000297%2C36%2C1501%2C18%2C200003922%22%2C%22scene%22%3A%22category_navigate%22%7D&page={p}&g=y&SearchText=%D9%82%D8%A8%D8%B9%D8%A9+%D9%85%D8%B6%D8%AD%D9%83%D8%A9"
            current_url = f"{url}&page={p}"
            logger.info(f"Processing URL: {current_url} in page = {p}")
            driver.get(current_url)
            scroll_step = 700  # Adjust this value to control the scrolling distance

            # Define the number of scrolls you want
            num_scrolls = 10

            # Scroll down incrementally
            n_scroll = 1
            for _ in range(num_scrolls):
                # Scroll down by the specified step
                logger.error(f"scroll {n_scroll}")
                n_scroll+=1

                driver.execute_script(f"window.scrollBy(0, {scroll_step});")

                # Wait for a short time to allow content to load
                time.sleep(1)

            html_content = driver.page_source

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            product_divs = soup.find_all('div', class_='list--gallery--C2f2tvm search-item-card-wrapper-gallery')


            # Loop through each product and scrape information
            for product_div in product_divs:
                title = product_div.find('h3', class_='multi--titleText--nXeOvyr').text.strip()
                try:
                    image_url = product_div.find('img', class_='multi--img--1IH3lZb').get('src')
                except:
                    try:
                        image_url = product_div.find('img', class_='images--item--3XZa6xf').get('src')
                    except:
                        image_url = None

                price_element = product_div.find('div', class_='multi--price-sale--U-S0jtj')
                price = price_element.text.strip() if price_element else None
                discount_element = product_div.find('span', class_='multi--discount--3hksz5G')
                discount = discount_element.text.strip() if discount_element else None
                units_sold_element = product_div.find('span', class_='multi--trade--Ktbl2jB')
                units_sold = units_sold_element.text.strip() if units_sold_element else None
                shipping_element = product_div.find('span', class_='tag--text--1BSEXVh tag--textStyle--3dc7wLU multi--serviceStyle--1Z6RxQ4')
                shipping = shipping_element.text.strip() if shipping_element else None
                store_element = product_div.find('span', class_='cards--store--3GyJcot')
                store = store_element.text.strip() if store_element else None

                try:
                    product_url = product_div.find('a', class_='multi--container--1UZxxHY cards--card--3PJxwBm search-card-item').get('href')
                except:
                    product_url = None



                if discount != None:
                    n=+1
                    logger.error(f"product {n}")
                    
                    # Find the original price element
                    original_price_element = product_div.find('div', class_='multi--price-original--1zEQqOK')

                    # Extract the original price text if the element is found
                    original_price = original_price_element.text.strip() if original_price_element else None
                    
                    product_info.append({
                        'Title': title,
                        'Image_URL': image_url,
                        'Price': price,
                        'Discount': discount,
                        'original_price':original_price,
                        'Units_Sold': units_sold,
                        'Shipping': shipping,
                        'Store': store,
                        'Product_URL':product_url,
                        'category':caty,
                        'scraped_from':url
                    })
                    # Save the scraped data to the database
                    product = Product(
                        title=title,
                        image_url=image_url,
                        price=price,
                        discount=discount,
                        original_price=original_price,
                        units_sold=units_sold,
                        shipping=shipping,
                        store=store,
                        product_url=product_url,
                        catygorie=caty,
                        scraped_from=url.replace('/', 'y'),
                        added_from="aliexpress",
                        duration=repetition_interval

                        
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


