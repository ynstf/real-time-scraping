from django.urls import path
from .views import start_scraper, scraper, result, task_status,stop_scraper  # Import the 'result' view

urlpatterns = [
    path('task_status/', task_status, name='task_status'),
    path('stop_scraper/', stop_scraper, name='stop_scraper'),
    path('start_scraper/', start_scraper, name='start_scraper'),
    path('scraper/', scraper, name='scraper'),
    path('result/', result, name='result'),  # Add the URL pattern for 'result'
    # ... other URL patterns ...
]