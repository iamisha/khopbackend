from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Nutrition)
admin.site.register(models.Vaccinations)
admin.site.register(models.PlacesOfVaccination)
admin.site.register(models.RecommendedNutritionAndVaccination)