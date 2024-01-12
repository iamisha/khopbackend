from django.urls import path
from .views import create_all_recommendation,index,nutrition
urlpatterns = [
    path('', create_all_recommendation, name="create_all_recommendations"),
    path('index/', index, name="index"  ),
    path('nutrition/', nutrition, name="nutrition"  )
]
   
