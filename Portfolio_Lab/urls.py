"""Portfolio_Lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from giveaway.views import MainView, AddDonation, Register, Login, AddDonationComplete, ProfileView, ArchiveDonation, ProfileUpdateView

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    path("", MainView.as_view(), name="main"),
    path("add-donation/", AddDonation.as_view(), name="add-donation"),
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="main"), name="logout",),
    path('confirmation/', AddDonationComplete.as_view(), name='confirmation'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileUpdateView.as_view(), name='edit-profile'),
    path('archive/<int:pk>/', ArchiveDonation.as_view(), name='archive-donation'),
    path('change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html',
            success_url = '/'
        ),
        name='change-password'),
]