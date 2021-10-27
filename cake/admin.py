from django.contrib import admin

from .models import (
    Level, Shape, Topping, Berry, AdditionalIngredient, Cake, Customer, Order
)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass


@admin.register(Topping)
class ToppingAdmin(admin.ModelAdmin):
    pass


@admin.register(Berry)
class BerryAdmin(admin.ModelAdmin):
    pass


@admin.register(AdditionalIngredient)
class AdditionalIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    # inlines = [
    #     LevelInline,
    #     ShapeInline,
    #     ToppingInline,
    #     BerryInline,
    #     AdditionalIngredientInline,
    # ]
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass