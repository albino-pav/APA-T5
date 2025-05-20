import struct as st
import matplotlib.pyplot as plt
import numpy as np

fichero = 'wav/komm.wav'
salida1 = 'wav/sortida1.wav'
salida2 = 'wav/sortida2.wav'
salida3 = 'wav/sortida3.wav'
salida4 = 'wav/sortida4.wav'
FicIzq = 'wav/izq.wav'
FicDer = 'wav/der.wav'

def codEstereo(ficEste, ficCod):
    """
    Esta funcion lee la señal estereo contenida en 'ficEste' codificada con PCM lineal de
    16 bits, y construye una señal codificada con 32 bits que permita su reproduccion tanto en 
    sistemas monofonicos cono en sistemas estero que lo permitan.
    """
  
    with open(ficEste, 'rb') as fpEste:
        # Leer cabecera RIFF
        riff, size, fformat = st.unpack('<4sI4s', fpEste.read(12))
        if riff != b'RIFF' or fformat != b'WAVE':
            raise Exception("No es un archivo WAV válido.")

        # Leer chunks hasta encontrar 'fmt '
        fmt_chunk_found = False
        data_chunk_found = False

        while not fmt_chunk_found:
            chunk_id, chunk_size = st.unpack('<4sI', fpEste.read(8))
            if chunk_id == b'fmt ':
                fmt_data = fpEste.read(chunk_size)
                fmt_chunk_found = True
            else:
                fpEste.seek(chunk_size, 1)

        audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = st.unpack('<HHIIHH', fmt_data[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise Exception("Este programa solo soporta WAV estéreo PCM de 16 bits.")

        # Leer chunks hasta encontrar 'data'
        while not data_chunk_found:
            chunk_id, chunk_size = st.unpack('<4sI', fpEste.read(8))
            if chunk_id == b'data':
                data_chunk_found = True
                data = fpEste.read(chunk_size)
            else:
                fpEste.seek(chunk_size, 1)

        # Separar canales
        L = int(data[::2])
        R = int(data[1::2])

        semiSum = (L+R)/2
        semiDif = (L-R)/2

        with open(ficCod, 'wb') as fpCod:
            for i in range(0, len(semiSum), 2):
                fpCod.write(semiSum[i], semiSum[i+1])
                fpCod.write(semiDif[i], semiDif[i+1])