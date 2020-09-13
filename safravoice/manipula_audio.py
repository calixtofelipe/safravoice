import base64
# import sounddevice as sd
import wavio


def encodeAudio(nome_arquivo):
    """
    Função utilizada para conversão base64
    :param nome_arquivo: Nome do arquivo de audios
    :return: Arquivo de texto encoded
    :author: Ellen Giacometti
    """
    encoded_audio = base64.b64encode(open(nome_arquivo, "rb").read())
    return encoded_audio


def decodeAudio(encoded_audio, nome_arquivo):
    """
    Função utilizada para desconversão base64
    :param encoded_audio: Arquivo de texto encoded
    :param nome_arquivo:Nome do arquivo de audios
    :author: Ellen Giacometti
    """

    base64_bytes = encoded_audio.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    wav_file = open(nome_arquivo, "wb+")
    wav_file.write(message_bytes)
