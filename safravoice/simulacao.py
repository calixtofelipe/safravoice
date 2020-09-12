import base64
import requests
import json


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


def send_transaction(token):
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
        'Content-Type':
        'application/json',
        'Authorization':
        'Bearer eyJ4NXQjUzI1NiI6IlNhWkUtSjdJdDBQWFRYNFlCaTBCeXk4WWhPVlJkSzlNNXgzREN3R2ZnbkEiLCJ4NXQiOiJVSWpBeHIyTWlzNk9JdTNMS2NsX3JPSHl3eXMiLCJraWQiOiJTSUdOSU5HX0tFWSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI5NGVkMDNhZDljOGI0YjA3OWZmMjhlYzg1NGZhYjgwMSIsImd0cCI6ImNjIiwidXNlci50ZW5hbnQubmFtZSI6ImlkY3MtOTAyYTk0NGZmNjg1NGM1ZmJlOTQ3NTBlNDhkNjZiZTUiLCJzdWJfbWFwcGluZ2F0dHIiOiJ1c2VyTmFtZSIsInByaW1UZW5hbnQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9pZGVudGl0eS5vcmFjbGVjbG91ZC5jb21cLyIsInRva190eXBlIjoiQVQiLCJjbGllbnRfaWQiOiI5NGVkMDNhZDljOGI0YjA3OWZmMjhlYzg1NGZhYjgwMSIsImNhX2d1aWQiOiJjYWNjdC1iOThlNGJjZDQ1MDU0YjZlOTc3NzU5OThiNmYzNmYwNiIsImF1ZCI6InVybjpvcGM6cmVzb3VyY2U6c2NvcGU6YWNjb3VudCIsInN1Yl90eXBlIjoiY2xpZW50Iiwic2NvcGUiOiJ1cm46b3BjOnJlc291cmNlOmNvbnN1bWVyOjphbGwiLCJjbGllbnRfdGVuYW50bmFtZSI6ImlkY3MtOTAyYTk0NGZmNjg1NGM1ZmJlOTQ3NTBlNDhkNjZiZTUiLCJleHAiOjE1OTk4NTcxOTEsImlhdCI6MTU5OTg1MzU5MSwidGVuYW50X2lzcyI6Imh0dHBzOlwvXC9pZGNzLTkwMmE5NDRmZjY4NTRjNWZiZTk0NzUwZTQ4ZDY2YmU1LmlkZW50aXR5Lm9yYWNsZWNsb3VkLmNvbTo0NDMiLCJjbGllbnRfZ3VpZCI6ImVhYzUyODkwMWQwYTQ1MGY5MTllZjg0Y2QxNmI2ZjEwIiwiY2xpZW50X25hbWUiOiJUaW1lIDEwIiwidGVuYW50IjoiaWRjcy05MDJhOTQ0ZmY2ODU0YzVmYmU5NDc1MGU0OGQ2NmJlNSIsImp0aSI6IjExZWFmNDY3N2RjNjJlM2ZiODc2YjMwMDU2MTRjMzczIn0.t5XVfruS0M4Wz-Idee42hN_y3-iTQkJTRty0WaMl6RGjQkI-_dF104LXkovW0UA86BKoy9C8J39uIZgLCzpQS-PQcAltWGP1OGvb23bGNIzxI2fjCVbxebH4gAqZCGDCxpUKxcmuA6Znzil6PxctTk0vlfgDUAWlw7SWuV2V8PxW78ZYNjAa325XOVi-FzbXc7J3PIforP8PFINz_WgTHStr83wF-FAO4qNNL6Gjw5mqJJjbYq_SgaAhQpATQNQ2jGwEGiWYKzONHrZ3G7tq5rwGm80wuCywZeCCNbx4GG3xXh3zYNwLLH9udUo3q_yAK-Br8x9UDqj3t52g3sWgcg'
    }
    response = requests.request("POST", url, headers=headers, data=json_object)
    if (response.status_code >= 200 and response.status_code <= 299):
        retorno = response.json()
    else:
        retorno['statuscode'] = 404


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

    url = 'https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/00711234522/transactions'

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
        retorno['statuscode'] = 200
        if (intencao == 'extrato_completo'):
            retorno['response'] = 'extrato_completo'
            return retorno
        elif (intencao == 'tipo_gasto'):
            for transaction in extrato['data']['transaction']:
                informacao = transaction['transactionInformation']
                if (tipoGasto.lower() in informacao.lower()):
                    retorno['response'] = 'positivo'
                else:
                    retorno['response'] = 'negativo'

    else:
        retorno['statuscode'] = response.status_code

    return retorno


import re


def string2number(str):
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


numbers = string2number("h3110d 23 cat 444.4 rabbit 11 2 dog")
print(numbers[0])
