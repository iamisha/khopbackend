from datetime import datetime, timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Nutrition, Vaccinations, RecommendedNutritionAndVaccination
from .serializers import  RecommenedNutritionAndVaccinationSerializer
from rest_framework import status

@api_view(['GET'])
def index(request):
    return render(request, 'vaccination.html')

@api_view(['GET'])
def nutrition(request):
    return render(request, 'nutritions.html')

@api_view(['GET'])
def create_all_recommendation(request):
    try:
        age = request.query_params.get('age')
        age_unit = request.query_params.get('age_unit')

        suitable_nutritions = Nutrition.objects.filter(
            min_age__lte=age, max_age__gte=age, age_unit=age_unit
        )
        suitable_vaccinations = Vaccinations.objects.filter(
            min_age__lte=age, max_age__gte=age, age_unit=age_unit
        )

        recommendation = RecommendedNutritionAndVaccination.objects.filter(
                min_age__lte=age, max_age__gte=age, age_unit=age_unit
                ).first()

        if recommendation:
            current_nutritions = set(recommendation.nutrition.all())
            current_vaccinations = set(recommendation.vaccination.all())
            vaccine_min_age = min([vaccine.min_age for vaccine in suitable_vaccinations])
            vaccine_max_age = max([vaccine.max_age for vaccine in suitable_vaccinations])
            nutrition_min_age = min([nutrition.min_age for nutrition in suitable_nutritions])
            nutrition_max_age = max([nutrition.max_age for nutrition in suitable_nutritions])


            if current_nutritions != suitable_nutritions or current_vaccinations != suitable_vaccinations:
                recommendation.nutrition.set(suitable_nutritions)
                recommendation.vaccination.set(suitable_vaccinations)
                recommendation.min_age=min(vaccine_min_age,nutrition_min_age)
                recommendation.max_age=max(vaccine_max_age,nutrition_max_age)
                recommendation.save()
        else:
            recommendation = RecommendedNutritionAndVaccination.objects.filter(
                min_age__lte=age, max_age__gte=age, age_unit=age_unit
                ).first()
            recommendation.nutrition.set(suitable_nutritions)
            recommendation.vaccination.set(suitable_vaccinations)
            recommendation.save()

        serializer = RecommenedNutritionAndVaccinationSerializer(recommendation)
        return Response(serializer.data)
    
    except Exception as e:
        print(e)
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
    


