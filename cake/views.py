from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import ConstructCakeForm, AdvancedInfoForm
from .forms import UserCreationWithEmailForm
from .models import Level, Shape, Topping, Berry, AdditionalIngredient

LETTERING_PRICE = 500

# LEVEL_PRICES = {
#     'level1': Level.objects.get(levels_count=1).price,
#     'level2': Level.objects.get(levels_count=2).price,
#     'level3': Level.objects.get(levels_count=3).price,
# }

# SHAPE_PRICES = {
#     'circle': Shape.objects.get(figure='Круг').price,
#     'square': Shape.objects.get(figure='Квадрат').price,
#     'rectangle': Shape.objects.get(figure='Прямоугольник').price
# }

# TOPPING_PRICES = {
#     'without_toppings': Topping.objects.get(name='Без топпинга').price,
#     'white_souse': Topping.objects.get(name='Белый соус').price,
#     'caramel_syrup': Topping.objects.get(name='Карамельный сироп').price,
#     'maple_syrup': Topping.objects.get(name='Кленовый сироп').price,
#     'strawberry_syrup': Topping.objects.get(name='Клубничный сироп').price,
#     'blueberry_syrup': Topping.objects.get(name='Черничный сироп').price,
#     'milk_choco': Topping.objects.get(name='Молочный шоколад').price,
# }

# BERRY_PRICES = {
#     'blackberry': Berry.objects.get(name='Ежевика').price,
#     'raspberry': Berry.objects.get(name='Малина').price,
#     'blueberry': Berry.objects.get(name='Голубика').price,
#     'Strawberry': Berry.objects.get(name='Клубника').price,
# }

# DECOR_PRICES = {
#     'without_decor': AdditionalIngredient.objects.get(name='Без декора').price,
#     'pistachio': AdditionalIngredient.objects.get(name='Фисташки').price,
#     'meringue': AdditionalIngredient.objects.get(name='Безе').price,
#     'funduk': AdditionalIngredient.objects.get(name='Фундук').price,
#     'pecan': AdditionalIngredient.objects.get(name='Пекан').price,
#     'Marshmallow': AdditionalIngredient.objects.get(name='Маршмеллоу').price,
#     'marzipan': AdditionalIngredient.objects.get(name='Марципан').price,
# }


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
        level_price = LEVEL_PRICES[cake_form.cleaned_data['levels']]
        shape_price = SHAPE_PRICES[cake_form.cleaned_data['level_shapes']]
        toppings_price = TOPPING_PRICES[cake_form.cleaned_data['toppings']]
        berries = cake_form.cleaned_data['berries']
        berries_price = get_price(berries, BERRY_PRICES)
        decor = cake_form.cleaned_data['decor']
        decor_price = get_price(decor, DECOR_PRICES)
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
