from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView, CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate  
from django.contrib.auth.mixins import (
    PermissionRequiredMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)  
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.db.models import Sum, Count, Q
from django.urls import reverse_lazy
from .forms import DonationForm, UserSignUpForm, EditUserForm
from .models import Donation, Category, Institution, User
import json
from io import StringIO
import re

# Create your views here.

class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = {}
        all_bags = Donation.objects.all().aggregate(Sum('quantity'))
        all_supported_orgs = Donation.objects.count()
        all_orgs_type_0 = Institution.objects.filter(type=0)
        all_orgs_type_1 = Institution.objects.filter(type=1)
        all_orgs_type_2 = Institution.objects.filter(type=2)

        context["all_bags"] = all_bags['quantity__sum']
        context["all_supported_orgs"] = all_supported_orgs
        context["all_orgs_type_0"] = all_orgs_type_0
        context["all_orgs_type_1"] = all_orgs_type_1
        context["all_orgs_type_2"] = all_orgs_type_2
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_donations"] = Donation.objects.filter(Q(user=self.request.user) & Q(is_taken=False))
        context["user_archived_donations"] = Donation.objects.filter(Q(user=self.request.user) & Q(is_taken=True))
        return context

class ArchiveDonation(UpdateView):
    success_url = reverse_lazy("profile")
    model = Donation
    fields = ["is_taken"]

    def get(self, request, *args, **kwargs):
        if self.request.method == "GET":
            arch_donation = get_object_or_404(Donation, pk=kwargs['pk'])
            print(arch_donation.is_taken)
            if arch_donation is None:
                return 'Obiekt nieistnieje'
            elif arch_donation.is_taken == True:
                arch_donation.is_taken = False
                arch_donation.save()
            elif arch_donation.is_taken == False:
                arch_donation.is_taken = True
                arch_donation.save()
            return redirect('profile')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditUserForm
    success_url = "main"
    login_url = 'login'
    template_name_suffix = "_update_form"

    def post(self, request, *args, **kwargs):
        form = EditUserForm(request.POST)
        user_ = request.user
        if form.is_valid():
            user_new_info = form.save(commit=False)
            user_auth = authenticate(username=user_.email, password=form.cleaned_data['password'])
            if user_auth is not None:
                user_.first_name = user_new_info.first_name
                user_.last_name = user_new_info.last_name
                user_.save()
                return redirect('main')
        else:
            return render(request, 'index.html', {'form': form})   


class AddDonation(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("main")
    template_name = "AddDonation.html"
    # form_class = Donation
    # fields = '__all__'

    def get_context_data(self):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {"categories": categories, 'institutions': institutions}
        return ctx

    def post(self, request, *args, **kwargs):
        form = DonationForm(request.POST)
        print('inside post')
        print(form)
        if form.is_valid():
            print('____form_valid____')
            form_data_dict = {}
            form_data_list = json.loads(form)
            for field in form_data_list:
                form_data_dict[field["name"]] = field["value"]
            return form_data_dict

            # quantity = request.POST.get('quantity')
            # categories = request.POST.get('categories')
            # # categories = json.dumps(categories)
            # institution = request.POST.get('organization')
            # address = request.POST.get('address')
            # city = request.POST.get('city')
            # postcode = request.POST.get('postcode')
            # phone = request.POST.get('phone')
            # pick_up_date = request.POST.get('data')
            # pick_up_time = request.POST.get('time')
            # pick_up_comment = request.POST.get('more_info')

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
            # io = StringIO(categories)
            # categories = json.load(categories)
            # categories = re.findall("\d+", categories)
            for cat_no in categories:
                cat_obj = Category.objects.get(pk=cat_no)
                donation_current.categories.add(cat_obj)
            return redirect('confirmation')
        else: 
            print('__Form invalid__')
            print(form.errors)
            return HttpResponse(json.dumps({'message':'not ok'}))
        return render(request, "AddDonation.html")            

class Login(LoginView):
    template_name = "login.html"
    success_url = reverse_lazy('main')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return redirect('register')


class Register(FormView):
    template_name = "register.html"
    form_class = UserSignUpForm
    success_url = reverse_lazy("main")

    def post(self, request, *args, **kwargs):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            print('Valid')
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('main')
        else:
            print('Invalid')
            print(form.is_valid())  #form contains data and errors
            print(form.errors)
            form = UserSignUpForm()
        return render(request, 'register.html', {"form": form})

class AddDonationComplete(TemplateView):
    template_name = 'form-confirmation.html'