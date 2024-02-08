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

logger = logging.getLogger(__name__)



###################  dashboard  ###################
def dashboard(request):
    shoops = [
        {"name":"Alieexpress","url":"/aliexpress/","image":"https://ae01.alicdn.com/kf/Sa0202ec8a96a4085962acfc27e9ffd04F/1080x1080.jpg"},
        ]
    context = {"shoops":shoops}
    return render(request, 'dashboard.html', context)


###################  result page  ###################
def result(request,url):
    # Retrieve all products from the database
    # products = Product.objects.all()
    products = Product.objects.filter(scraped_from= url)
    # Pass the products to the template
    context = {'products': products}
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
    except Task.DoesNotExist:
        status = 'not_started'
    return JsonResponse({'status': status})

@background
def scrape_products(url, products_number, repetition_interval,caty):
    while True:
        task_name = 'scraperapp.views.scrape_products'  
        task = Task.objects.filter(task_name=task_name)
        print(task)
        if task.exists() :
            pass
        else:
            break


        scrape(url, products_number, repetition_interval,caty)
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



###################  darha  ###################

def deraah(request):

    products = []

    context = {'products': products}
    return render(request,"deraah.html",context)

