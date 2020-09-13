import base64
import sounddevice as sd
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


def gravaAudio(audio_filename, segundos):
    """
    Função usada para gravar audios de testes unitários ao longo do processo

    :param audio_filename: Nome do arquivo de audio
    :param segundos: Tempo  em segundos do audio
    :author: Ellen Giacometti
    """
    fs = 44100  # Taxa de amostragem
    for i in range(len(audio_filename)):
        # A captura de audio deve começar após 500ms,esse tempo de silêncio é para minimizar os ruídos
        print("[AUDIO_INPUT] Gravando audio")
        audio = sd.rec(int(segundos * fs), samplerate=fs, channels=2)
        sd.wait()  # Aguarda enquanto o audio está sendo gravado
        print("[AUDIO_INPUT] Salvando audio no formato .wav")
        wavio.write(audio_filename[i], audio, fs,
                    sampwidth=2)  # Salva o audio na taxa de amostragem gravada
