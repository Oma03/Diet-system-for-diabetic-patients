from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .resources import FoodListResource
from .models import Contact, DetailsN, DCalorie, FoodList, MealPlan, ContactUs


# Register your models here.
admin.site.register(Contact)
admin.site.register(ContactUs)
admin.site.register(DetailsN)
admin.site.register(DCalorie)


class FoodListResources(resources.ModelResource):
    class Meta:
        model = FoodList


class FoodListAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FoodListResource


admin.site.register(FoodList, FoodListAdmin)


class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_id', 'day', 'breakfast', 'lunch', 'snack', 'dinner', 'created_at')


admin.site.register(MealPlan, MealPlanAdmin)
