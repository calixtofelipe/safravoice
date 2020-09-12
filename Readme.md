# SafraVoice

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

SafraVoice é o atendimento por voz realizado pelo Safra visando simplificar o atendimento para os clientes.

# New Features por comando de voz!
  - Realiza transferencias
  - Realiza consulta de extrato
  - Obter informações sobre lançamentos no extrato

## Integrações
SafraVoice utiliza integrações com duas API:
  - API Safra OPEN Banking
  - API IBM Watson (transcrição de voz e análise de texto)

#### Endpoints

##### Obter token
`GET [host]/api/get_token`

##### Enviar audio para ser processado
`POST [host]/api/process_voice`


### Tech

* [Django] - servidor de endpoints para o frontend
* [jangorestframework] - controle de rotas, serializers e provedor dos endpoints
* [React native] - frontend.
* [Autenticacão por token] - uso do app authtoken do rest_framework para autenticação.
* [Sqlite Database] - banco de dados utilizado para guardar os endpoints da integração.

### Installation

1 - Rode o requirements
2 - Configure usuário no Admin do jango
3 - Configure no cadastro de request builder os tokens e urls necessários para API Safra e API Watson


# Technee

## Aspectos técnicos

### APIs

#### Endpoints

##### Consulta saldo da conta
`GET [host]/open-banking/v1/accounts/{accountId}/balances`

##### Consulta extrato da conta
`GET [host]/open-banking/v1/accounts/{accountId}/transactions`

### Dados de Acesso Admin
user = safraadm
senha = s@fra!Voice

user = safraapi
senha = s@fra!restVoice