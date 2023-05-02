from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignUpSerializer(serializers.Serializer):
    fname = serializers.CharField(max_length=100)
    lname = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField()

    def validate(self, data):
        
        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Username is Taken')
        
        return data
    
    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name = validated_data['fname'],
            last_name = validated_data['lname']
        )

        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField()

    def validate(self, data):
        
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Account does not exists.')
        
        return data
    
    def get_jwt_token(self, data):

        user = authenticate(username=data['username'],password=data['password'])

        if not user : 
            return {'message' : "invalid credetails", 'data' : {}}
        
        refresh = RefreshToken.for_user(user)

        content = {
            'token' : str(refresh),
            'access' : str(refresh.access_token)
        }

        return {'message' : "Logged In", 'data' : content}


