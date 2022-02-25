from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.CharField()


class CategorySerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class AccountSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class TransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    description = serializers.CharField()
    amount = serializers.FloatField()
    date = serializers.DateField()
    category = CategorySerializer()
