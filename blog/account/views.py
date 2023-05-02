from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializer import SignUpSerializer, LoginSerializer

# Create your views here.
class SignUpView(APIView):

    def post(self, request):

        try:
            data = request.data

            serializer = SignUpSerializer(data=data)

            if not serializer.is_valid():
                content = {
                    'data' : serializer.errors,
                    'message' : "Credentials not valid, Try again!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            content = {
                    'data' : {},
                    'message' : "Account Created Successfully"
                }
            return Response(content, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            content = {
                    'data' : {},
                    'message' : "Something went wrong"
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        


class LoginView(APIView):
    
    def post(self, request):

        try:
            data = request.data

            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                content = {
                    'data' : serializer.errors,
                    'message' : "Credentials not valid, Try again!"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            content = {
                    'data' : {},
                    'message' : "Something went wrong"
                }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)