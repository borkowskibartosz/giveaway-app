from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, CreateView, ListView
from django.contrib.auth.views import LoginView    
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import JsonResponse

from django.urls import reverse_lazy
from .forms import DonationForm
from .models import Donation, Category, Institution
import json
from io import StringIO
import re

# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

class AddDonation(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("main")
    template_name = "AddDonation.html"
    form_class = Donation
    fields = '__all__'

    def get_context_data(self):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {"categories": categories, 'institutions': institutions}
        return ctx

    def post(self, request, *args, **kwargs):
        if self.request.method == "POST" and self.request.is_ajax():
            # form = DonationForm(request.POST)
            print('###### Data Recieved ######')
            # if form.is_valid():
            # print('Form valid')
            # donation = form.save(commit=False)

            quantity = request.POST.get('quantity')
            categories = request.POST.get('categories')
            categories = json.dumps(categories)
            institution = request.POST.get('organization')
            address = request.POST.get('address')
            city = request.POST.get('city')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            pick_up_date = request.POST.get('data')
            pick_up_time = request.POST.get('time')
            pick_up_comment = request.POST.get('more_info')
            user = request.user

            print(f'Ilość {quantity}')
            print(f'{categories}')
            print(f'Organizacja {institution}')
            print(f'Adres: {address}')
            print(f'Miasto: {city}')
            print(f'Kod pocztowy {postcode}')
            print(f'Telefon: {phone}')
            print(f'Data: {pick_up_date}')
            print(f'Godzina: {pick_up_time}')
            print(f'Komentarze: {pick_up_comment}')
            donation_current = Donation.objects.create(
                quantity = quantity,
                institution = Institution.objects.get(pk=institution),
                address = address,
                city = city,
                zip_code = postcode,
                phone = phone,
                pick_up_date = pick_up_date,
                pick_up_time = pick_up_time,
                pick_up_comment = pick_up_comment,
                user = request.user,
                )
            io = StringIO(categories)
            categories = json.load(io)
            # categories = categories[1:-1].split(",")
            categories = re.findall("\d+", categories)
            for cat_no in categories:
                cat_obj = Category.objects.get(pk=cat_no)
                donation_current.categories.add(cat_obj)
            # donation.save()
            return redirect('confirmation')
            
            
        return render(request, "AddDonation.html")            

class Login(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('main')

class Register(TemplateView):
    template_name = "register.html"

class AddDonationComplete(TemplateView):
    template_name = 'form-confirmation.html'