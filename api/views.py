from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView, 
    RetrieveAPIView
)
from django.contrib.auth import get_user_model
from .serializers import UserSerializers, OrganizationSerializers
from rest_framework import permissions, authentication
from .permissions import UserPerm
from .authentication import TokenAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from userauth_org.models import Organizations
from django.http import JsonResponse

User = get_user_model()

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['phone'] = user.phone
        token['email'] = user.email

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
   refresh = RefreshToken.for_user(user)

   return {
     'refresh': str(refresh),
     'access': str(refresh.access_token),
   }    

class ListUsersApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

class CreateUsersApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

    def perform_create(self, serializer):
        # password = serializer.validated_data.get('password')
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            email = request.data['email']
            password = request.data['password']
            user = authenticate(email=email, password=password)
        if user:
            return Response(data = {
                "status": "success",
                "message": "Registration successful",
                "data":{
                    "accessToken": get_tokens_for_user(user)['access'],
                    "user":{
                        "userId": user.userId,
                        "firstName": user.firstname,
                        "lastName": user.lastname,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }, status=201)
        return Response(data={
            "status": "Bad request",
            "message": "Registration unsucccessful",
            "statusCode": 400
        }, status=401)
            


class RetrieveUserApiView(RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return Response(data = {
                "status": "success",
                "message": "Registration successful",
                "data":{
                    "accessToken": get_tokens_for_user(user)['access'],
                    "user":{
                        "userId": user.userId,
                        "firstName": user.firstname,
                        "lastName": user.lastname,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }, status=201)
        return Response(data={
            "status": "Bad request",
            "message": "You must login first",
            "statusCode": 400
        }, status=401)





class LoginApiView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['pasword']
        user = authenticate(email = email, password = password)
        if user:
            return Response(data = {
                "status": "success",
                "message": "Login Successful",
                "data":{
                    "accessToken": get_tokens_for_user(user)['access'],
                    "user":{
                        "userId": user.userId,
                        "firstName": user.firstname,
                        "lastName": user.lastname,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
            }, status=200)
        return Response(data={
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=401)




# class ListOrganization(ListAPIView):
#     serializer_class = OrganizationSerializers
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
#     authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

#     def get_object(self, request):
#         user = request.user
#         if user.is_authenticated:
#             return Organizations.objects.all().filter(user == user)

class ListOrganization(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            queryset = Organizations.objects.all().filter(user = user)
            serilaizer = OrganizationSerializers(queryset, many =True)
            # return JsonResponse(serilaizer.data, safe=False)
            return Response(data = {
                "status": "success",
                "message": "The organizations you belong to",
                "data":{
                    
                    "organizations": serilaizer.data
                }
            }, status=200)
        return Response(data={
            "status": "Bad request",
            "message": "You must login to see the list of organizations you belong to",
            "statusCode": 401
        }, status=401)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = OrganizationSerializers(data=request.data)
        if user.is_authenticated:
            if serializer.is_valid(raise_exception=True):
                
                obj = serializer.save()
                obj.user.add(user)
                obj.save()
                
                return Response(data = {
                    "status": "success",
                    "message": "Organization created successfully",
                    "data":{
                        "orgId": obj.id,
                        "name": obj.name,
                        "description": obj.description,
                    }
                }, status=201)
        return Response(data={
            "status": "Bad request",
            "message": "Client error",
            "statusCode": 400
        }, status=400)
            
 

class RetriveOrganizationsView(RetrieveAPIView):
    queryset = Organizations.objects.all()
    lookup_field = 'id'
    serializer_class = OrganizationSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)

        return Response(data={
            "status": "Bad request",
            "message": "You must login first",
            "statusCode": 400
        }, status=401)
    
# class CreateUsersApiView(CreateAPIView):
#     queryset = Organizations.objects.all()
#     serializer_class = OrganizationSerializers
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPerm]
#     authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             obj = self.perform_create(serializer)
#             name = request.data['name']
#             description = request.data['description']
#             return Response(data = {
#                 "status": "success",
#                 "message": "Organization created successfully",
#                 "data":{
#                     "orgId": obj.id,
#                     "name": name,
#                     "description": description,
#                 }
#             }, status=201)
#         return Response(data={
#             "status": "Bad request",
#             "message": "Client error",
#             "statusCode": 400
#         }, status=400)
