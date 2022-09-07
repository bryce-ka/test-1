# from django import urls
from django.urls import path
from . import views
from django.urls import include




urlpatterns = [
path('', views.landing_page, name = 'landing'),

# path('CreateAccount', include('Accounts.urls'), name ='CreateAccount'),
# path('base', views.base_page, name= 'base' ),
# path('home/', views.login, name = "view_board")
]