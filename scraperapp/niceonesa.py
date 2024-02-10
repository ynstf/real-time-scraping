import requests
from bs4 import BeautifulSoup
from .models import Product


def niceonesa_scrape(url, products_number, repetition_interval, caty):

    print("i start")

    # i want to know the namber of all pages
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'html.parser')
    products = soup.find_all("div", {"class":"product-container"})
    pages = soup.find_all("li", {"class":"page-item"})
    try:
        page_numbers = int(pages[-1].a.get('href').split("page=")[-1])
        print('i found page_numbers')
    except:
        print('page_numbers dont found ')
    

    product_info = []
    product_scraped = 0
    for p in range(1,page_numbers+1):
        
        url = url.split("page")[0]+f"page={p}"
        print(url)
        html = requests.get(url)
        soup = BeautifulSoup(html.content,'html.parser')
        products = soup.find_all("div", {"class":"product-container"})
        
        
        for i in range(len(products)):
            try:
                title = products[i].find("h3", {"class":"product-title"}).text.strip()
            except:
                title = None
            print(title)

            try :
                img = products[i].find('img').get('data-url')
                
            except :
                img= None
            print(img)

            try:
                old_price = products[i].find("h3", {"class":"preReductionPrice"}).text.strip()

            except:
                old_price= None
            print(old_price)


            try:
                discount_rate = products[i].find("span", {"class":"discountBadge mt-3"}).text.strip()
            except:
                discount_rate = None
            print(discount_rate)


            try:
                new_price = products[i].find("h3", {"class":"sellingPrice text-nowrap"}).text.strip()
            except:
                new_price=None
            print(new_price)


            try:
                product_url = products[i].find('a').get('href')

                product_url = "https://niceonesa.com"+product_url.replace('en-US','ar')
                ns = requests.get(product_url)
                soup = BeautifulSoup(ns.content,'html.parser')
                try:
                    desc = soup.find("div", {"class":"pannel-body"}).text.strip().split('ISBN')[0]
                except:
                    decs = None

            except:
                product_url = None
                decs = None

            print(product_url)
            print(desc)

            if (discount_rate != None) and (title != None) and (product_url != None)  and (new_price != None) and (old_price != None) and (discount_rate != None) and (title != None) and (img != None):
                product_scraped+=1
                product_info.append({
                    'Title': title,
                    'Image_URL': img,
                    'Price': new_price,
                    'Discount': discount_rate,
                    'original_price':old_price,
                    'description':desc,
                    'Product_URL':product_url
                })

                product = Product(
                title= title,
                image_url=img,
                price=new_price,
                discount=discount_rate,
                original_price=old_price,
                product_url=product_url,
                catygorie=caty,
                scraped_from=url.replace('/', 'y'),
                added_from="niceonesa",
                duration=repetition_interval,
                description=desc
                )

                product.save()

                print('i have now', product_scraped)
                print('i want ',products_number)
                if product_scraped >= products_number:
                    print("i break")
                    break
            if product_scraped >= products_number:
                print("i break")
                break
        if product_scraped >= products_number:
            print("i break")
            break
