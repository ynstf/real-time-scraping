from django.shortcuts import render
import time
from .models import Product,AliexpressAction
from django.http import JsonResponse
from background_task import background
from django.views.decorators.csrf import csrf_exempt
from background_task.models import Task
import logging
from django.http import JsonResponse
from background_task.models import Task
from django.forms.models import model_to_dict
import json
from .aliexpress import scrape
from selenium import webdriver
from django.utils import timezone


logger = logging.getLogger(__name__)



###################  dashboard  ###################
def dashboard(request):
    shoops = [
        {"name":"Alieexpress","url":"/aliexpress/","image":"https://ae01.alicdn.com/kf/Sa0202ec8a96a4085962acfc27e9ffd04F/1080x1080.jpg"},
        {"name":"Deraah","url":"/deraah/","image":"https://www.deraahstore.com/on/demandware.static/Sites-deraah_SA-Site/-/default/dwed8cc41d/images/deraah-logo.png"},
        {"name":"Niceonesa","url":"/niceonesa/","image":"https://cdn.niceonesa.com/web/assets/img/a886eac.svg"},
        {"name":"Cvaley","url":"/cvaley/","image":"https://cdn.salla.sa/PBDO/wzoKKUEOQui0eXcSeMkS6vYSAdWLKtV22DCrJiCm.png"},
        {"name":"Extra","url":"/extra/","image":"https://cdn.extrastores.com/hybris/new_ui_ux/logo/eXtra-logo.svg"},
        ]
    context = {"shoops":shoops}
    return render(request, 'dashboard.html', context)


###################  result page  ###################

def result(request, url):
    # Retrieve all products from the database
    products = Product.objects.filter(scraped_from=url)


    # Calculate the time difference for each product
    current_time = timezone.now()

    valid_products = []
    for product in products:
        time_difference = current_time - product.added_at
        print(time_difference)
        product.duration = timezone.timedelta(minutes=product.duration) - time_difference

        # Only include products with positive duration
        if product.duration.total_seconds() > 0:
            valid_products.append(product)

        

    # Pass the products to the template
    context = {'products': valid_products}
    return render(request, 'result.html', context)

###################  alixpress  ###################
def get_scraper_status(request):
    task_name = 'scraperapp.views.scrape_products'
    task_exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'status': 'started' if task_exists else 'not_started'})

def get_task_status(request, url):
    try:
        task = AliexpressAction.objects.get(url=url)  # Replace YourTaskModel with your actual model
        status = task.status  # Assuming your task model has a 'status' field
        return JsonResponse({'status': status})
    except AliexpressAction.DoesNotExist:
        return JsonResponse({'status': 'not_found'})

def task_status(request):
    task_name = 'scraperapp.views.scrape_products' 
    task = Task.objects.filter(task_name=task_name)
    print(task)
    if task.exists() :
        status = 'running'
    else:
        status = 'completed'
    return JsonResponse({'status': status})

def stop_task(request):
    url = request.GET.get('url', None)
    print(url)
    task_name = 'scraperapp.views.scrape_products'
    try:

        # Filter tasks with the specified task_name
        tasks = Task.objects.filter(task_name=task_name)
        # Delete all tasks in the queryset
        #tasks.delete()

        for task in tasks:
            
            task_params_str = model_to_dict(task)["task_params"]
            task_params_list = json.loads(task_params_str)
            print(task_params_list)
            if task_params_list[0][0] == url:
                task.delete()
        
        urls = AliexpressAction.objects.filter(url=url)
        urls.delete()
        status = 'stopped'
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})

@background
def scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.scrape_products'  
        task = Task.objects.filter(task_name=task_name)
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
        print(task)
        if task.exists() :
            pass
        else:
            break

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)
        scrape(url, products_number, repetition_interval,caty,driver)
        driver.quit()

        #time.sleep(repetition_interval*60)
        for m in range(repetition_interval):
            task_name = 'scraperapp.views.scrape_products' 
            task = Task.objects.filter(task_name=task_name)
            print(task)
            if task.exists() :
                pass
            else:
                break
            time.sleep(60)

