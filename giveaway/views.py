from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, ListView

# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

class AddDonation(TemplateView):
    template_name = "AddDonation.html"

class Login(TemplateView):
    template_name = "login.html"

class Register(TemplateView):
    template_name = "register.html"