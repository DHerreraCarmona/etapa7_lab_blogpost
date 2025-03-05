from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= get_user_model()
        fields = ["id", "email", "username","password"]
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]

        user = get_user_model()
        new_user = user.objects.create(email=email,username=username)
        new_user.set_password(password)
        new_user.save()

        return new_user