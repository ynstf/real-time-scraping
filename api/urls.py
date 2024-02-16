from django.urls import path
from .views import tasks, status, products
urlpatterns = [
    path('v1/tasks/<str:provider>', tasks , name='tasks'),
    path('v1/status/<int:id>', status , name='status'),
    path('v1/products', products , name='products'),
]

