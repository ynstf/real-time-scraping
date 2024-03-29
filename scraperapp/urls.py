from django.urls import path
from .views import start_scraper, scraper, result, task_status,stop_task, get_scraper_status, get_task_status,dashboard
from .views import niceonesa_start_scraper, niceonesa_scraper, niceonesa_task_status, niceonesa_stop_task, niceonesa_get_scraper_status, niceonesa_get_task_status
from .views import deraah_scraper,deraah_start_scraper,deraah_get_scraper_status, deraah_task_status,deraah_stop_task,deraah_get_task_status
from django.conf import settings
from django.conf.urls.static import static

from .views import cvaley_scraper, cvaley_start_scraper, cvaley_get_scraper_status, cvaley_task_status, cvaley_stop_task, cvaley_get_task_status
from .views import extra_scraper, extra_start_scraper, extra_get_scraper_status, extra_task_status, extra_stop_task, extra_get_task_status

urlpatterns = [
    
    # general pages
    path('', dashboard, name='dashboard'),
    path('result/<str:url>/', result, name='result'),

    # for aliexpress pages
    path('start_scraper/', start_scraper, name='start_scraper'),
    path('aliexpress/', scraper, name='scraper'),
    path('get_scraper_status/', get_scraper_status, name='get_scraper_status'),
    path('get_task_status/<str:url>/', get_task_status, name='get_task_status'),
    path('task_status/', task_status, name='task_status'),
    path('stop_task/', stop_task, name='stop_task'),

    # deraah pages
    path('deraah/', deraah_scraper, name='deraah_scraper'),
    path('deraah_start_scraper/', deraah_start_scraper, name='deraah_start_scraper'),
    path('deraah_get_scraper_status/', deraah_get_scraper_status, name='deraah_get_scraper_status'),
    path('deraah_task_status/', deraah_task_status, name='deraah_task_status'),
    path('deraah_stop_task/', deraah_stop_task, name='deraah_stop_task'),
    path('deraah_get_task_status/<str:url>/', deraah_get_task_status, name='deraah_get_task_status'),


    # niceonesa pages
    path('niceonesa/', niceonesa_scraper, name='niceonesa_scraper'),
    path('niceonesa_start_scraper/', niceonesa_start_scraper, name='niceonesa_start_scraper'),
    path('niceonesa_get_scraper_status/', niceonesa_get_scraper_status, name='niceonesa_get_scraper_status'),
    path('niceonesa_task_status/', niceonesa_task_status, name='niceonesa_task_status'),
    path('niceonesa_stop_task/', niceonesa_stop_task, name='niceonesa_stop_task'),
    path('niceonesa_get_task_status/<str:url>/', niceonesa_get_task_status, name='niceonesa_get_task_status'),

    # cvaley pages
    path('cvaley/', cvaley_scraper, name='cvaley_scraper'),
    path('cvaley_start_scraper/', cvaley_start_scraper, name='cvaley_start_scraper'),
    path('cvaley_get_scraper_status/', cvaley_get_scraper_status, name='cvaley_get_scraper_status'),
    path('cvaley_task_status/', cvaley_task_status, name='cvaley_task_status'),
    path('cvaley_stop_task/', cvaley_stop_task, name='cvaley_stop_task'),
    path('cvaley_get_task_status/<str:url>/', cvaley_get_task_status, name='cvaley_get_task_status'),


    # extra pages
    path('extra/', extra_scraper, name='extra_scraper'),
    path('extra_start_scraper/', extra_start_scraper, name='extra_start_scraper'),
    path('extra_get_scraper_status/', extra_get_scraper_status, name='extra_get_scraper_status'),
    path('extra_task_status/', extra_task_status, name='extra_task_status'),
    path('extra_stop_task/', extra_stop_task, name='extra_stop_task'),
    path('extra_get_task_status/<str:url>/', extra_get_task_status, name='extra_get_task_status'),



    
    # ... other URL patterns ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)