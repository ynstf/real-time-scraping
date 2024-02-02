from django.shortcuts import render
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import json

from .models import Product
from django.http import JsonResponse
from django.urls import reverse
from background_task import background
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from background_task.models import Task
#from background_task.models import Task as BackgroundTask


import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

from django.http import JsonResponse
from background_task.models import Task

def task_status(request):
    task_status = 'running' if Task.objects.filter(task_name='scraperapp.tasks.scrape_products').exists() else 'stopped'
    return JsonResponse({'status': task_status})

def stop_scraper(request):
    # Code to stop the scraper task goes here (e.g., use Task.objects.filter().delete())
    return JsonResponse({'status': 'stopped'})



def scrape(url, products_number, repetition_interval):
    print("hii")
    n=1
    try :
        logger.error("open drive")
        options = webdriver.FirefoxOptions()
        #options.add_argument("--headless")  # Run the browser in headless mode
        options.add_argument("--window-size=1920,1080")  # Set the window size
        driver = webdriver.Firefox(options=options)
        # Open the webpage
        #driver.get(url)
        logger.error(f"{url} {products_number} {repetition_interval}")

        product_info = []
        while len(product_info) < products_number:

            p=1
            #current_url = f"{url}&page={p}"
            #current_url=f"https://ar.aliexpress.com/w/wholesale-%D9%82%D8%A8%D8%B9%D8%A9-%D9%85%D8%B6%D8%AD%D9%83%D8%A9.html?isFromCategory=y&categoryUrlParams=%7B%22q%22%3A%22%D9%82%D8%A8%D8%B9%D8%A9+%D9%85%D8%B6%D8%AD%D9%83%D8%A9%22%2C%22s%22%3A%22qp_nw%22%2C%22osf%22%3A%22categoryNagivateOld%22%2C%22sg_search_params%22%3A%22on___%2528%2520prism_tag_id%253A%25271000342180%2527%2520%2529%22%2C%22guide_trace%22%3A%2216aeb945-7528-4faa-8ed1-79406b7d038b%22%2C%22scene_id%22%3A%2230630%22%2C%22searchBizScene%22%3A%22openSearch%22%2C%22recog_lang%22%3A%22ar%22%2C%22bizScene%22%3A%22categoryNagivateOld%22%2C%22guideModule%22%3A%22unknown%22%2C%22postCatIds%22%3A%22200000297%2C36%2C1501%2C18%2C200003922%22%2C%22scene%22%3A%22category_navigate%22%7D&page={p}&g=y&SearchText=%D9%82%D8%A8%D8%B9%D8%A9+%D9%85%D8%B6%D8%AD%D9%83%D8%A9"
            current_url = f"{url}&page={p}"
            logger.info(f"Processing URL: {current_url}")
            driver.get(current_url)
            scroll_step = 700  # Adjust this value to control the scrolling distance

            # Define the number of scrolls you want
            num_scrolls = 10

            # Scroll down incrementally
            for _ in range(num_scrolls):
                # Scroll down by the specified step
                logger.error(f"scroll")

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
                    logger.error(f"loop {n}")
                    
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
                        'Product_URL':product_url
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
                        product_url=product_url
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



@background
def scrape_products(url, products_number, repetition_interval):
    # Your scraping logic goes here
    while True:


        scrape(url, products_number, repetition_interval)
        time.sleep(repetition_interval*60)


@csrf_exempt
def start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        
        try:
            # Call the scrape_products function directly, without scheduling
            """scrape_products(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
            )"""
            print('test')
            scrape_products(url,products_number,repetition_interval)  # Setting repeat to 0 means it will repeat indefinitely


        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})


def scraper(request):
    return render(request, 'scraper.html')


def result(request):
    # Retrieve all products from the database
    products = Product.objects.all()

    # Pass the products to the template
    context = {'products': products}
    return render(request, 'result.html', context)  # Replace 'result.html' with your actual template