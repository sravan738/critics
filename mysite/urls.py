from django.urls import path
from . import views
urlpatterns = [
    path('', views.index3),
    path('2', views.index2),
    path('home', views.index),
    path('thor',views.thor),
    path('avengers',views.avengers),
    path('sherlock', views.sherlock),
    path('lion', views.lion),
    path('saveComment', views.saveComment),
    path('about', views.about),
    path('textfile', views.textfile),
    path('csv', views.csv),
    path('token', views.token001),
    path('login', views.login),
    path('visual', views.token003),
    path('classification', views.classification),

]
