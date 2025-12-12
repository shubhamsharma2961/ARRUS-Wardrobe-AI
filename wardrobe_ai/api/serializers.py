from rest_framework import serializers
from .models import Wardrobe, Occasion, UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username= serializers.CharField(required=True, write_only= True )
    email= serializers.EmailField(required=True, validators= [UniqueValidator(queryset=User.objects.all())])
    password= serializers.CharField(write_only= True, required= False, validators= [validate_password])
    password2= serializers.CharField(write_only= True, required= True)

    class Meta:
        model = User
        fields= ('username', 'email', 'password', 'password2')

    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match.")

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already taken')
        return data
    
    def create(self, validated_data):
        print(validated_data)
        user= User.objects.create(username= validated_data['username'], email= validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField(write_only= True)
    password2 = serializers.CharField(write_only= True)
    refresh_token= serializers.CharField(read_only= True)
    access_token= serializers.CharField(read_only= True)

    def validate(self, data):
        username= data.get('username')
        password= data.get('password')
        password2= data.get('password2')
        
        user = authenticate(username= username, password= password, password2= password2)
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match.")
        
        if user is None:
            raise serializers.ValidationError('Invalid Login Credentials.')
        
        refresh= RefreshToken.for_user(user)
        data['refresh_token']= str(refresh)
        data['access_token']= str(refresh.access_token)
        return data


'''class CustomTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials.')

        refresh = RefreshToken.for_user(user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)

        return data'''

class WardrobeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wardrobe
        fields = ['id', 'user', 'image', 'category', 'color', 'formality']

class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'name', 'description']
        Occasion.objects.create(name="Casual", description="For casual events")

class UserProfileSerializer(serializers.ModelSerializer):
    wardrobe = WardrobeSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'wardrobe']     