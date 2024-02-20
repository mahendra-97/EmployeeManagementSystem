from django.contrib import admin
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('employees.urls'))
    path('', lambda request: redirect('/home')),
    path('', include('employees.urls')),
]
