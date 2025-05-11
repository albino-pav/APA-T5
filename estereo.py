"""
Arnau Piñero Masegosa

Este fichero contiene algunas funciones que permiten gestionar los canales de ficheros
WAVE incluyendo su codificacion y decodificacion.
"""

import struct as st

def estereo2mono(ficEste, ficMono, canal=2):
    """
    Esta funcion lee el fichero 'ficEste', que contiene una señal estereo, y devuelve una
    señal monofonica en el fichero 'ficMono'. El tipo de señal monofonica depende del argumento
    'canal':
    canal = 0 ==> Se almacena en el canal izquierdo (L).
    canal = 1 ==> Se almacena en el canal derecho (R).
    canal = 2 ==> Se almacena la semisuma (L+R)/2. (Default)
    canal = 3 ==> Se almacena la semidiferencia (L-R)/2.
    """

    with open(ficEste, 'rb') as fpEstero:
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerData = list(st.unpack(formato, datos))
        # chunkID[0], chunkSize[1], format[2], chunk1ID[3], chunk1Size[4], audFormat[5], nChannels[6], sampleRate[7], bitRate[8], bAlign[9], bps[10], chunk2ID[11], fileSize[12]  
        
        if headerData[0] != b'RIFF' or formato != b'WAVE':
            raise Exception(f'El fichero {ficEste} no tiene formato WAVE.')
        
        with open(ficMono, 'wb') as fpMono:
            fpEstero.seek(44, 0) # Posicionamos el puntero de lectura al principio de los datos (byte 44)
            for i in range(0, headerData[12]):
                L = fpEstero.read(2)
                R = fpEstero.read(2)
            
            # Cambiamos el numero de canales en la cabecera
            headerData[6] = 1
            fpMono.write(headerData)

            if canal == 0:
                fpMono.write(L)

            elif canal == 1:
                fpMono.write(R)
                
            elif canal == 2:
                mono = (L+R)/2 
                fpMono.write(mono)
                
            elif canal == 3:
                mono = (L-R)/2
                fpMono.write(mono)

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Esta funcion construye a partir de las señales monofonicas 'ficIzq' (L) y 'ficDer' (R)
    una señal estereo, que se almacena en el fichero 'ficEste'.
    """
    with open(ficIzq, 'rb') as fpIzq:
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerDataL = list(st.unpack(formato, datos))

        with open(ficDer, 'rb') as fpDer:
            formato = '<4sI4s4sIHHIIH4sI'
            datos = ficEste.read(st.calcsize(formato))
            headerDataR = list(st.unpack(formato, datos)) 

            # Comprovamos coincidencias por orden: RIFF, sampleRate, fileSize
            if headerDataL[0] != b'RIFF' or headerDataR[0] != b'RIFF':
                raise Exception(f'Los ficheros de entrada no tienen formato WAVE.')
            if headerDataL[7] != headerDataR[7]:
                raise Exception(f'La frequencia de muestro de los ficheros no coincide.')
            if headerDataL[12] != headerDataR[12]:
                raise Exception(f'El tamaño de los ficheros no coincide.')

            with open(ficEste, 'wb') as fpEste:
                # Cambiamos el numero de canales a 2 y añadimos la cabecera al fichero de salida
                headerDataL[6] = 2 
                fpEste.write(headerDataL)

                for i in range(0, len(fpDer)):
                    L = fpIzq.read(2)
                    R = fpDer.read(2)
                    fpEste.write(L)
                    fpEste.write(R)

def codEstereo(ficEste, ficCod):
    """
    Esta funcion lee la señal estereo contenida en 'ficEste' codificada con PCM lineal de
    16 bits, y construye una señal codificada con 32 bits que permita su reproduccion tanto en 
    sistemas monofonicos cono en sistemas estero que lo permitan.
    """
    # 4 bytes de L+R y 4 de L-R
    ...

def decEstereo(ficCod, ficEste):
    """
    Esta funcion lee la señal monofonnica de 32 bits contenida en 'ficCod' en la que los 
    16 MSB contienen la semisuma de los canales L y R, y los 16 LSB contienen la semidiferencia
    y escribe en 'ficEste' los dos canales por separado en formato WAVE estereo.
    """

    ...



#- Es muy recomendable escribir, además, sendas funciones que *empaqueten* 
# y *desempaqueten* las cabeceras de los ficheros WAVE a partir de los 
# datos contenidos en ellas.

#- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, 
# de *comprensiones*.

#- Los ficheros se deben abrir y cerrar usando gestores de contexto.

#- Las funciones deberán comprobar que los ficheros de entrada tienen el 
# formato correcto y, en caso contrario, elevar la excepción correspondiente.

#- Los ficheros resultantes deben ser reproducibles correctamente usando
# cualquier reproductor estándar; por ejemplo, el Windows Media Player 
# o similar. Es probable, muy probable, que tenga que modificar los de las
# cabeceras de los ficheros para conseguirlo.