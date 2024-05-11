"""
Student name: Yago Carballo Barroso
Module description: Este módulo contiene funciones para manejar la información de archivos WAVE, contiene funciones para pasar de estéreo a mon y viceversa.
Functions:  
    estereo2mono: Convierte un fichero .wav de estéreo a mono, según el valor de 'canal' hará lo siguiente:
        canal=0 : el archivo resultante tendrá la información del canal izquierdo original.
        canal=1 : el archivo resultante tendrá la información del canal derecho original.
        canal=2 : el archivo resultante contendrá la semisuma ((L + R) / 2) de R y L.
        canal=3 : el archivo resultante contendrá la semiresta ((L - R) / 2) de R y L.
    mono2estereo: Convierte dos ficheros .wav monofónicos en uno estereofónico
    codEstereo: Codifica un fichero .wav estereofónico y lo formatea alternando la semisuma y semiresta de cada muestra.
    decEstereo: Descodifica un fichero con el formato anterior y genera un fichero .wav estéreo. 
        ATENCIÓN: Para comprobar el correcto funcionamiento los canales R y L se intercambian en la descodificación, para evitarlo descomenta la linea 115 (y comenta la 116).

"""

import struct

HEADER_FORMAT = '<4sI4s4sIHHIIHH4sI'

def getData(file):

    with open(file, 'rb') as f:

        header = list(struct.unpack(HEADER_FORMAT, f.read(44)))

        data_format = f'<{ len(f.read()) // 2 }h'
        f.seek(44)
        
        data = list(struct.unpack(data_format, f.read()))

    if not header[0] == b'RIFF' and header[2] == b'WAVE' and header[3] == b'fmt ' and header[4] == 16 and header[5] == 1 and header[11] == b'data':
        raise TypeError("Los archivos deben ser .WAV PCM sin compresión.")

    return data, header
  

def setData(header, data, file_name, mono=True, BPSample=16):

    header[6] = 1 if mono else 2
    header[12] = len(data) * 2
    header[10] = BPSample

    header_bytes = struct.pack(HEADER_FORMAT, *header)

    data_format = f'<{ len(data) }h'
    data_bytes = struct.pack(data_format, *data)

    with open(file_name, 'wb') as f:
        f.write(header_bytes)
        f.write(data_bytes)


def estereo2mono(ficEste, ficMono, canal=2):
    data, header = getData(ficEste)

    if not header[6] == 2:
        raise TypeError("El archivo debe ser estéreo.")

    if canal == 0:
        data_ficMono = data[0::2]

    elif canal == 1:
        data_ficMono = data[1::2]

    elif canal == 2:
        data_ficMono = [ (data[i] + data[i+1]) // 2 for i in range(0, len(data), 2) ]

    elif canal == 3:
        data_ficMono = [ (data[i] - data[i+1]) // 2 for i in range(0, len(data), 2) ]

    else:
        raise ValueError("Debe introduir un canal válido (0 <= canal <= 3).")

    setData(header, data_ficMono, ficMono)
    

def mono2estereo(ficIzq, ficDer, ficEste):
    if not isinstance(ficIzq, str) and isinstance(ficDer, str) and isinstance(ficEste, str):
        raise ValueError("Los parámetros deben ser un string con la ruta a los archivos.")

    data_izq, header_izq = getData(ficIzq)
    data_der, header_der = getData(ficDer)

    
    if not header_izq[6] == 1 and header_der[6] == 1:
        raise TypeError("Ambos archivos deden ser monofónicos.")

    data_Este = [valor for tupla in zip(data_izq, data_der) for valor in tupla]
    
    setData(header_izq, data_Este, ficEste, mono=False)


def codEstereo(ficEste, ficCod):
    data_este, header_este = getData(ficEste)

    if not header_este[6] == 2:
        raise TypeError("El archivo debe ser estéreo.")

    data_este_sum = [ (data_este[i] + data_este[i+1]) // 2 for i in range(0, len(data_este), 2) ]
    data_este_sub = [ (data_este[i] - data_este[i+1]) // 2 for i in range(0, len(data_este), 2) ]

    data_cod = [valor for tupla in zip(data_este_sum, data_este_sub) for valor in tupla]

    setData(header_este, data_cod, ficCod, BPSample=32)


def decEstereo(ficCod, ficEste):
    data_cod, header_cod = getData(ficCod)

    data_este_L = [data_cod[i] + data_cod[i+1] for i in range(0, len(data_cod), 2) ]
    data_este_R = [data_cod[i] - data_cod[i+1] for i in range(0, len(data_cod), 2) ]

    # data_este = [valor for tupla in zip(data_este_L, data_este_R) for valor in tupla]   ===> Para no alterar los canales R y L
    data_este = [valor for tupla in zip(data_este_R, data_este_L) for valor in tupla]   # ===> Para intercambiar canales R y L

    setData(header_cod, data_este, ficEste, mono=False)
    

if __name__ == '__main__':

    estereo2mono('wav/komm.wav', 'wav/komm_e2m0.wav', canal=0) 
    estereo2mono('wav/komm.wav', 'wav/komm_e2m1.wav', canal=1)
    estereo2mono('wav/komm.wav', 'wav/komm_e2m2.wav', canal=2)
    estereo2mono('wav/komm.wav', 'wav/komm_e2m3.wav', canal=3)

    mono2estereo('wav/komm_e2m0.wav', 'wav/komm_e2m1.wav', 'wav/komm_m2e.wav')

    codEstereo('wav/komm.wav', 'wav/komm_cod.wav')
    decEstereo('wav/komm_cod.wav', 'wav/komm_deco.wav')
