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

url = "https://cvaley.com/ar/offers"


def cvaley_scrape(url, products_number, repetition_interval,caty,driver):
    try :
        
        # Open the webpage
        driver.get(url)

        for i in range(20):
            try:
                element = driver.find_element(By.CLASS_NAME, "s-infinite-scroll-btn")
                # Click on the element
                element.click()
                print("found more product button")
                time.sleep(2)
            except:
                time.sleep(2)
                print("not found more product button")
                
            html = driver.page_source
            soup = BeautifulSoup(html,'lxml')

            cards = soup.find_all("div",{"class":"s-product-card-content"})
            descount = []
            urls = []

            for card in cards:
                try:
                    descount.append(card.find("div",{"class":"s-product-card-sale-price"}).span)
                    urls.append(card.find("h3",{"class":"s-product-card-content-title"}).a.get("href"))
                except:
                    pass
            if len(descount)> products_number:
                break
        
        product_scraped=0
        product_info = []

        for u in urls:
            html = requests.get(u).content
            soup = BeautifulSoup(html,'lxml')
            
            product_url = u
            print(product_url)
            
            title = soup.find("h1",{'class':'text-xl md:text-2xl leading-10 font-bold mb-6 text-gray-800'}).text.strip()
            #print(title)
            
            desc = soup.find("div",{'class':'product__description'}).text.strip()
            #print(desc)
            
            old_price = soup.find('span',{'class':"before-price"}).text.strip()
            #print(old_price)
            
            new_price = soup.find('h4',{'class':"total-price"}).text.strip()
            #print(new_price)
            
            
            try:
                old_price_str = old_price
                new_price_str = new_price
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

            #print(discount_rate)
            
            image_url=[]
            slid = soup.find_all('div',{'class':'slide--one-fourth'})
            if len(slid)>0:
                for img in slid:
                    #print(img.find('img').get('src'))
                    image_url.append(img.find('img').get('src'))
            else:
                img = soup.find('img',{'class':'h-full object- w-full'}).get('src')
                image_url.append(img)
                #print(img)

            #print(image_url)
            

            print()
            if (discount_rate != None) and (title != None) and (product_url != None)  and (new_price != None) and (old_price != None) and (discount_rate != None) and (title != None) :
                product_scraped+=1
                product_info.append({
                    'Title': title,
                    'Image_URL': image_url,
                    'Price': new_price,
                    'Discount': discount_rate,
                    'original_price':old_price,
                    'description':desc,
                    'Product_URL':product_url})
                product = Product(
                    title= title,
                    image_url=image_url,
                    price=new_price,
                    discount=discount_rate,
                    original_price=old_price,
                    product_url=product_url,
                    catygorie=caty,
                    scraped_from=url.replace('/', 'y'),
                    added_from="cvaley",
                    duration=repetition_interval,
                    first_img = image_url[0],
                    description=desc)
                product.save()

                print('i have now', product_scraped)
                print('i want ',products_number)
                if product_scraped >= products_number:
                    print("i break")
                    driver.quit()
                    break
        
        print(product_info)
        driver.quit()
    except:
        driver.quit()
    finally:
        driver.quit()
    driver.quit()