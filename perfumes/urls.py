from django.urls import path
from . import views

app_name = 'perfumes'

urlpatterns = [
    path('', views.perfume_list, name='list'),
    path('<slug:slug>/', views.perfume_detail, name='detail'),
]

