from django.urls import path
from . import views

appname = 'practice'

urlpatterns = [
    path('', views.index),
    path('index.html',views.index, name='index'),
    # path('index2.html',views.news_pop),
    path('charts.html',views.charts),
    path('samsung.html', views.samsung),
    path('sk_hynicx.html', views.sk_hynicx),
    path('hyundai.html', views.hyundai),
    path('lg_chem.html', views.lg_chem),
    path('celltrion.html', views.celltrion),

    # path('index.html/<int:yearid>/',views.result, name='result'),
    path('index.html/<int:yearid>/', views.index, name='result'),

    path('samsung.html/<int:yearid>/', views.samsung, name='samsung'),
    path('hyundai.html/<int:yearid>/', views.hyundai, name='hyundai'),
    path('sk_hynicx.html/<int:yearid>/', views.sk_hynicx,name='sk_hynicx'),
    path('lg_chem.html/<int:yearid>/', views.lg_chem,name='lg_chem'),
    path('celltrion.html/<int:yearid>/', views.celltrion,name='celltrion'),

    # like chk
    # path('samsung.html/<int:like_chk>/', views.samsung_chk, name='samsung_chk'),
    path(r'^like/$', views.samsung_chk, name='samsung_chk'),

    # path('index.html/(?P<yearid>[0-9]{4})/$', views.result, name='result'),

]