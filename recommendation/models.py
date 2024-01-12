from django.db import models

# Create your models here.

class Nutrition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="nutrition_images/")
    url_for_image = models.URLField(verbose_name="only for development purposes",default="")
    age_unit = models.CharField(max_length=10, choices=[('days', 'days'),('weeks', 'weeks'),('months', 'months'), ('years', 'years')],default="days")
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.name

class Vaccinations(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="vaccination_images/")
    url_for_image = models.URLField(verbose_name="only for development purposes",default="")
    age_unit = models.CharField(max_length=10, choices=[('days', 'days'),('weeks', 'weeks'),('months', 'months'), ('years', 'years')],default="days")
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    




class PlacesOfVaccination(models.Model):
    vaccine=models.ManyToManyField(Vaccinations,related_name="places")
    address=models.TextField()
    map_url=models.URLField()
    starting_time=models.TimeField(default="23:59:59")
    ending_time=models.TimeField(default="23:59:59")
    vaccination_date=models.DateField(default="2023-12-31")

    def __str__(self) -> str:
        return self.address.split(",")[0]




class RecommendedNutritionAndVaccination(models.Model):
    nutrition=models.ManyToManyField(Nutrition,related_name="vaccination")
    vaccination=models.ManyToManyField(Vaccinations,related_name="nutrition")
    age_unit = models.CharField(max_length=10, choices=[('days', 'days'),('weeks', 'weeks'),('months', 'months'), ('years', 'years')],default="days")
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f" for childs of age {self.min_age} {self.age_unit} to {self.max_age} {self.age_unit}"