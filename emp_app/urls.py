from django.contrib import admin
from django.urls import path
from . import views

from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('list',views.list,name="list"),
    path('add',views.add,name="add"),
    path('search', views.search, name='search'),
    path('delete/<int:employee_id>', views.delete, name='delete'),
    path('<int:employee_id>',views.update, name='update')
]