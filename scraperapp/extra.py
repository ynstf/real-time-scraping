import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from .models import Product

from selenium.common.exceptions import WebDriverException


def extra_scrape(url, products_number, repetition_interval, caty, driver):

    
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')
    try:
        prods = int(soup.find("section",{'class':"product-count"}).text.strip().split(' ')[0])
    except:
        prods = 10

    my_prod=0
    product_scraped=0
    product_info = []

    while my_prod<int(prods)-2:
        page=1
        urln = url.split('pg=')[0]+f'&pg={page}'
        page+=1
        driver.get(urln)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        alll = soup.find_all("section",{'class':"product-tile-wrapper"})

        for p in alll:
            my_prod+=1
            try:
                discount_rate = p.find('div', {'class':"discount-side-below-striked"}).text.strip()
            except:
                discount_rate = None

            if discount_rate:
                print(discount_rate)


                title = p.find('div', class_='product-name').text.strip()
                print(title)

                try:
                    product_url = p.find('a', class_='position-relative').get('href')
                    product_url = "https://www.extra.com"+product_url
                except:
                    product_url = ''
                print(product_url)


                try:
                    old_price = p.find('div', class_='secondary-price').span.text.strip()+' SAR'
                except:
                    old_price = ''
                print(old_price)

                try:
                    new_price = p.find('span', class_='price').text.strip()+' SAR'
                except:
                    new_price=''
                print(new_price)

                #image
                try:
                    image_url = p.find('img', class_='img-hover').get('src')
                except:
                    image_url = ""
                print(image_url)

                #desc
                try:
                    desc = p.find('section', class_='product-stats-container').text.strip()
                except:
                    desc = ''
                print(desc)


                print()
                if (product_url != None)  and (new_price != None) and (old_price != None) and (discount_rate != None) and (title != None) :
                    product_scraped+=1
                    product_info.append({
                        'Title': title,
                        'Image_URL': image_url,
                        'Price': new_price,
                        'Discount': discount_rate,
                        'original_price':old_price,
                        'description':desc,
                        'Product_URL':product_url
                    })

                    product = Product(
                    title= title,
                    image_url=image_url,
                    price=new_price,
                    discount=discount_rate,
                    original_price=old_price,
                    product_url=product_url,
                    catygorie=caty,
                    scraped_from=url.replace('/', 'y'),
                    added_from="extra",
                    first_img = image_url,
                    duration=repetition_interval,
                    description=desc
                    )

                    product.save()

                    print('i have now', product_scraped)
                    print('i want ',products_number)
                    if product_scraped >= products_number:
                        driver.close()
                        driver.quit()
                        print("i break")
                        break
        if product_scraped >= products_number:
            print("i break")
            driver.quit()
            try:
                driver.close()
            except WebDriverException:
                pass

            break
        driver.close()


