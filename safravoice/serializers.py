from rest_framework import serializers
from safravoice.models import ReqBuilder
from safravoice.api_safra import send_transaction_safra


class ReqBuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReqBuilder
        fields = ['id', 'description', 'url']


class SendTransactionSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=300)


class IntentionSerializer(serializers.Serializer):
    intention = serializers.CharField(max_length=300)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
