import base64
import requests
import json
import re
import os


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


def string2number(str):
    #numberlist = [int(s) for s in str.split() if s.isdigit()]
    numberlist = re.findall(r'\d+', str)
    if (len(numberlist) == 1):
        return numberlist[0]

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
            break
            #raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


#audio_bytes = decodeAudio(
#    os.path.dirname(os.path.abspath(__file__)) + '\\BemVindo01.wav',
#    'teste.wav')
#print(audio_bytes.decode("utf-8"))
#audiofile = decodeAudio(audio_bytes.decode("utf-8"),
#                       "teste.txt")
#bytes(audio_bytes.decode("utf-8"), 'utf-8')
"""

print(
    encodeAudio(
        os.path.dirname(os.path.abspath(__file__)) +
        '\\BemVindo01.wav').decode("utf-8"))
path_arquivo = os.path.dirname(os.path.abspath(__file__)) + '\\BemVindo01.wav'
audio_encode = encodeAudio(path_arquivo).decode("utf-8")
audiofile = decodeAudio(audio_encode, "teste.wav")
"""

#message = "Python is fun"

#print(encoded_audio)
#base64.b64decode(encoded_audio)
#message_bytes = encoded_audio.decode("utf-8")
#print(message_bytes)
#base64_bytes = base64.b64encode(encoded_audio)
#base64_message = base64_bytes.decode('ascii')

#print(base64_message)
#print('bytes >>>>>>>>>>>>', message_bytes.encode("utf-8"))
#message_bytes = base64.b64decode(message_bytes.encode("utf-8"))
#print('bytes >>>>>>>>>>>>', message_bytes)
#encode_audio = base64.b64encode(open("BemVindo01.wav", "rb").read())
#base64_message = 'UklGRv////9XQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAATElTVBoAAABJTkZPSVNGVA4AAABMYXZmNTguMjkuMTAwAGRhdGH/////6P/r/+v/4//f/9r/3v/c/9z/3P/b/9v/2//b/9v/2//c/9z/3P/e/97/3//Y/9z/3P/c/97/3v/f/9//3//g/+j/5P/m/+7/6//s/+7/5//r/+T/4P/e/+L/4v/i/9r/3v/W/9j/2v/Y/9j/2P/Y/9j/2v/S/9f/3v/i/9//4P/a/97/3//f/9j/1P/a/+L/3v/m/9v/2P/c/9z/3v/W/9r/2v/b/9v/2//j/+D/4P/i/+L/6//v/+z/9P/y//P/9v/2//f////2//r/AgD//wAAAAAIAAUABQAGAAYADgAKAAwADAAMAA0ADQAFAAEA/v8BAAgACgAOAAoACgAKABIAFgAaAB4AGgAcAB0AFgAUABAACgAWABkAFQAcACAAHAAcABoAIgAeAB4AGAAUABAAEgAaABUAFQAUABIADAAOABUAIAAYABgAGAAYABEAFQAcACYAJgAiACwAKAAxAC0ANQA5ADwAOgA6ADQAMAA0ADIAMgAxADAAMAA2ADIAMQA4ADoAPQA5AEEARQBBAEkATABIAEEARQA9AEAAQABFAEkARABEAEIAQQBBADgAMgAtADAALgAtACwAKQAhACIAIQAYABIADQAAAP//CAAMABgAEAAVACEAEgAOABAADgAWABQADAAGAAoAAgAFAA0AEAANAAwAFAAIAAoACgAKAAoACQAJAAkAEQANAA0ADQAMAAwADAAMAAQABgD//wIA+//2//L//P/6/wgAEQAJAAkACQABAP7/AAAAAAAA+v/0/wAABAAJAAUABAAEAAQABAAEAPT/9P/w/+v/6P/j/9//2//X/9r/2v/T/9b/3v/i/+f/5P/c/9r/3P/X/9P/1//f/97/1//b/9P/2P/g/97/3v/X/9v/5P/i/+P/2//f/+D/4v/j/+v/6P/i/+b/5v/n/+j/6P/o/+r/4//f/+P/4//k/+T/5v/u/+v/8//4//T/9v/2//f/7//z//T//P/y//b/9v/2////+/8CAAAABgAEAAQABQAMAAkACQAJAAkACgAKAAoACQARAA4ABgABAAUABQAFAP7/+P/0/+//8//r/9//3v/a/9z/3v/W/9j/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'
#base64_bytes = base64_message.encode('ascii')
#message_bytes = base64.b64decode(base64_bytes)
#message = message_bytes.decode('ascii')

#print(message)


def encode64_byte_to_texto(bytes):
    encoded_audio = base64.b64encode(bytes)
    byte2text = encoded_audio.decode("utf-8")
    print(len(byte2text))
    return byte2text


def write2file(text, nome_file):
    #request = encode64_byte_to_texto(byte_audio)
    wav_file = open(nome_file, "wb+")
    wav_file.write(text)


def decode64_text_to_byte(text):
    text2bytes = text.encode("utf-8")
    bytes_real = base64.b64decode(text2bytes)
    return bytes_real


#nome_arquivo = "Intencao07.wav"
#bytes_file = open(nome_arquivo, "rb").read()
#print(teste)
#print(os.path.dirname(os.path.abspath(__file__)) + '\\BemVindo01.wav')

encoded_audio = base64.b64encode(open(nome_arquivo, "rb").read())
request = encode64_byte_to_texto(bytes_file)
write2file(request.encode("utf-8"), 'Intencao07.txt')
#print(request)

# response = decode64_text_to_byte(base64teste)
# print(response)

text2int("quero fazer uma transferência de cem reais pimentões ")