@csrf_exempt
def start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        caty = request.POST.get('caty')

        try:
            # Call the scrape_products function directly, without scheduling
            print('test')
            scrape_products(url,products_number,repetition_interval,caty)  # Setting repeat to 0 means it will repeat indefinitely
            # Save the action to the database
            aliexpress_action = AliexpressAction.objects.create(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
                Category=caty,
                status="started"
                )

        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})

def scraper(request):

    aliexpress_actions = AliexpressAction.objects.filter(status="started")
    #print(aliexpress_actions)

    context={
        'tasks_run':aliexpress_actions
    }
    return render(request, 'scraper.html',context=context)



###################  deraah  ###################
from .models import DeraahAction
from .deraah import deraah_scrape

def deraah_scraper(request):

    aliexpress_actions = DeraahAction.objects.filter(status="started")
    #print(aliexpress_actions)
    context={
        'tasks_run':aliexpress_actions
    }
    return render(request,"deraah.html",context)

@csrf_exempt
def deraah_start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        caty = request.POST.get('caty')

        try:
            # Call the scrape_products function directly, without scheduling
            print('test')
            deraah_scrape_products(url,products_number,repetition_interval,caty)  # Setting repeat to 0 means it will repeat indefinitely
            # Save the action to the database
            deraah_action = DeraahAction.objects.create(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
                Category=caty,
                status="started"
                )

        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})


@background
def deraah_scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.deraah_scrape_products'  
        task = Task.objects.filter(task_name=task_name)
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
        print(task)
        if task.exists() :
            pass
        else:
            break
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chrome_options)
        time.sleep(3)
        print("9able")
        deraah_scrape(url, products_number, repetition_interval,caty, driver)
        driver.quit()
        print("ba3d")
        for m in range(repetition_interval):
            print("im sleep")
            print(m)
            task_name = 'scraperapp.views.deraah_scrape_products' 
            task = Task.objects.filter(task_name=task_name)
            print(task)
            if task.exists() :
                pass
            else:
                break
            time.sleep(60)


def deraah_get_scraper_status(request):
    task_name = 'scraperapp.views.deraah_scrape_products'
    task_exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'status': 'started' if task_exists else 'not_started'})

def deraah_task_status(request):
    task_name = 'scraperapp.views.deraah_scrape_products' 
    task = Task.objects.filter(task_name=task_name)
    print(task)
    if task.exists() :
        status = 'running'
    else:
        status = 'completed'
    return JsonResponse({'status': status})

def deraah_stop_task(request):
    url = request.GET.get('url', None)
    print(url)
    task_name = 'scraperapp.views.deraah_scrape_products'
    try:

        # Filter tasks with the specified task_name
        tasks = Task.objects.filter(task_name=task_name)
        # Delete all tasks in the queryset
        #tasks.delete()

        for task in tasks:
            
            task_params_str = model_to_dict(task)["task_params"]
            task_params_list = json.loads(task_params_str)
            print(task_params_list)
            if task_params_list[0][0] == url:
                task.delete()
        
        urls = DeraahAction.objects.filter(url=url)
        urls.delete()
        status = 'stopped'
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})

def deraah_get_task_status(request, url):
    try:
        task = DeraahAction.objects.get(url=url)  # Replace YourTaskModel with your actual model
        status = task.status  # Assuming your task model has a 'status' field
        return JsonResponse({'status': status})
    except DeraahAction.DoesNotExist:
        return JsonResponse({'status': 'not_found'})



###################  niceonesa  ###################
from .models import NiceonesaAction
from .niceonesa import niceonesa_scrape


def niceonesa_get_scraper_status(request):
    task_name = 'scraperapp.views.niceonesa_scrape_products'
    task_exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'status': 'started' if task_exists else 'not_started'})

def niceonesa_get_task_status(request, url):
    try:
        task = NiceonesaAction.objects.get(url=url)  # Replace YourTaskModel with your actual model
        status = task.status  # Assuming your task model has a 'status' field
        return JsonResponse({'status': status})
    except NiceonesaAction.DoesNotExist:
        return JsonResponse({'status': 'not_found'})

def niceonesa_task_status(request):
    task_name = 'scraperapp.views.niceonesa_scrape_products' 
    task = Task.objects.filter(task_name=task_name)
    print(task)
    if task.exists() :
        status = 'running'
    else:
        status = 'completed'
    return JsonResponse({'status': status})

