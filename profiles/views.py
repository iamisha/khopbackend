from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from .models import ChildProfile, HealthProfessionalProfile,ParentProfile
from .serializers import ChildProfileDisplaySerializer, ChildProfileSerializer, HealthProfessionalProfileSerializer,ParentProfileSerializer
# Create your views here.


class HealthProfessionalProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        profile,created=HealthProfessionalProfile.objects.get_or_create(user=request.user,)
        serializer=HealthProfessionalProfileSerializer(profile,context={'request': request})
        return Response({"data":serializer.data,"msg":"found profile for user","success":True},status=status.HTTP_201_CREATED)
    
    def put(self, request):
        print(request.data)
        profile = HealthProfessionalProfile.objects.get(user=request.user)
        serializer = HealthProfessionalProfileSerializer(profile, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "Profile updated successfully", "success": True}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)



    




class ParentProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id=None):
        print(id,"*************")
        if id:
            profile = ParentProfile.objects.get(id=id, user__user=request.user)
            serializer = ParentProfileSerializer(profile, context={'request': request})
            return Response({"data": serializer.data, "msg": "found profile for user", "success": True}, status=status.HTTP_200_OK)


        doctor=HealthProfessionalProfile.objects.prefetch_related("parent_profile").get(user=request.user)
        profiles=doctor.parent_profile.all()

        if not profiles:
            return Response({"data":None,"msg":"No profile found for user","success":False},status=status.HTTP_404_NOT_FOUND)
        
        serializer=ParentProfileSerializer(profiles,context={'request': request},many=True)
        return Response({"data":serializer.data,"msg":"found profile for user","success":True},status=status.HTTP_200_OK)
        
    def post(self, request): 
        health_professional_profile, created = HealthProfessionalProfile.objects.get_or_create(user=request.user)
        serializer = ParentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=health_professional_profile)
            return Response({"data": serializer.data, "msg": "Profile updated successfully", "success": True}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, id=None):
        try:
            if id:
                profile = ParentProfile.objects.get(user__user=request.user, id=id)
        except ParentProfile.DoesNotExist:
            return Response({"error": "ParentProfile not found", "success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParentProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "msg": "Profile updated successfully", "success": True}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id:int):
        profile = HealthProfessionalProfile.objects.prefetch_related("parent_profile").get(user=request.user)
        parents_profile = profile.parent_profile.all()
        if id in [p.id for p in parents_profile]:
            profile_to_be_deleted = ParentProfile.objects.get(id=id)
            profile_to_be_deleted.delete()
            return Response({"data": None, "success": True, "msg": "Parent profile deleted successfully!"},status=status.HTTP_204_NO_CONTENT)
        return Response({"data": None, "success": False, "msg": "Unauthorized access!"}, status=status.HTTP_400_BAD_REQUEST)
        
    # def delete(self, request,id:int):
    #     parent_profile = ParentProfile.objects.get(id=id)
    #     parent_profile.delete()
    #     return Response({"data": None, "success": True, "msg": "Parent profile deleted successfully!"},status=status.HTTP_204_NO_CONTENT)

class ChildProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        pk = request.query_params.get("pk") 
        id = request.query_params.get("id")
        if not pk:
            if id and id != "null":
                profiles = ParentProfile.objects.prefetch_related("child_profile").get(user__user=request.user,id=id)
                children_profiles = profiles.child_profile.all()
                serializer = ChildProfileDisplaySerializer(children_profiles, many=True)
                return Response({"data": serializer.data, "success": True}, status=status.HTTP_200_OK)
            return Response({"data": None, "success": False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                child = ChildProfile.objects.get(user__user__user=request.user,pk=pk)
            except Exception as e:
                print(e)
            serializer = ChildProfileDisplaySerializer(child)
            return Response({"data": serializer.data, "success": True}, status=status.HTTP_200_OK)

    def post(self, request):
        pk = request.query_params.get("pk")
        profile = ParentProfile.objects.get(user__user=request.user,pk=pk)
        print(profile)
        serializer = ChildProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=profile)
            return Response({"data": serializer.data, "success": True, "msg": "Child profile created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            vaccine = None
            pk = request.query_params.get("pk")
            vaccine_id = request.data.get("vaccine_id", None)

            profile = ChildProfile.objects.get(user__user__user=request.user, pk=pk)
            if vaccine_id:
                vaccine = Vaccinations.objects.get(id=vaccine_id)
            print(vaccine_id,vaccine)
        except ChildProfile.DoesNotExist:
            return Response({"error": "ChildProfile not found", "success": False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChildProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            if vaccine:
                profile.past_vaccinations.add(vaccine)  
            return Response({"data": serializer.data, "msg": "Profile updated successfully", "success": True}, status=status.HTTP_200_OK)
        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            pk = request.query_params.get("pk")
            profile = ChildProfile.objects.get(user__user__user=request.user, pk=pk)    
            if profile:
                profile.delete()
                return Response({"data": None, "success": True, "msg": "Child profile deleted successfully!"},status=status.HTTP_204_NO_CONTENT)
            return Response({"data": None, "success": False, "msg": "Unauthorized access!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)  
            return Response({"data": str(e), "success": False, "msg": "error!"}, status=status.HTTP_400_BAD_REQUEST)

        