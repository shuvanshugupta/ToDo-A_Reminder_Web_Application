from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
    path('',views.todohome,name='todohome'),
    path('add',views.add, name='add'),
    path('<int:pk>',views.delete,name='delete'),
]
