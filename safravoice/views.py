from django.shortcuts import render
import requests
import io
import json
from requests.models import Response
from django.http import JsonResponse
from safravoice.models import ReqBuilder
from safravoice.serializers import ReqBuilderSerializer, SendTransactionSerializer, IntentionSerializer
from safravoice.api_safra import send_transaction_safra, get_extrato
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from collections import namedtuple
from safravoice.watson.api_watson import decodeAudio, voz2Texto, texto2intensao
# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def process_voice(request):
    """
        Esse endpoint processa a voz do usuário o e nome do arquivo para retornar qual a intenção do usuário.
        Caso seja uma inteção de consulta de extrato já faz a consulta e retorna a resposta.
    """
    if request.method == 'POST':
        response = dict()
        intention = audio2intention(request.data['nome_arquivo'],
                                    request.data['encoded_audio'])
        intention = 'extrato_completo'
        response['intention'] = intention

        if (intention in ['extrato_completo', 'tipo_gasto']):
            retorno_extrato = get_extrato(intention, "carro")
            response = get_extrato(intention, "carro")

        serializer = IntentionSerializer(data=response)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
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


"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def consulta_extrato(request):
    'Esse endpoint efetua a consulta do extrato e retorna'
    if request.method == 'POST':
        response = dict()
        intention = audio2intention(request.data['nome_arquivo'],
                                    request.data['encoded_audio'])
        intention = 'efetuar_transferencia'
        response['intention'] = intention
        serializer = IntentionSerializer(data=response)

        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class ReqBuilderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ReqBuilder.objects.all()
    serializer_class = ReqBuilderSerializer


def audio2intention(nome_arquivo, encoded_audio):
    audiofile = decodeAudio(encoded_audio, nome_arquivo)
    text_audio = voz2Texto(audiofile)
    intention = texto2intensao(text_audio)
    return intention
