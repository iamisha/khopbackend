from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Users
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
# Create your views here.



@api_view(["POST"])
def sign_up(request):
    data=request.data
    print(data)
    serializer=UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data":serializer.data,"msg":"User Created Successfully","success":True},status=status.HTTP_201_CREATED)
    return Response({"msg":"User Not Created","success":False,"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def sign_in(request):
    data=request.data
    serializer=UserLoginSerializer(data=data)
    if serializer.is_valid():
        email=serializer.validated_data["email"]
        password=serializer.validated_data["password"]
        user=authenticate(email=email,password=password)
        print(user,"*****************")
        if user is not None:
            token,created=Token.objects.get_or_create(user=user)
            # json.dumps({"token":token.key})
            return Response({"data":token.key,"msg":"User Logged In Successfully","success":True},status=status.HTTP_200_OK)
    
    return Response({"msg":"User Not Logged In","success":False,"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sign_out(request):
    request.user.auth_token.delete()
    return Response({"msg":"User Logged Out Successfully","success":True},status=status.HTTP_200_OK)


