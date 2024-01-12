from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer

from recommendation.serializers import VaccinationsSerializer
from .models import ChildProfile, HealthProfessionalProfile,ParentProfile
from accounts.serializers import UserDisplayserializer
from rest_framework import serializers

class HealthProfessionalProfileSerializer(ModelSerializer):
    user = UserDisplayserializer(required=False)
    email = serializers.EmailField(required=False)
    phone_no = serializers.CharField(required=False)
    dob=serializers.DateField(required=False)
    class Meta:
        model = HealthProfessionalProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        print(validated_data)
        print("updating.............................")
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.profile_verification = validated_data.get('profile_verification', instance.profile_verification)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.document = validated_data.get('document', instance.document)
        instance.liscence_no = validated_data.get('liscence_no', instance.liscence_no)
        instance.yrs_of_experience = validated_data.get('yrs_of_experience', instance.yrs_of_experience)

        instance.user.date_of_birth = validated_data.get('dob', instance.user.date_of_birth)
        instance.user.email = validated_data.get('email')
        instance.user.phone_no = validated_data.get('phone_no', instance.user.phone_no)
        instance.user.save()

        instance.save()
        return instance

class ParentProfileSerializer(ModelSerializer):
    
    user = HealthProfessionalProfileSerializer(required=False)

    class Meta:
        model = ParentProfile
        fields = "__all__"

class ChildProfileSerializer(ModelSerializer):

    user = ParentProfileSerializer(required=False)

    class Meta:
        model = ChildProfile 
        fields = "__all__"

class ChildProfileDisplaySerializer(ModelSerializer):
    past_vaccinations=VaccinationsSerializer(many=True,required=False)
    class Meta:
        model = ChildProfile 
        fields = ["id","full_name", "age","age_in_months","age_in_days","age_in_weeks","date_of_birth","user","past_vaccinations"]