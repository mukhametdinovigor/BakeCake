from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import ConstructCakeForm, AdvancedInfoForm
from .forms import UserCreationWithEmailForm, UserLoginForm
from .models import *


LETTERING_PRICE = 500


def get_price(ingredients):
    price = 0
    for ingredient in ingredients:
        price += float(ingredient.split('+')[1].strip())
    return price


def index(request):
    request.session.pop('cake_price', None)
    form = ConstructCakeForm()
    return render(request, 'index.html', {'form': form})


def advanced_info(request):
    advanced_form = AdvancedInfoForm()
    if not request.session.session_key:
        request.session.save()
    try:
        cake_price = request.session['cake_price']
        return render(request, 'adv_order_info.html', {'form': advanced_form,
                                                       'cake_price': cake_price,
                                                       })
    except KeyError:
        cake_form = ConstructCakeForm(request.POST)
        cake_price = 0
        if cake_form.is_valid():
            level_price = float(cake_form.cleaned_data.get('levels').split('+')[1].strip())
            shape_price = float(cake_form.cleaned_data.get('shapes').split('+')[1].strip())
            toppings_price = float(cake_form.cleaned_data.get('toppings').split('+')[1].strip())
            berries_attrs = cake_form.cleaned_data.get('berries')
            berries_price = get_price(berries_attrs)
            decor_attrs = cake_form.cleaned_data.get('decor')
            decor_price = get_price(decor_attrs)
            lettering_price = 0
            if cake_form.cleaned_data['lettering']:
                lettering_price = LETTERING_PRICE
            cake_price = sum((level_price, shape_price, toppings_price, berries_price, decor_price, lettering_price))
            request.session['cake_cleaned_data'] = cake_form.cleaned_data
            request.session['cake_price'] = cake_price
        return render(request, 'adv_order_info.html', {'form': advanced_form,
                                                       'cake_price': cake_price,
                                                       })


def confirm(request):
    cake_cleaned_data = request.session['cake_cleaned_data']
    # cake, created = Cake.objects.get_or_create(
    #     level=level,
    #     shape=shape,
    #     topping=topping,
    #     berries__in=berrieses,
    #     defaults={'berries': berrieses},
    #     additional_ingredients__in=additionals_ingredients,
    #     defaults={'additional_ingredients': additionals_ingredients},
    #     lettering=lettering
    #     lettering_cost=
    # )

    additional_form = AdvancedInfoForm(request.POST)
    # if additional_form.is_valid():
    #     delivered_at = additional_form.cleaned_data.get('delivered_at')
    #     delivery_time = additional_form.cleaned_data.get('delivery_time')
    #     comment = additional_form.cleaned_data.get('order_comment')
    #     order, created = Order.objects.get_or_create(
    #         delivered_at=delivered_at,
    #         delivery_time=delivery_time,
    #         comment=comment,
    #         total_price=1,
    #         customer=1,
    #         cake=1,

        # )
    return render(request, 'confirmation.html')


def account(request):
    return render(request, 'account.html')


class LoginUserView(LoginView):
    def get_success_url(self):
        if self.request.session.get('cake_cleaned_data'):
            return reverse('advanced_info')
        else:
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
        if request.session.get('cake_cleaned_data'):
            return redirect('advanced_info')
        else:
            return redirect('index')
