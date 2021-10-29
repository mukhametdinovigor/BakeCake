import json
import tablib

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from import_export import resources
from import_export.admin import ExportMixin
from .models import (
    Level, Shape, Topping, Berry, AdditionalIngredient, Cake, Customer, Order, STATUS
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


class CakeResource(resources.ModelResource):
    class Meta:
        model = Cake

    def export(self, queryset=None, *args, **kwargs):
        cake_stats = get_cake_stats()
        ingredients, ingredients_count = zip(*cake_stats)

        export_stats = tablib.Dataset(headers=ingredients)
        export_stats.append(ingredients_count)
        return export_stats


@admin.register(Cake)
class CakeAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CakeResource

    def changelist_view(self, request, extra_context=None):
        cake_stats = get_cake_stats()
        ingredients, ingredients_count = zip(*cake_stats)

        charts_data = json.dumps(ingredients_count, cls=DjangoJSONEncoder)
        charts_labels = json.dumps(ingredients, cls=DjangoJSONEncoder)
        extra_context = extra_context or {
            'data': charts_data,
            'labels': charts_labels,
            'extend_url': 'admin/cake/cake/change_list.html',
        }
        return super().changelist_view(request, extra_context=extra_context)


def get_cake_stats():
    cakes = Cake.objects.all()
    yield from (
        cakes
        .values_list('level__levels_count')
        .annotate(levels=Count('id'))
        .order_by()
    )
    yield from (
        cakes
        .values_list('topping__name')
        .annotate(toppings_count=Count('id'))
        .order_by()
    )
    yield from (
        cakes
        .values_list('shape__figure')
        .annotate(shapes_count=Count('id'))
        .order_by()
    )
    yield from (
        cakes
        .values_list('berries__name')
        .annotate(berries_count=Count('id'))
        .order_by()
    )
    yield from (
        cakes
        .values_list('additional_ingredients__name')
        .annotate(additional_ingredients_count=Count('id'))
        .order_by()
    )


def get_customer_stats():
    return (
        Customer.objects.annotate(date=TruncDay('date_joined'))
        .values('date')
        .annotate(y=Count('id'))
        .order_by('-date')
    )


class CustomerResources(resources.ModelResource):
    class Meta:
        model = Customer

    def export(self, queryset=None, *args, **kwargs):
        customer_stats = get_customer_stats()
        dates, customers_count = zip(*(
            date_with_stats.values() for date_with_stats in customer_stats
        ))
        labels = (date.strftime('%Y-%m-%d') for date in dates)

        export_stats = tablib.Dataset(headers=labels)
        export_stats.append(customers_count)
        return export_stats


@admin.register(Customer)
class CustomerAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CustomerResources

    def changelist_view(self, request, extra_context=None):
        chart_data = get_customer_stats()

        chart_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        total_customers = Customer.objects.count()

        extra_context = extra_context or {
            'chart_data': chart_json,
            'total_customers': total_customers,
            'extend_url': 'admin/cake/customer/change_list.html',
        }

        return super().changelist_view(request, extra_context=extra_context)


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order

    def export(self, queryset=None, *args, **kwargs):
        labels, stati_count = get_order_stats()

        export_stats = tablib.Dataset(headers=labels)
        export_stats.append(stati_count)
        return export_stats


def get_order_stats():
    order_stati = (
        Order.objects
        .values_list('status')
        .annotate(stati_count=Count('status'))
    )

    stati, stati_count = zip(*order_stati)
    labels = [dict(STATUS).get(label) for label in stati]
    return labels, stati_count


@admin.register(Order)
class OrderAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource

    def changelist_view(self, request, extra_context=None):
        labels, stati_count = get_order_stats()

        charts_labels = json.dumps(labels, cls=DjangoJSONEncoder)
        charts_data = json.dumps(stati_count, cls=DjangoJSONEncoder)

        extra_context = extra_context or {
            'data': charts_data,
            'labels': charts_labels,
            'extend_url': 'admin/cake/order/change_list.html',
        }

        return super().changelist_view(request, extra_context=extra_context)
