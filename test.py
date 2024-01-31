from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

url = "https://www.aliexpress.com/w/wholesale-Women's-Sunglasses.html?spm=a2g0o.best.allcategoriespc.145.73852c25A8BbeA&categoryUrlParams=%7B%22q%22%3A%22Women%27s%20Sunglasses%22%2C%22s%22%3A%22qp_nw%22%2C%22osf%22%3A%22categoryNagivateOld%22%2C%22sg_search_params%22%3A%22on___%2528%2520prism_tag_id%253A%25271000337683%2527%2520%2529%22%2C%22guide_trace%22%3A%220f682b8d-ff8c-4209-b412-0c7e3467deb6%22%2C%22scene_id%22%3A%2230630%22%2C%22searchBizScene%22%3A%22openSearch%22%2C%22recog_lang%22%3A%22en%22%2C%22bizScene%22%3A%22categoryNagivateOld%22%2C%22guideModule%22%3A%22unknown%22%2C%22postCatIds%22%3A%22200000297%2C36%2C1501%2C18%2C200003922%22%2C%22scene%22%3A%22category_navigate%22%7D&isFromCategory=y"

# Set up the Chrome webdriver
#chrome_service = ChromeService(executable_path='/path/to/chromedriver')  # Specify the path to your chromedriver executable
#driver = webdriver.Chrome(service=chrome_service)

options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # Run the browser in headless mode
#options.add_argument("--window-size=1920,1080")  # Set the window size
driver = webdriver.Firefox(options=options)
# Open the webpage
driver.get(url)

# Scroll down to load more products (you may need to adjust the number of scrolls based on your needs)
for _ in range(5):
    ActionChains(driver).send_keys(Keys.END).perform()
    time.sleep(2)  # Allow time for the content to load

# Get the HTML content after loading all products
html_content = driver.page_source

# Close the webdriver
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
product_divs = soup.find_all('div', class_='list--gallery--C2f2tvm search-item-card-wrapper-gallery')

# List to store all product information
all_products_info = []

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

    product_info = {
        'Title': title,
        'Image URL': image_url,
        'Price': price,
        'Discount': discount,
        'Units Sold': units_sold,
        'Shipping': shipping,
        'Store': store
    }

    if product_info:
        # Append the product information to the list
        all_products_info.append(product_info)

# Print or use the list of all product information as needed
print(all_products_info)
