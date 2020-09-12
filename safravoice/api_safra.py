import base64
import json
import os
import base64
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safraapp.settings')
print(os.environ.get('DJANGO_SETTINGS_MODULE'))
import django
django.setup()

from safravoice.models import ReqBuilder, ExtratoModel
import requests


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
    response_token = get_token()

    retorno = dict()
    if (response_token['statuscode'] == 200):
        token = response_token['access_token']
    else:
        return retorno['statuscode'] == 405

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
    print(token)
    response = requests.request("POST", url, headers=headers, data=json_object)
    retorno = dict()
    if (response.status_code >= 200 and response.status_code <= 299):
        print(response.status_code)
        retorno = response.json()
        retorno['statuscode'] = 200

    else:
        retorno['statuscode'] = response.status_code

    return retorno


def get_extrato(intencao, tipoGasto):
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
        if (intencao == 'extrato_completo'):
            retorno['intention'] = 'extrato_completo'
            return retorno
        elif (intencao == 'tipo_gasto'):
            for transaction in extrato['data']['transaction']:
                informacao = transaction['transactionInformation']
                if (tipoGasto.lower() in informacao.lower()):
                    retorno['intention'] = 'positivo'
                else:
                    retorno['intention'] = 'negativo'

    else:
        retorno['intention'] = 'error'

    return retorno