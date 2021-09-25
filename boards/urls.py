from django.urls import path
from . import views

app_name = 'boards'
urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.search,name='search'),
    path('graph/',views.graph,name='graph'),
    path('totalgraph/',views.totalgraph,name='totalgraph'),
]