def niceonesa_stop_task(request):
    url = request.GET.get('url', None)
    print(url)
    task_name = 'scraperapp.views.niceonesa_scrape_products'
    try:

        # Filter tasks with the specified task_name
        tasks = Task.objects.filter(task_name=task_name)
        # Delete all tasks in the queryset
        #tasks.delete()

        for task in tasks:
            
            task_params_str = model_to_dict(task)["task_params"]
            task_params_list = json.loads(task_params_str)
            print(task_params_list)
            if task_params_list[0][0] == url:
                task.delete()
        urls = NiceonesaAction.objects.filter(url=url)
        urls.delete()
        status = 'stopped'
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})

@background
def niceonesa_scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.niceonesa_scrape_products'  
        task = Task.objects.filter(task_name=task_name)
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
        print(task)
        if task.exists() :
            pass
        else:
            break


        niceonesa_scrape(url, products_number, repetition_interval,caty)
        #time.sleep(repetition_interval*60)
        for m in range(repetition_interval):
            task_name = 'scraperapp.views.niceonesa_scrape_products' 
            task = Task.objects.filter(task_name=task_name)
            print(task)
            if task.exists() :
                pass
            else:
                break
            time.sleep(60)

@csrf_exempt
def niceonesa_start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        caty = request.POST.get('caty')

        try:
            # Call the scrape_products function directly, without scheduling
            print('test')
            niceonesa_scrape_products(url,products_number,repetition_interval,caty)  # Setting repeat to 0 means it will repeat indefinitely
            # Save the action to the database
            niceonesa_action = NiceonesaAction.objects.create(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
                Category=caty,
                status="started"
                )

        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})

def niceonesa_scraper(request):

    niceonesa_actions = NiceonesaAction.objects.filter(status="started")
    #print(aliexpress_actions)

    context={
        'tasks_run':niceonesa_actions
    }
    return render(request, 'niceonesa.html',context=context)


###################  cvaley  ###################
from .models import CvaleyAction
from .cvaley import cvaley_scrape



def cvaley_get_scraper_status(request):
    task_name = 'scraperapp.views.cvaley_scrape_products'
    task_exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'status': 'started' if task_exists else 'not_started'})

def cvaley_get_task_status(request, url):
    try:
        task = CvaleyAction.objects.get(url=url)  # Replace YourTaskModel with your actual model
        status = task.status  # Assuming your task model has a 'status' field
        return JsonResponse({'status': status})
    except CvaleyAction.DoesNotExist:
        return JsonResponse({'status': 'not_found'})

def cvaley_task_status(request):
    task_name = 'scraperapp.views.cvaley_scrape_products' 
    task = Task.objects.filter(task_name=task_name)
    print(task)
    if task.exists() :
        status = 'running'
    else:
        status = 'completed'
    return JsonResponse({'status': status})

def cvaley_stop_task(request):
    url = request.GET.get('url', None)
    print(url)
    task_name = 'scraperapp.views.cvaley_scrape_products'
    try:

        # Filter tasks with the specified task_name
        tasks = Task.objects.filter(task_name=task_name)
        # Delete all tasks in the queryset
        #tasks.delete()

        for task in tasks:
            
            task_params_str = model_to_dict(task)["task_params"]
            task_params_list = json.loads(task_params_str)
            print(task_params_list)
            if task_params_list[0][0] == url:
                task.delete()
        
        urls = CvaleyAction.objects.filter(url=url)
        urls.delete()
        status = 'stopped'
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})


@background
def cvaley_scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.cvaley_scrape_products'  

        task = Task.objects.filter(task_name=task_name)

        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
        
        print(task)
        if task.exists() :
            pass
        else:
            break

        options = webdriver.FirefoxOptions()
        #options.add_argument("--headless")  # Run the browser in headless mode
        options.add_argument("--window-size=1920,1080")  # Set the window size
        driver = webdriver.Firefox(options=options)

        cvaley_scrape(url, products_number, repetition_interval,caty,driver)
        driver.quit()
        #time.sleep(repetition_interval*60)
        for m in range(repetition_interval):
            task_name = 'scraperapp.views.cvaley_scrape_products' 
            task = Task.objects.filter(task_name=task_name)
            print(task)
            if task.exists() :
                pass
            else:
                break
            time.sleep(60)

