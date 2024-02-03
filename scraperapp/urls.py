from django.urls import path
from .views import start_scraper, scraper, result, task_status,stop_task, get_scraper_status, get_task_status,dashboard  # Import the 'result' view


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('task_status/', task_status, name='task_status'),
    path('stop_task/', stop_task, name='stop_task'),
    path('start_scraper/', start_scraper, name='start_scraper'),
    path('aliexpress/', scraper, name='scraper'),
    path('get_scraper_status/', get_scraper_status, name='get_scraper_status'),
    path('get_task_status/<str:url>/', get_task_status, name='get_task_status'),
    path('result/<str:url>/', result, name='result'),
    # ... other URL patterns ...
]