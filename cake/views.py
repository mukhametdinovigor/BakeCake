from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import ConstructCakeForm, AdvancedInfoForm
from .forms import UserCreationWithEmailForm


LETTERING_PRICE = 500


def get_price(ingredients, prices):
    price = 0
    for ingredient in ingredients:
        price += prices[ingredient]
    return price


def index(request):
    form = ConstructCakeForm()
    return render(request, 'index.html', {'form': form})


def advanced_info(request):
    cake_form = ConstructCakeForm(request.POST)
    cake_price = 0
    if cake_form.is_valid():
        level_price = float(cake_form.cleaned_data.get('levels'))
        shape_price = float(cake_form.cleaned_data.get('shapes'))
        toppings_price = float(cake_form.cleaned_data.get('toppings'))
        berries_price = sum(map(float, cake_form.cleaned_data.get('berries')))
        decor_price = sum(map(float, cake_form.cleaned_data.get('decor')))
        lettering_price = 0
        if cake_form.cleaned_data['lettering']:
            lettering_price = LETTERING_PRICE

        cake_price = sum((level_price, shape_price, toppings_price, berries_price, decor_price, lettering_price))

    advanced_form = AdvancedInfoForm()

    return render(request, 'adv_order_info.html', {'form': advanced_form, 'cake_price': cake_price})


class LoginUserView(LoginView):
    def get_success_url(self):
        return reverse('index')


class SignupUserView(View):

    def get(self, request):
        form = UserCreationWithEmailForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationWithEmailForm(request.POST)
        if not form.is_valid():
            return render(request, 'registration/signup.html', {'form': form})
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')
