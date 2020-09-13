import base64
import json
import os
import base64
import requests
import json

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safraapp.settings')
#print(os.environ.get('DJANGO_SETTINGS_MODULE'))
#import django
#django.setup()

from safravoice.models import ReqBuilder
import requests
import re


def get_token():
    """
        Responsável por obter o token de autenticação na api do safra
    """
    queryset = ReqBuilder.objects.filter(description='reqToken').get()
    client_id = queryset.client_id
    secret = queryset.secret
    url = queryset.url

    payload = "grant_type=client_credentials&scope=urn:opc:resource:consumer::all"

    to_token = client_id + ':' + secret
    encoded = base64.b64encode(to_token.encode("ascii"))
    auth = 'Basic ' + encoded.decode()
    headers = {
        'authorization': 'Basic ' + encoded.decode(),
        'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    retorno = dict()
    if (response.status_code >= 200 and response.status_code <= 299):
        retorno = response.json()
        retorno['statuscode'] = response.status_code
    else:
        retorno['statuscode'] = response.status_code

    return retorno


def send_transaction_safra(celular):
    """
        Responsável por realizar transferência de um usuário para outra conta
    """
    print('begin', 'send_transaction_safra')
    response_token = get_token()

    retorno = dict()
    if (response_token['statuscode'] == 200):
        token = response_token['access_token']
    else:
        return retorno['statuscode'] == 405
    print("recuperou_token_safra", token)
    queryset = ReqBuilder.objects.filter(description='transfSafra').get()
    url = queryset.url

    payload = {
        "Type": "TEF",
        "TransactionInformation": "Mensalidade Academia",
        "DestinyAccount": {
            "Bank": "422",
            "Agency": "0071",
            "Id": "1234533",
            "Cpf": "12345678933",
            "Name": "Mark Zuckerberg da Silva",
            "Goal": "Credit"
        },
        "Amount": {
            "Amount": "250.00",
            "Currency": "BRL"
        }
    }
    json_object = json.dumps(payload)
    auth = 'Bearer ' + token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }

    response = requests.request("POST", url, headers=headers, data=json_object)
    print('retorno request extrato', response.status_code)
    retorno = dict()
    if (response.status_code >= 200 and response.status_code <= 299):
        retorno = response.json()
        retorno['statuscode'] = 200

    else:
        retorno['statuscode'] = response.status_code

    return retorno


def get_extrato(script):
    """
        Responsável por realizar a consulta de extrato bancário
    """
    response_token = get_token()

    retorno = dict()
    if (response_token['statuscode'] == 200):
        token = response_token['access_token']
    else:
        return retorno['statuscode'] == 405

    queryset = ReqBuilder.objects.filter(description='consultaExtrato').get()
    url = queryset.url

    auth = 'Bearer ' + token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': auth,
    }
    response = requests.request("GET", url, headers=headers)
    retorno = dict()
    if (response.status_code >= 200 and response.status_code <= 299):
        #retorno = response.json()
        extrato = response.json()
        for transaction in extrato['data']['transaction']:
            informacao = transaction['transactionInformation']
            if (informacao.lower() in script.lower()):
                retorno['intention'] = informacao
            else:
                retorno['intention'] = 'sem_despesa'

    else:
        retorno['intention'] = 'error'
    print('retorno_extrato', retorno)
    return retorno


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


def string2number(str):
    """
        realizar a conversão de uma string com números para uma lista de números
    """
    #numberlist = [int(s) for s in str.split() if s.isdigit()]
    numberlist = re.findall(r'\d+', str)
    numberAnterior = None
    final_list = []
    sequencial = 0
    for number in numberlist:
        sequencial = sequencial + 1
        if (numberAnterior is None):
            numberAnterior = number
            #print(numberAnterior)
        else:
            number_decimal = numberAnterior + '.' + number
            #print(number_decimal)
            if (number_decimal in str):

                final_list.append(number_decimal)
                numberAnterior = None
            else:
                if (sequencial == len(numberlist)):
                    final_list.append(numberAnterior)
                    final_list.append(number)
                else:
                    final_list.append(numberAnterior)
                    numberAnterior = number

    return final_list


def text2int(textnum, numwords={}):
    if not numwords:
        units = [
            "zero",
            "um",
            "dois",
            "três",
            "quatro",
            "cinco",
            "seis",
            "sete",
            "oito",
            "nove",
            "dez",
            "onze",
            "doze",
            "treze",
            "quatorze",
            "quinze",
            "dezesseis",
            "dezesete",
            "dezoito",
            "dezenove",
        ]

        tens = [
            "", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta",
            "setenta", "oitenta", "noventa"
        ]

        centenas = [
            "", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
            "seiscentos", "setecentos", "oitocentos", "novecentos"
        ]

        scales = ["mil", "milh", "bilh", "trilh"]

        numwords["e"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(centenas):
            numwords[word] = (1, idx * 100)
        for idx, word in enumerate(scales):
            numwords[word] = (10**(idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current