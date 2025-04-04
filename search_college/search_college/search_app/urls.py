from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),  # Landing page
    path('home/', views.home, name='home'),
    path('search_colleges/', views.search_colleges, name='search_colleges'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
