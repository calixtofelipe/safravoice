from django.shortcuts import render
import base64
import requests
import io
import json
from requests.models import Response
from django.http import JsonResponse
from collections import namedtuple
import os
from os.path import join, dirname
from safravoice.models import ReqBuilder, TransactionModel
from safravoice.serializers import ReqBuilderSerializer, SendTransactionSerializer, IntentionSerializer
from safravoice.api_safra import send_transaction_safra, get_extrato, string2number, text2int
from safravoice.interface_ibm import texto2Intencao, texto2Voz, voz2Texto, voz2TextoBytes
from safravoice.manipula_audio import decodeAudio

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def process_voice(request):
    """
        Esse endpoint processa a voz do usuário o e nome do arquivo para retornar qual a intenção do usuário.
        Caso seja uma inteção de consulta de extrato já faz a consulta e retorna a resposta.
    """
    print('entrou no processvoice')
    if request.method == 'POST':
        try:
            response = dict()
            print("entrou no post")
            [intention, confianca,
             script] = audio2intention(request.data['encoded_audio'],
                                       request.data['nome_arquivo'])

            if (intention in ['Banking_Transfer_Money']):
                # TRATATIVA PARA INTENTION DE TRANSFERENCIA - PEDINDO O TELEFONE

                valor = 100  #text2int(script)
                print('entrou no Banking_Transfer_Money', script, valor)
                try:
                    queryset = TransactionModel.objects.get(id=1)
                    queryset.valor = valor
                    queryset.save()

                except TransactionModel.DoesNotExist as e:
                    queryset = TransactionModel.objects.get(
                        pk=1, valor=100, intention='Banking_Transfer_Money')
                # retornar pedindo o numero.
                response['intention'] = intention

            elif (intention in ['VocalizaTelefone']):
                # TRATATIVA PARA INTENTION DE TRANSFERENCIA REALIZAR A TRANSFERENCIA
                print('entrou na vocaliza telefone', script)
                cellphone = 34994887452  #string2number(script)
                print('entrou na vocaliza telefone', cellphone)
                retorno_extrato = send_transaction_safra(cellphone)
                if (retorno_extrato['statuscode'] >= 200
                        and retorno_extrato['statuscode'] <= 299):
                    response['intention'] = 'sucesso'
                    print('sucesso_extrato')
                else:
                    response['intention'] = 'servidor_indisponivel'

            elif (intention in ['QuestionarPagamento']):
                # TRATATIVA PARA INTENTION DE QUESTIONAR PAGAMENTO
                print('entrou no questionar pagamento')
                info_extrato = get_extrato(script)
                response['intention'] = info_extrato['intention']
            else:
                response['intention'] = intention
        except Exception as e:
            response['intention'] = 'error'

        serializer = IntentionSerializer(data=response)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReqBuilderViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ReqBuilder.objects.all()
    serializer_class = ReqBuilderSerializer


def audio2intention(encoded_audio, nome_arquivo):
    print('entrou no audio2intention')
    message_bytes = decode64_text_to_byte(encoded_audio)
    text_audio = voz2TextoBytes(message_bytes)
    retorno = texto2Intencao(text_audio)
    return retorno


def decode64_text_to_byte(text):
    text2bytes = text.encode("utf-8")
    bytes_real = base64.b64decode(text2bytes)
    return bytes_real