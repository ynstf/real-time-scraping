from django.shortcuts import render
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time



def scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))  # Default to 10 if not provided

        


        if url:
            
            try:
                options = webdriver.FirefoxOptions()
                options.add_argument("--headless")  # Run the browser in headless mode
                options.add_argument("--window-size=1920,1080")  # Set the window size
                driver = webdriver.Firefox(options=options)
                # Open the webpage
                #driver.get(url)

                product_info = []
                while len(product_info) < products_number:
                    p=1
                    current_url = f"{url}&page={p}"
                    driver.get(current_url)
                    scroll_step = 700  # Adjust this value to control the scrolling distance

                    # Get the current scroll height
                    last_height = driver.execute_script("return document.body.scrollHeight")

                    # Define the number of scrolls you want
                    num_scrolls = 10

                    # Scroll down incrementally
                    for _ in range(num_scrolls):
                        # Scroll down by the specified step
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
                    print(len(product_info))
                    p+=1



                return render(request, 'result.html', {'product_info': product_info})
            except Exception as e:
                return render(request, 'error.html', {'error_message': str(e)})

    return render(request, 'scraper.html')
