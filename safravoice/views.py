from django.shortcuts import render
import requests
import io
import json
from requests.models import Response
from django.http import JsonResponse
from safravoice.models import ReqBuilder
from safravoice.serializers import ReqBuilderSerializer, SendTransactionSerializer, UserSerializer
from safravoice.api_safra import send_transaction_safra
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from collections import namedtuple
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_transaction(request):
    """
        Esse endpoint recebe o numero de telefone consulta no banco de dados
        busca os dados bancários no cadastro e faz a transferência.
    """
    if request.method == 'POST':
        response = dict()
        retorno_transaction = send_transaction_safra(request.data['celular'])
        if (retorno_transaction['statuscode'] == 200):
            response['status'] = 'Sucesso'
        else:
            response['status'] = 'Não foi possível realizar transferência'
        serializer = SendTransactionSerializer(data=response)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReqBuilderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ReqBuilder.objects.all()
    serializer_class = ReqBuilderSerializer