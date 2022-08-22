from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.adminlogin, name='adminlogin'),
    path('database/',views.admindatabase, name='database'),
    path('logout/',views.adminlogout, name='adminlogout'),
    path('creation/',views.admincreateuser, name='create'),
    path('updation/<id>',views.adminupdation, name='update'),
    path('deletion/<id>',views.admindelete, name='delete'),
]
