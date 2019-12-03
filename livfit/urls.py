"""LivFit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('Home.urls'), name='home-index'),
    path('user/', include('Users.urls'), name='user-index'),
    path('user/', include('Users.urls'), name='register'),
    path('user/', include('Users.urls'), name='login'),
    path('user/', include('Users.urls'), name='logout'),
    path('user/', include('Users.urls'), name='profile'),
    path('dietplan/', include('Dietplan.urls'), name='caloriescalculator'),
    path('dietplan/', include('Dietplan.urls'), name='get-dietplan'),
    path('dietplan/', include('Dietplan.urls'), name='ingredient'),
    path('dietplan/', include('Dietplan.urls'), name='meal'),
    path('dietplan/', include('Dietplan.urls'), name='vegdietplan'),
    path('dietplan/', include('Dietplan.urls'), name='non-vegdietplan'),
    path('admin/', admin.site.urls),
]
