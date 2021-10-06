from django.urls import path
from . import views

appname = 'practice'

urlpatterns = [

    #페이지
    path('', views.index),
    path('index.html',views.index, name='index'),
    
    path('charts.html',views.charts),
    path('charts_fin.html',views.charts_fin),
    path('samsung.html', views.samsung),
    path('sk_hynicx.html', views.sk_hynicx),
    path('hyundai.html', views.hyundai),
    path('lg_chem.html', views.lg_chem),
    path('celltrion.html', views.celltrion),
    
    # 주식, 코스피 그래프
    path('index.html/<int:yearid>/', views.index, name='result'),
    path('samsung.html/<int:yearid>/', views.samsung, name='samsung'),
    path('hyundai.html/<int:yearid>/', views.hyundai, name='hyundai'),
    path('sk_hynicx.html/<int:yearid>/', views.sk_hynicx,name='sk_hynicx'),
    path('lg_chem.html/<int:yearid>/', views.lg_chem,name='lg_chem'),
    path('celltrion.html/<int:yearid>/', views.celltrion,name='celltrion'),

    # 투표
    path(r'^like/$', views.samsung_chk, name='samsung_chk'),

]