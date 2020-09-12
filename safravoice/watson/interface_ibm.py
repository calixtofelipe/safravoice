from safravoice.watson.manipula_audio import encodeAudio
from os.path import join, dirname
from safravoice.models import ReqBuilder
from ibm_watson import SpeechToTextV1, TextToSpeechV1, AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def voz2Texto(nome_audio):
    """
    Função que converte o audio do cliente para um arquivo de texto
    :param nome_audio: Nome do arquivo de audios
    :return: script - Variável de texto  contendo as falas do cliente.
    :author: Ellen Giacometti
    """
    queryset = ReqBuilder.objects.filter(description='voz2Texto').get()
    secret = queryset.secret
    url = queryset.url
    authenticator = IAMAuthenticator(secret)
    voztexto_service = SpeechToTextV1(authenticator=authenticator)
    voztexto_service.set_service_url(url)
    with open(join(dirname(__file__), './.', nome_audio), 'rb') as audio_file:
        watson_resultado = voztexto_service.recognize(
            audio=audio_file,
            model='pt-BR_BroadbandModel',
            content_type='audio/wav',
            word_alternatives_threshold=0.9).get_result()
    script = ""
    while bool(watson_resultado.get('results')):
        script = watson_resultado.get('results').pop().get(
            'alternatives').pop().get('transcript') + script[:]
    return script


# pt-BR_IsabelaVoice,pt-BR_IsabelaV3Voice,
def texto2Voz(nome_arquivo, script):
    """
    Função que dado um texto converte para a voz da Isabela (Watson).
    Inicialmente iríamos usar a voz da Isabela,  mas como ela não tinha entonação humanizada,preferimos gravar os audios.
    :param nome_arquivo: Nome do arquivo de audios
    :param script: Variável de texto  contendo as falas do cliente.
    :author: Ellen Giacometti
    """

    queryset = ReqBuilder.objects.filter(description='texto2Voz').get()
    secret = queryset.secret
    url = queryset.url
    authenticator = IAMAuthenticator(secret)
    textovoz_service = TextToSpeechV1(authenticator=authenticator)
    textovoz_service.set_service_url(url)
    with open(nome_arquivo, 'wb') as audio_file:
        audio_file.write(
            textovoz_service.synthesize(
                script, voice="pt-BR_IsabelaV3Voice",
                accept='audio/wav').get_result().content)


def texto2Intencao(script):
    """
    Função recebe uma string de texto  e retorna a intenção do cliente e a acertividade da intenção identificada
    :param script: Variável de texto  contendo as falas do cliente.
    :return:intencao - Qual a intenção  que o cliente quis  transmitir
            confianca - Acertividade da intenção identificada
            script - Variável de texto  contendo as falas do cliente.
    :author: Ellen Giacometti
    """
    queryset = ReqBuilder.objects.filter(description='texto2Intencao').get()
    secret = queryset.secret
    url = queryset.url

    authenticator = IAMAuthenticator(secret)
    assistant = AssistantV1(version='2020-04-01', authenticator=authenticator)
    assistant.set_service_url(url)
    response = assistant.message(
        workspace_id='0cdbed9b-0268-43a6-968d-3030de036bf5',
        assistant_id='4873209d-6ce9-4bf1-8361-f4638e99b5a5',
        input={
            'message_type': 'text',
            'text': script
        }).get_result()
    intencao = response['intents'][0]['intent']
    confianca = response['intents'][0]['confidence']
    # print(response)
    return intencao, confianca, script


def montaAudioContasPagas(desc_pagamentos, valor, dia):
    """
    Função que montaria um aúdio único  para cada informação de extrato obtida na API Safra

    :param desc_pagamentos: Lista com os transactionDescription (informações de pagamento) do usuário
    :param valor: Lista com o valor dos pagamentos respectivos do transactionDescription
    :param dia: Lista com os dias dos pagamentos respectivos do transactionDescription
    :return: Variável encoded base64 referente ao aúdio
    :author: Ellen Giacometti
    """
    if len(desc_pagamentos) == 0:
        falafinal = "Então aqui não tem nenhum pagamento feito esse mês"

    if len(desc_pagamentos) == 1:
        falafinal = "Olha você já pagou " + valor[
            0] + " reais  referente a " + desc_pagamentos[
                0] + " no dia " + dia[0] + "desse mês."

    if len(desc_pagamentos) > 1:
        falainicial = "Fica sem preocupação estou vendo aqui que nesse mês você  já pagou "
        fala = desc_pagamentos[0]
        for descricao in desc_pagamentos[1:]:
            fala = fala + " e " + descricao
        falafinal = falainicial + fala
    texto2Voz("ContasPagasPersonalizado.wav", falafinal)
    audioContasPagas = encodeAudio("ContasPagasPersonalizado.wav")
    return audioContasPagas
