'''
Núria Rodríguez Pardo. 
Sonido estéreo y ficheros WAVE: este fichero incluyen las funciones 
que permiten el manejo de los canales de una señal estéreo y su 
codificación/decodificación para compatiblilizar ésta con sistemas
monofónicos.
'''

import numpy as np
import struct as st

fichero = 'wav/komm.wav'
salida1 = 'wav/sortida1.wav'
salida2 = 'wav/sortida2.wav'
salida3 = 'wav/sortida3.wav'
salida4 = 'wav/sortida4.wav'
FicIzq = 'wav/izq.wav'
FicDer = 'wav/der.wav'

def estereo2mono(ficEste, ficMono, canal=2):
    '''
    Convierte un fichero estéreo a mono.

    canal = 0 ==> Se almacena en el canal izquierdo (L).
    canal = 1 ==> Se almacena en el canal derecho (R).
    canal = 2 ==> Se almacena la semisuma (L+R)/2. (Default)
    canal = 3 ==> Se almacena la semidiferencia (L-R)/2.
    '''
    with open(ficEste, 'rb') as f:
        # Leer cabecera RIFF
        riff, size, fformat = st.unpack('<4sI4s', f.read(12))
        if riff != b'RIFF' or fformat != b'WAVE':
            raise Exception("No es un archivo WAV válido.")

        # Leer chunks hasta encontrar 'fmt '
        fmt_chunk_found = False
        data_chunk_found = False

        while not fmt_chunk_found:
            chunk_id, chunk_size = st.unpack('<4sI', f.read(8))
            if chunk_id == b'fmt ':
                fmt_data = f.read(chunk_size)
                fmt_chunk_found = True
            else:
                f.seek(chunk_size, 1)

        audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = st.unpack('<HHIIHH', fmt_data[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise Exception("Este programa solo soporta WAV estéreo PCM de 16 bits.")

        # Leer chunks hasta encontrar 'data'
        while not data_chunk_found:
            chunk_id, chunk_size = st.unpack('<4sI', f.read(8))
            if chunk_id == b'data':
                data_chunk_found = True
                data = f.read(chunk_size)
            else:
                f.seek(chunk_size, 1)

    # Convertir datos binarios a arrays de muestras L y R
    num_samples = len(data) // 4  # 4 bytes por muestra estéreo (2 bytes L + 2 bytes R)
    L = []
    R = []
    mono = []

    for i in range(0, len(data), 4):
        l, r = st.unpack('<hh', data[i:i+4])
        L.append(l)
        R.append(r)
        if canal == 0:
            m = l
        elif canal == 1:
            m = r
        elif canal == 2:
            m = (l + r) // 2
        elif canal == 3:
            m = (l - r) // 2
        else:
            raise ValueError("Canal inválido.")
        mono.append(m)

    # Guardar archivo mono
    muestras_mono = b''.join([st.pack('<h', m) for m in mono])
    subchunk2_size = len(muestras_mono)
    chunk_size = 36 + subchunk2_size

    header = st.pack('<4sI4s', b'RIFF', chunk_size, b'WAVE')
    fmt = st.pack('<4sIHHIIHH', b'fmt ', 16, 1, 1, sample_rate,
                  sample_rate * 2, 2, 16)
    data_header = st.pack('<4sI', b'data', subchunk2_size)

    with open(ficMono, 'wb') as f:
        f.write(header)
        f.write(fmt)
        f.write(data_header)
        f.write(muestras_mono)


def mono2estereo(ficIzq, ficDer, ficEste):
    '''
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales
    izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
    ficEste.
    '''
    def leer_cabecera_y_datos(fic):
        with open(fic, 'rb') as f:
            riff, size, fformat = st.unpack('<4sI4s', f.read(12))
            if riff != b'RIFF' or fformat != b'WAVE':
                raise Exception(f'{fic} no tiene formato WAV válido.')

            # Buscar 'fmt ' chunk
            while True:
                chunk_id, chunk_size = st.unpack('<4sI', f.read(8))
                if chunk_id == b'fmt ':
                    fmt_data = f.read(chunk_size)
                    break
                else:
                    f.seek(chunk_size, 1)

            audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = st.unpack('<HHIIHH', fmt_data[:16])
            if num_channels != 1 or bits_per_sample != 16:
                raise Exception(f'{fic} no es un archivo mono PCM de 16 bits.')

            # Buscar 'data' chunk
            while True:
                chunk_id, chunk_size = st.unpack('<4sI', f.read(8))
                if chunk_id == b'data':
                    data = f.read(chunk_size)
                    break
                else:
                    f.seek(chunk_size, 1)

        return sample_rate, np.frombuffer(data, dtype='<i2')  # Array NumPy 16-bit signed int

    # Leer datos de los dos canales
    fs_L, L = leer_cabecera_y_datos(ficIzq)
    fs_R, R = leer_cabecera_y_datos(ficDer)

    if fs_L != fs_R:
        raise Exception("Las frecuencias de muestreo no coinciden.")
    if len(L) != len(R):
        raise Exception("Los tamaños de los datos no coinciden.")

    num_muestras = len(L)
    tiempo = np.arange(num_muestras) / fs_L

    # Crear datos estéreo intercalados (L, R, L, R, ...)
    intercalado = np.empty((num_muestras * 2,), dtype='<i2')
    intercalado[0::2] = L
    intercalado[1::2] = R
    stereo_bytes = intercalado.tobytes()

    # Guardar archivo estéreo WAV
    subchunk2_size = len(stereo_bytes)
    chunk_size = 36 + subchunk2_size

    with open(ficEste, 'wb') as f:
        f.write(st.pack('<4sI4s', b'RIFF', chunk_size, b'WAVE'))
        f.write(st.pack('<4sIHHIIHH', b'fmt ', 16, 1, 2, fs_L, fs_L * 4, 4, 16))
        f.write(st.pack('<4sI', b'data', subchunk2_size))
        f.write(stereo_bytes)

def codEstereo(ficEste, ficCod):
    '''
    Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
    construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
    monofónicos como por sistemas estéreo preparados para ello.
    '''
    with open(ficEste, 'rb') as f:
        header = f.read(44)
        fmt = '<4sI4s4sIHHIIHH4sI'
        campos = list(st.unpack(fmt, header))

        n_channels = campos[6]
        sample_rate = campos[7]
        bits_per_sample = campos[10]
        data_size = campos[12]

        if n_channels != 2 or bits_per_sample != 16:
            raise Exception("El archivo debe ser estéreo con muestras de 16 bits.")

        n_frames = data_size // (2 * n_channels)
        raw_data = f.read(data_size)
        samples = np.frombuffer(raw_data, dtype='<i2')  # int16

    # Separar canales
    L = samples[::2]
    R = samples[1::2]

    # Codificar (L << 16) | R
    codificados = ((L.astype(np.uint32) & 0xFFFF) << 16) | (R.astype(np.uint32) & 0xFFFF)

    # Guardar como binario
    with open(ficCod, 'wb') as f:
        f.write(st.pack('<' + 'I' * len(codificados), *codificados))

    return sample_rate  # Devolver sample_rate para reutilizar

    

def decEstereo(ficCod, ficEste, sample_rate=44100):
    '''
    Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
    contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
    semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
    ficheros WAVE estéreo.
    '''
    with open(ficCod, 'rb') as f:
        data = f.read()
        codificados = np.frombuffer(data, dtype='<u4')  # uint32

    # Separar L y R
    L = ((codificados >> 16) & 0xFFFF).astype('<i2')
    R = (codificados & 0xFFFF).astype('<i2')

    # Intercalar L y R
    interleaved = np.empty(len(L) * 2, dtype='<i2')
    interleaved[0::2] = L
    interleaved[1::2] = R

    data_bytes = interleaved.tobytes()
    subchunk2_size = len(data_bytes)
    chunk_size = 36 + subchunk2_size
    byte_rate = sample_rate * 2 * 2
    block_align = 2 * 2

    # Escribir cabecera + datos WAV
    header = st.pack('<4sI4s', b'RIFF', chunk_size, b'WAVE')
    header += st.pack('<4sIHHIIHH', b'fmt ', 16, 1, 2, sample_rate, byte_rate, block_align, 16)
    header += st.pack('<4sI', b'data', subchunk2_size)

    with open(ficEste, 'wb') as f:
        f.write(header)
        f.write(data_bytes)


    
