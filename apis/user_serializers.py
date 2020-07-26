from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from k12App.models import User

import re

class UserRegisterSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=255, required = True)
    username = serializers.CharField(max_length=255, required = True)
    mobile = serializers.CharField(max_length=255, required = True)
    email = serializers.CharField(required= True, validators = [validate_email])
    password = serializers.CharField(max_length=255, required = True)
    confirm_password = serializers.CharField(max_length=255, required = True)

    class Meta:
        model = User
        #fields = '__all__'
        fields = ['name','username','mobile','email', 'password','confirm_password']
        # extra_kwargs = {'confirm_password',}

    def validate_name(self, name):
        if name is None:
            raise serializers.ValidationError('Name cannot be null')
        elif not re.match(r"^[a-zA-z_.-]*$",name):
            raise serializers.ValidationError('Name should contain only alphabets')
        return name

    def validate_username(self, username):
        if not username:
            raise serializers.ValidationError('Please provide username')
        else:
            try:
                User = get_user_model()
                if not User.objects.filter(username=username).exists():
                    return username
                else:
                    raise serializers.ValidationError('username should be unique')
            except Exception as e:
                raise (e)

    def validate_mobile(self, number):
        if not number:
            raise serializers.ValidationError('Please enter mobile number')
        elif len(number)> 10:
            raise serializers.ValidationError('Number should not be greater than 10 digits')
        elif not number.isdigit():
            raise serializers.ValidationError('Number should be digits only')
        else:
            try:
                User = get_user_model()
                user = User.objects.get(mobile=number)
                if user:
                    raise serializers.ValidationError('Number already registered')
            except User.DoesNotExist:
                return number
            except Exception as e:
                raise e

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError('Email is required')
        else:
            try:
                User = get_user_model()
                user = User.objects.get(email=email)
                if user:
                    raise serializers.ValidationError('Email already registered')
            except User.DoesNotExist:
                return email
            except Exception as e:
                raise e

    def validate_password(self, password):
        return password

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password and confirm password does not match')

        data.pop('confirm_password')

        return data

