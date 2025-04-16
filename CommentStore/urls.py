"""
URL configuration for CommentStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from request import views
from register import views as register_views

urlpatterns = [

    path('home/', views.home, name="home"),
    path("register/", register_views.register_user, name="register"),
    path("login/", register_views.login_user, name="login"),
    path("logout/", register_views.logout_user, name="logout"),
    path('request/', include('request.urls')),
    path('moneytransfer/', include('transactions.urls')),
    path('admin/', admin.site.urls),
    path('conversion-auth/', include('rest_framework.urls')),
    path('conversion/', include('conversion.urls')),path('conversion/', include('conversion.urls')),
]