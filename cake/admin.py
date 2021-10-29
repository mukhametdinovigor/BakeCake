import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay

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
    def changelist_view(self, request, extra_context=None):
        cakes = Cake.objects.all()
        levels_chart_data = (
            cakes
            .values('level__levels_count')
            .annotate(levels=Count('id'))
            .order_by()
        )
        toppings_chart_data = (
            cakes
            .values_list('topping__name')
            .annotate(toppings_count=Count('id'))
            .order_by()
        )
        shapes_chart_data = (
            cakes
            .values('shape__figure')
            .annotate(shapes_count=Count('id'))
            .order_by()
        )
        berries_chart_data = (
            cakes
            .values('berries__name')
            .annotate(berries_count=Count('id'))
            .order_by()
        )
        additional_ingredients_chart_data = (
            cakes
            .values('additional_ingredients__name')
            .annotate(additional_ingredients_count=Count('id'))
            .order_by()
        )

        print(shapes_chart_data)
        shapes = json.dumps(list(shapes_chart_data), cls=DjangoJSONEncoder)
        print(shapes)
        # extra_context = extra_context or {'data': shapes}
        # print(levels_chart_data)
        # print(toppings_chart_data)
        # print(shapes_chart_data)
        # print(berries_chart_data)
        # print(additional_ingredients_chart_data)
        # print(dict(toppings_chart_data).values())
        labels = json.dumps(list((dict(toppings_chart_data).keys())), cls=DjangoJSONEncoder)

        chart_json = json.dumps(list((dict(toppings_chart_data).values())), cls=DjangoJSONEncoder)
        extra_context = extra_context or {'data': chart_json, 'labels': labels}
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # pass
    def changelist_view(self, request, extra_context=None):
        chart_data = (
            Customer.objects.annotate(date=TruncDay('date_joined'))
            .values('date')
            .annotate(y=Count('id'))
            .order_by('-date')
        )

        chart_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        total_customers = Customer.objects.count()

        extra_context = extra_context or {
            'chart_data': chart_json, 'total_customers': total_customers,
        }

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass