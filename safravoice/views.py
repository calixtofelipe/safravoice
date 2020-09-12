from django.shortcuts import render
import requests
from safravoice.models import ReqBuilder
from safravoice.serializers import ReqBuilderSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from safravoice.api_safra import send_transaction_safra
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from collections import namedtuple
# Create your views here.
import io
import json
from requests.models import Response
from django.http import JsonResponse


@api_view(['GET'])
def send_transaction(request):
    data = send_transaction_safra()
    if request.method == 'GET':
        response = JsonResponse(data)
    return response


@api_view(['GET', 'POST'])
def reqbuilder_list(request):
    """
        
    """
    if request.method == 'GET':
        reqbuiders = ReqBuilder.objects.all()
        serializer = ReqBuilderSerializer(reqbuiders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReqBuilderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)