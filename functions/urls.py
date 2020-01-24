from django.urls import path

from . import views

app_name = 'functions'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.FunctionCreate.as_view(), name='add'),
    path('update/', views.update, name='update'),
]
