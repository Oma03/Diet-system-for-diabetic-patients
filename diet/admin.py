from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .resources import FoodListResource
from .models import Contact, DetailsN, DCalorie, FoodList


# Register your models here.
admin.site.register(Contact)
admin.site.register(DetailsN)
admin.site.register(DCalorie)


class FoodListResources(resources.ModelResource):
    class Meta:
        model = FoodList


class FoodListAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FoodListResource


admin.site.register(FoodList, FoodListAdmin)
