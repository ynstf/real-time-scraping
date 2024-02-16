from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from scraperapp.models import Product
from scraperapp.models import AliexpressAction,DeraahAction,NiceonesaAction,ExtraAction,CvaleyAction
from scraperapp.views import niceonesa_scrape_products,scrape_products, deraah_scrape_products, cvaley_scrape_products, extra_scrape_products
from .serializers import TaskSerializer, ProductSerializer
from background_task.models import Task
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict


@api_view(['GET'])
def status(request, id):
    # Retrieve details about a scraping task
    task = get_object_or_404(Task, id=id)

    task_params_str = model_to_dict(task)["task_params"]
    task_params_list = json.loads(task_params_str)
    url =  task_params_list[0][0]
    products_number =  task_params_list[0][1]
    duration =  task_params_list[0][2]
    category =  task_params_list[0][3]
    
    # Create a dictionary with the required information
    task_info = {
        'status': 'running' if task.locked_at else 'completed',
        'latest_errors': task.last_error,
        'task_provider': task.task_name.split('.')[-1].split('_scrape_products')[0] ,  # Use the field that represents category in your model
        'url':url,
        'products_number':products_number,
        'duration':duration,
        'category':category
    }

    return JsonResponse(task_info)

@api_view(['GET'])
def products(request):
    # Retrieve all products from the database
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def tasks(request,provider):
    # Handle the POST request to start a scraping task
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        url = data['url']
        products_number = data["products_number"]
        repetition_interval = data["duration"]
        caty = data["category"]

        ###################### niceonesa #################
        if provider == "niceonesa":
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
                return Response({'status': f"started: {niceonesa_action}"})

            except Exception as e:
                print(f"Error in scrape_products: {e}")
                return Response({'status': f"Error in scrape products: {e}"}, status=400)

        ###################### niceonesa #################
        elif provider == "aliexpress":
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
                return Response({'status': f"started: {aliexpress_action}"})

            except Exception as e:
                print(f"Error in scrape_products: {e}")
                return Response({'status': f"Error in scrape products: {e}"}, status=400)
        
        ###################### deraah #################
        elif provider == "deraah":
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
                return Response({'status': f"started: {deraah_action}"})

            except Exception as e:
                print(f"Error in scrape_products: {e}")
                return Response({'status': f"Error in scrape products: {e}"}, status=400)

        ###################### cvaley #################
        elif provider ==  "cvaley" :
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
                return Response({'status': f"started: {cvaley_action}"})

            except Exception as e:
                print(f"Error in scrape_products: {e}")
                return Response({'status': f"Error in scrape products: {e}"}, status=400)

        ###################### extra #################
        elif provider ==  "extra" :
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
                return Response({'status': f"started: {extra_action}"})

            except Exception as e:
                print(f"Error in scrape_products: {e}")
                return Response({'status': f"Error in scrape products: {e}"}, status=400)


        else:
            return Response({'status': 'provider not supported'}, status=400)



    else:
        return Response({'data': "data not valid"})