@csrf_exempt
def cvaley_start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        caty = request.POST.get('caty')

        try:
            # Call the scrape_products function directly, without scheduling
            print('test')
            cvaley_scrape_products(url,products_number,repetition_interval,caty)  # Setting repeat to 0 means it will repeat indefinitely
            #cvaley_scrape_products(repeat=60)
            # Save the action to the database
            cvaley_action = CvaleyAction.objects.create(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
                Category=caty,
                status="started"
                )

        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})

def cvaley_scraper(request):

    cvaley_actions = CvaleyAction.objects.filter(status="started")
    #print(aliexpress_actions)

    context={
        'tasks_run':cvaley_actions
    }
    return render(request, 'cvaley.html',context=context)



###################  Extra  ###################
from .models import ExtraAction
from .extra import extra_scrape


def extra_get_scraper_status(request):
    task_name = 'scraperapp.views.extra_scrape_products'
    task_exists = Task.objects.filter(task_name=task_name).exists()
    return JsonResponse({'status': 'started' if task_exists else 'not_started'})

def extra_get_task_status(request, url):
    try:
        task = ExtraAction.objects.get(url=url)  # Replace YourTaskModel with your actual model
        status = task.status  # Assuming your task model has a 'status' field
        return JsonResponse({'status': status})
    except ExtraAction.DoesNotExist:
        return JsonResponse({'status': 'not_found'})

def extra_task_status(request):
    task_name = 'scraperapp.views.extra_scrape_products' 
    task = Task.objects.filter(task_name=task_name)
    print(task)
    if task.exists() :
        status = 'running'
    else:
        status = 'completed'
    return JsonResponse({'status': status})

def extra_stop_task(request):
    url = request.GET.get('url', None)
    print(url)
    task_name = 'scraperapp.views.extra_scrape_products'
    try:

        # Filter tasks with the specified task_name
        tasks = Task.objects.filter(task_name=task_name)
        # Delete all tasks in the queryset
        #tasks.delete()

        for task in tasks:
            
            task_params_str = model_to_dict(task)["task_params"]
            task_params_list = json.loads(task_params_str)
            print(task_params_list)
            if task_params_list[0][0] == url:
                task.delete()
        
        urls = ExtraAction.objects.filter(url=url)
        urls.delete()
        status = 'stopped'
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})

@background
def extra_scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.extra_scrape_products'  
        task = Task.objects.filter(task_name=task_name)
        try:
            products = Product.objects.filter(scraped_from=url.replace('/', 'y'))
            products.delete()
        except:
            print('no products found')
        print(task)
        if task.exists() :
            pass
        else:
            break

        
        options = webdriver.FirefoxOptions()
        #loptions.add_argument("--headless")  # Run the browser in headless mode
        options.add_argument("--window-size=1920,1080")  # Set the window size
        driver = webdriver.Firefox(options=options)

        extra_scrape(url, products_number, repetition_interval,caty,driver)

        driver.quit()

        #time.sleep(repetition_interval*60)
        for m in range(repetition_interval):
            task_name = 'scraperapp.views.extra_scrape_products' 
            task = Task.objects.filter(task_name=task_name)
            print(task)
            if task.exists() :
                pass
            else:
                break
            time.sleep(60)
        

@csrf_exempt
def extra_start_scraper(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        products_number = int(request.POST.get('products_number', 10))
        repetition_interval = int(request.POST.get('repetition_interval', 5))  # in minutes
        caty = request.POST.get('caty')

        try:
            # Call the scrape_products function directly, without scheduling
            print('test')
            extra_scrape_products(url,products_number,repetition_interval,caty)  # Setting repeat to 0 means it will repeat indefinitely
            #extra_scrape_products(repeat=60)
            # Save the action to the database
            extra_action = ExtraAction.objects.create(
                url=url,
                products_number=products_number,
                repetition_interval=repetition_interval,
                Category=caty,
                status="started"
                )

        except Exception as e:
            print(f"Error in scrape_products: {e}")
            raise

        # Return a JSON response to indicate that the scraping has started
        return JsonResponse({'status': 'started'})

    return JsonResponse({'status': 'error'})

def extra_scraper(request):

    extra_actions = ExtraAction.objects.filter(status="started")
    #print(aliexpress_actions)

    context={
        'tasks_run':extra_actions
    }
    return render(request, 'extra.html',context=context)



