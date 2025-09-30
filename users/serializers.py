from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User
from rest_framework import serializers

class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','first_name', 'last_name','email', 'password')
        ref_name = "CustomUserCreateSerializerGym"

    def create(self, validated_data):
        validated_data['role'] = 'MEMBER'
        return super().create(validated_data)


class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',  'role', 'is_verified')
        ref_name = "CustomUserSerializerGym"
        read_only_fields = ('role', 'is_verified')
