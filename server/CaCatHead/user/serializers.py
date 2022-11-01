from rest_framework import serializers


class LoginPayloadSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)


class RegisterPayloadSerializers(LoginPayloadSerializer):
    email = serializers.EmailField()
