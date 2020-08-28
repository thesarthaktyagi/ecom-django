from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import JsonResponse
from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        username = validated_data.get('email')
        password = validated_data.pop('password', None)
        UserModel = get_user_model()
        old = UserModel.objects.filter(email=username)

        if old:
            raise serializers.ValidationError(
                {'error': 'email already exists'})
        else:
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)

            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        extra_kwargs = {'email': {'validators': [IntegrityError]},
                        'password': {'write_only': True}}
        fields = ('name', 'email', 'password', 'phone', 'gender',
                  'is_active', 'is_staff', 'is_superuser')
