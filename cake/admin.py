import json
import tablib

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportMixin, ExportMixin, ExportActionMixin, ImportExportModelAdmin

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


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        charts_data = get_charts_data(Cake)
        ingredients, ingredients_count = zip(*charts_data)

        charts_data = json.dumps(ingredients_count, cls=DjangoJSONEncoder)
        charts_labels = json.dumps(ingredients, cls=DjangoJSONEncoder)
        extra_context = extra_context or {'data': charts_data, 'labels': charts_labels}
        return super().changelist_view(request, extra_context=extra_context)


def get_charts_data(model):
    objects = model.objects.all()
    yield from (
        objects
        .values_list('level__levels_count')
        .annotate(levels=Count('id'))
        .order_by()
    )
    yield from (
        objects
        .values_list('topping__name')
        .annotate(toppings_count=Count('id'))
        .order_by()
    )
    yield from (
        objects
        .values_list('shape__figure')
        .annotate(shapes_count=Count('id'))
        .order_by()
    )
    yield from (
        objects
        .values_list('berries__name')
        .annotate(berries_count=Count('id'))
        .order_by()
    )
    yield from (
        objects
        .values_list('additional_ingredients__name')
        .annotate(additional_ingredients_count=Count('id'))
        .order_by()
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
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


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order

    def export(self, queryset=None, *args, **kwargs):
        labels, stati_count = get_order_queryser()

        data = tablib.Dataset(headers=labels)
        data.append(stati_count)

        self.after_export(queryset, data, *args, **kwargs)

        return data


def get_order_queryser():
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
        labels, stati_count = get_order_queryser()

        charts_labels = json.dumps(labels, cls=DjangoJSONEncoder)
        charts_data = json.dumps(stati_count, cls=DjangoJSONEncoder)

        extra_context = extra_context or {
            'data': charts_data,
            'labels': charts_labels,
            'extend_url': 'admin/cake/order/change_list.html',
        }

        return super().changelist_view(request, extra_context=extra_context)
