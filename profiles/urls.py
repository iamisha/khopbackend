from django.urls import path
from .views import  ChildProfileView, HealthProfessionalProfileView,ParentProfileView
urlpatterns = [
    path("health-professional/",HealthProfessionalProfileView.as_view(),name="health-professional"),
    path("parents/<int:id>",ParentProfileView.as_view(),name="parents"),
    path("parents/",ParentProfileView.as_view(),name="parents_all"),  
    path("childs/",ChildProfileView.as_view(),name="childs_all"),

]
