from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import ConstructCakeForm, AdvancedInfoForm
from .forms import UserCreationWithEmailForm
from .models import *
from environs import Env

from datetime import timedelta


env = Env()
env.read_env()

LETTERING_PRICE = env.float('LETTERING_PRICE')


def get_price(ingredients):
    price = 0
    for ingredient in ingredients:
        price += float(ingredient.split('+')[1].strip())
    return price


def get_ids_from_cake_order(elements):
    objects = []
    for element in elements:
        obj_id = int(element.split('+')[0].strip())
        objects.append(obj_id)
    return objects


def get_order_objects(cake_cleaned_data):
    level_id = int(cake_cleaned_data['levels'].split('+')[0].strip())
    level = get_object_or_404(Level, id=level_id)
    shape_id = int(cake_cleaned_data['shapes'].split('+')[0].strip())
    shape = get_object_or_404(Shape, id=shape_id)
    topping_id = int(cake_cleaned_data['toppings'].split('+')[0].strip())
    topping = get_object_or_404(Topping, id=topping_id)
    berry_ids = get_ids_from_cake_order(cake_cleaned_data['berries'])
    decor_ids = get_ids_from_cake_order(cake_cleaned_data['decor'])
    lettering = cake_cleaned_data['lettering']
    return level, shape, topping, berry_ids, decor_ids, lettering


def index(request):
    request.session.pop('cake_price', None)
    form = ConstructCakeForm()
    return render(request, 'index.html', {'form': form})


def advanced_info(request):
    if request.user.pk:
        customer = get_object_or_404(Customer, id=request.user.id)
        advanced_form = AdvancedInfoForm(initial={'address': customer.address})
    else:
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
    global LETTERING_PRICE
    cake_price = request.session.get('cake_price')
    surcharge = 0
    cake_cleaned_data = request.session['cake_cleaned_data']
    level, shape, topping, berry_ids, decor_ids, lettering = get_order_objects(cake_cleaned_data)
    if not lettering:
        LETTERING_PRICE = 0
    cake, created = Cake.objects.get_or_create(
        level=level,
        shape=shape,
        topping=topping,
        lettering=lettering,
        lettering_cost=LETTERING_PRICE
    )
    for berry_id in berry_ids:
        cake.berries.add(berry_id)
    for decor_id in decor_ids:
        cake.additional_ingredients.add(decor_id)
    cake.save()

    additional_form = AdvancedInfoForm(request.POST)
    customer = get_object_or_404(Customer, id=request.user.id)
    if additional_form.is_valid():
        delivery_time = additional_form.cleaned_data.get('delivery_time')
        comment = additional_form.cleaned_data.get('order_comment')
        address = additional_form.cleaned_data.get('address')
        order, created = Order.objects.get_or_create(
            delivery_time=delivery_time,
            comment=comment,
            total_price=request.session.get('cake_price'),
            customer=customer,
            cake=cake
        )
        customer.address = address
        customer.save()
        if delivery_time - order.created_at < timedelta(1):
            surcharge = round(cake_price * 0.2, 2)
        return render(request, 'confirmation.html', {'cake_price': cake_price,
                                                     'surcharge': surcharge
                                                     })
    else:
        return render(request, 'adv_order_info.html', {'form': additional_form,
                                                       'cake_price': cake_price,
                                                       })


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
