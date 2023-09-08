from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserInfo


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2') 
        if password != password2:
            raise serializers.ValidationError("password and conform password doesn't match")
        return attrs

    def create(self, validated_data):
        password2 = validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username', 'password']
    

class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    image = serializers.ImageField()
    class Meta:
        model = UserInfo
        fields = ('username', 'image', 'bio')



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username")