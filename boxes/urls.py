from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'boxes'

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile_page, name='user_profile'),
    path('random_page', views.random_page, name='losuj')
]






