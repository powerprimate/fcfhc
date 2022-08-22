
from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.studentlogin, name='login'),
    path('logout/',views.studentlogout, name='logout'),
    path('register/',views.studentregister, name='register'),
    path('home/',views.home, name='home'),
]
