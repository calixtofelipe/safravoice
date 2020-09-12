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


def get_token2():
    """
        Responsável por obter o token de validação
    """
    queryset = ReqBuilder.objects.filter(
        description='Requisição de token').get()
    client_id = queryset.client_id
    secret = queryset.secret
    url = queryset.url
    header = {"Content-type": "application/json"}
    to_token = client_id + ':' + secret
    encoded = base64.b64encode(bytes(to_token, 'uft-8'))
    print(encoded, encoded.encode('utf-8'))
    response = requests.post(url, headers=header, json=encoded.encode('utf-8'))
    print(response)


def get_token():
    """
        Responsável por obter o token de validação
    """
    client_id = 'f892fe88abc443ac9362e11125092313'
    secret = 'a71948e5-02fc-48ec-b8bc-4e3b7ebb2cd0'
    url = "https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token"

    to_token = client_id + ':' + secret
    payload = "grant_type=client_credentials&scope=urn:opc:resource:consumer::all"
    encoded = base64.b64encode(to_token.encode("ascii"))
    headers = {
        'authorization': 'Basic ' + encoded.decode(),
        'content-type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if (response.status_code >= 200 and response.status_code <= 299):
        retorno = response.json()
        retorno['statuscode'] = 200
    else:
        retorno['statuscode'] = response.status_code

    return retorno


def send_transaction_safra():

    response_token = get_token()

    retorno = dict()
    if (response_token['statuscode'] == 200):
        token = response_token['access_token']
    else:
        return retorno['statuscode'] == 405

    url = "https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/accounts/v1/accounts/00711234511/transfers"

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

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("POST", url, headers=headers, data=json_object)
    if (response.status_code >= 200 and response.status_code <= 299):
        retorno = response.json()
        retorno['statuscode'] = 200

    else:
        retorno['statuscode'] = response.status_code
        print(response.status_code)

    return retorno
