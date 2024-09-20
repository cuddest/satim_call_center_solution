from rest_framework import serializers
from .models import Administrator, User, call, order


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)  # This will hash the password
        instance.save()
        return instance


class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class call_serializer(serializers.ModelSerializer):
    class Meta:
        model = call
        fields = "__all__"


class order_serializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = "__all__"
