from rest_framework import serializers


class InputTextSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=['en'], required=True)
    text = serializers.CharField(required=True)
