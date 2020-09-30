from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.contrib.auth.views import LoginView    
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from django.urls import reverse_lazy

from .models import Donation, Category, Institution
# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

class AddDonation(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("main")
    fields = '__all__'
    template_name = "AddDonation.html"
    model = Donation

    def get_context_data(self):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {"categories": categories, 'institutions': institutions}
        return ctx

class Login(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('main')

class Register(TemplateView):
    template_name = "register.html"

class AddDonationComplete(TemplateView):
    template_name = 'form-confirmation.html'