from rest_framework import serializers
from safravoice.models import ReqBuilder, ExtratoModel


class ReqBuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReqBuilder
        fields = ['id', 'description', 'url']
