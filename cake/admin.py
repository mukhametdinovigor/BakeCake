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
    # def changelist_view(self, request, extra_context=None):
    #     chart_data = 
    pass

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

        aa_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        total_customers = Customer.objects.count()
        print(total_customers)
        extra_context = extra_context or {
            'chart_data': aa_json, 'total_customers': total_customers,
        }

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass