from rest_framework.serializers import ModelSerializer
from .models import Nutrition, Vaccinations, PlacesOfVaccination, RecommendedNutritionAndVaccination

class NutritionSerializer(ModelSerializer):
    class Meta:
        model = Nutrition
        fields = "__all__"



class VaccinationsSerializer(ModelSerializer):
    class Meta:
        model = Vaccinations
        fields = "__all__"


class PlacesOfVaccinationSerializer(ModelSerializer):
    vaccine=VaccinationsSerializer(many=True)
    class Meta:
        model = PlacesOfVaccination
        fields = "__all__"



class RecommenedNutritionAndVaccinationSerializer(ModelSerializer):
    nutrition=NutritionSerializer(many=True)
    vaccination=VaccinationsSerializer(many=True)
    class Meta:
        model = RecommendedNutritionAndVaccination
        fields = "__all__"