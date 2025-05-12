'''
Núria Rodríguez Pardo. 
Sonido estéreo y ficheros WAVE: este fichero incluyen las funciones 
que permiten el manejo de los canales de una señal estéreo y su 
codificación/decodificación para compatiblilizar ésta con sistemas
monofónicos.
'''

import numpy as np
import struct as st
import matplotlib.pyplot as plt

ficEste = 'wav/komm.wav'

def estereo2mono(ficEste, ficMono, canal=2):
    '''
    Convierte un fichero estéreo a mono.
    '''
    # Abrimos el fichero estéreo
    with open(ficEste, 'rb') as fpWave: 
        formato = '<4sI4s'
        datos = fpWave.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)
        if chunkID != b'RIFF' or format != b'WAVE':
            raise Exception(f"El fichero {ficEste} no tiene formato WAVE")
        print(f"La mida del fitxer és de {chunkSize+8} bytes.")

    plt.plot(ficEste, "magenta")