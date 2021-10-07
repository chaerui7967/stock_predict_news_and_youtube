from django.urls import path
from . import views

appname = 'practice'

urlpatterns = [
    path('', views.index),
    path('index.html',views.index),
    path('charts.html',views.charts),
    path('samsung.html', views.samsung),
    path('sk_hynicx.html', views.sk_hynicx),
    path('hyundai.html', views.hyundai),
    path('lg_chem.html', views.lg_chem),
    path('celltrion.html', views.celltrion),


]