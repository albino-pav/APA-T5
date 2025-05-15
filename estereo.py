"""   
    Quinta tarea de APA - Sonido estéreo y ficheros WAVE

    Àlex Segura

    Esta tarea consiste en implementar funciones para convertir entre
    ficheros estéreo y mono en formato WAVE, así como para codificar
    y decodificar señales estéreo en un formato compatible con sistemas
    monofónicos.

"""

import struct

# Funcion para pasar una archivo de estéreo a mono
def estereo2mono(ficEste, ficMono, canal = 2):

    """
    
    Convierte un archivo WAVE estéreo a mono en función del canal indicado:
    0 = izquierdo, 1 = derecho, 2 = semisuma, 3 = semidiferencia.

    """
    with open(ficEste, 'rb') as fe:
        cabecera = fe.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido")

        fmt_tag, n_channels, sample_rate, byte_rate, block_align, bps = struct.unpack('<HHIIHH', cabecera[20:36])
        if n_channels != 2 or fmt_tag != 1 or bps != 16:
            raise ValueError("El fichero no es estéreo o no usa PCM lineal de 16 bits")

        data_size = struct.unpack('<I', cabecera[40:44])[0]
        num_frames = data_size // 4  # 4 bytes por muestra estéreo (2 bytes por canal)
        datos = fe.read()

    muestras = struct.unpack('<' + 'hh'*num_frames, datos)
    if canal == 0:
        canal_mono = [muestras[i] for i in range(0, len(muestras), 2)]
    elif canal == 1:
        canal_mono = [muestras[i] for i in range(1, len(muestras), 2)]
    elif canal == 2:
        canal_mono = [(muestras[i] + muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
    elif canal == 3:
        canal_mono = [(muestras[i] - muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
    else:
        raise ValueError("Parámetro 'canal' no válido. Usa 0, 1, 2 o 3.")

    nuevo_data_size = len(canal_mono) * 2  # 2 bytes por muestra
    nuevo_byte_rate = sample_rate * 2
    nuevo_block_align = 2
    with open(ficMono, 'wb') as fm:
        fm.write(b'RIFF')
        fm.write(struct.pack('<I', 36 + nuevo_data_size))
        fm.write(b'WAVE')
        fm.write(b'fmt ')
        fm.write(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate,
                             nuevo_byte_rate, nuevo_block_align, 16))
        fm.write(b'data')
        fm.write(struct.pack('<I', nuevo_data_size))
        fm.write(struct.pack('<' + 'h'*len(canal_mono), *canal_mono))


# Funcion para convertir dos archivos mono a uno estéreo
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Genera un archivo WAVE estéreo combinando dos archivos WAVE mono.

    Cada archivo debe tener el mismo número de muestras, frecuencia de muestreo
    y formato (PCM 16-bit). El canal izquierdo se toma de ficIzq y el derecho de ficDer.
    
    """
    with open(ficIzq, 'rb') as fz:
        header_izq = fz.read(44)
        if header_izq[0:4] != b'RIFF' or header_izq[8:12] != b'WAVE':
            raise ValueError("ficIzq no es un fichero WAVE válido")
        fmt_tag, nchannels, sample_rate, _, _, bps = struct.unpack('<HHIIHH', header_izq[20:36])
        if nchannels != 1 or fmt_tag != 1 or bps != 16:
            raise ValueError("ficIzq no es un fichero mono PCM 16-bit válido")
        data_izq = fz.read()

    with open(ficDer, 'rb') as fd:
        header_der = fd.read(44)
        if header_der[0:4] != b'RIFF' or header_der[8:12] != b'WAVE':
            raise ValueError("ficDer no es un fichero WAVE válido")
        fmt_tag_d, nchannels_d, sample_rate_d, _, _, bps_d = struct.unpack('<HHIIHH', header_der[20:36])
        if nchannels_d != 1 or fmt_tag_d != 1 or bps_d != 16:
            raise ValueError("ficDer no es un fichero mono PCM 16-bit válido")
        if sample_rate_d != sample_rate or bps_d != bps:
            raise ValueError("Los ficheros mono no tienen la misma configuración")
        data_der = fd.read()

    muestras_izq = struct.unpack('<' + 'h' * (len(data_izq) // 2), data_izq)
    muestras_der = struct.unpack('<' + 'h' * (len(data_der) // 2), data_der)
    if len(muestras_izq) != len(muestras_der):
        raise ValueError("Los ficheros mono no tienen el mismo número de muestras")

    intercaladas = [val for pair in zip(muestras_izq, muestras_der) for val in pair]
    data_size = len(intercaladas) * 2  # 2 bytes por muestra
    byte_rate = sample_rate * 4        # 2 canales x 2 bytes
    block_align = 4                    # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        fe.write(b'RIFF')
        fe.write(struct.pack('<I', 36 + data_size))
        fe.write(b'WAVE')
        fe.write(b'fmt ')
        fe.write(struct.pack('<IHHIIHH', 16, 1, 2, sample_rate,
                             byte_rate, block_align, 16))
        fe.write(b'data')
        fe.write(struct.pack('<I', data_size))
        fe.write(struct.pack('<' + 'h' * len(intercaladas), *intercaladas))


# Funcion para codificar un archivo estéreo a mono con diferencias
def codEstereo(ficEste, ficCod):
    """

    Lee un fichero estéreo de 16 bits por canal (ficEste) y genera un fichero ficCod
    de 32 bits por muestra codificando:
    - Semisuma (L + R) // 2 en los 16 bits más significativos
    - Semidiferencia (L - R) // 2 en los 16 bits menos significativos

    El resultado permite ser reproducido como mono (semisuma) o reconstruido como estéreo.
    """
    with open(ficEste, 'rb') as f:
        cabecera = f.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido.")
        fmt = cabecera[20:22]
        nchannels = struct.unpack('<H', cabecera[22:24])[0]
        sampwidth = struct.unpack('<H', cabecera[34:36])[0]

        if fmt != b'\x01\x00' or nchannels != 2 or sampwidth != 16:
            raise ValueError("El fichero debe ser PCM, estéreo, 16 bits por muestra.")

        datos = f.read()

    # Extraer muestras como enteros de 16 bits
    muestras = struct.unpack('<' + 'h'*(len(datos)//2), datos)
    left = muestras[::2]
    right = muestras[1::2]

    # Calcular semisuma y semidiferencia
    sumas = [(l + r) // 2 for l, r in zip(left, right)]
    diffs = [(l - r) // 2 for l, r in zip(left, right)]

    # Combinar en 32 bits (semisuma << 16) | (semidiferencia & 0xFFFF)
    samples_32bit = [(suma << 16) | (diff & 0xFFFF) for suma, diff in zip(sumas, diffs)]

    # Crear nueva cabecera WAVE para 1 canal, 32 bits por muestra
    nuevo_num_channels = 1
    nuevo_bits_per_sample = 32
    sample_rate = struct.unpack('<I', cabecera[24:28])[0]
    byte_rate = sample_rate * nuevo_num_channels * nuevo_bits_per_sample // 8
    block_align = nuevo_num_channels * nuevo_bits_per_sample // 8
    data_size = len(samples_32bit) * 4
    chunk_size = 36 + data_size

    nueva_cabecera = (
        b'RIFF' +
        struct.pack('<I', chunk_size) +
        b'WAVE' +
        b'fmt ' +
        struct.pack('<I', 16) +             # Subchunk1Size
        struct.pack('<H', 1) +              # AudioFormat: PCM
        struct.pack('<H', nuevo_num_channels) +
        struct.pack('<I', sample_rate) +
        struct.pack('<I', byte_rate) +
        struct.pack('<H', block_align) +
        struct.pack('<H', nuevo_bits_per_sample) +
        b'data' +
        struct.pack('<I', data_size)
    )

    with open(ficCod, 'wb') as f:
        f.write(nueva_cabecera)
        f.write(struct.pack('<' + 'i'*len(samples_32bit), *samples_32bit))



# Funcion para decodificar un archivo codificado a estéreo 
def decEstereo(ficCod, ficEste):
    """
    decEstereo(ficCod, ficEste)

    Decodifica un fichero codificado en 32 bits por muestra (ficCod), donde:
    - Los 16 bits más significativos contienen la semisuma (L + R) // 2
    - Los 16 bits menos significativos contienen la semidiferencia (L - R) // 2
    para obtener los canales izquierdo y derecho originales.

    Guarda el resultado en un fichero estéreo de 16 bits por muestra (ficEste).
    """
    with open(ficCod, 'rb') as f:
        cabecera = f.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido.")

        num_channels = struct.unpack('<H', cabecera[22:24])[0]
        bits_per_sample = struct.unpack('<H', cabecera[34:36])[0]

        if num_channels != 1 or bits_per_sample != 32:
            raise ValueError("El fichero debe tener 1 canal y 32 bits por muestra.")

        sample_rate = struct.unpack('<I', cabecera[24:28])[0]
        data = f.read()

    muestras_32bit = struct.unpack('<' + 'i' * (len(data) // 4), data)

    semisumas = [(m >> 16) for m in muestras_32bit]
    semidiffs = [((m & 0xFFFF) ^ 0x8000) - 0x8000 for m in muestras_32bit]  # Convertir a signed short

    left = [s + d for s, d in zip(semisumas, semidiffs)]
    right = [s - d for s, d in zip(semisumas, semidiffs)]

    # Crear nueva cabecera WAVE para 2 canales de 16 bits
    nuevo_num_channels = 2
    nuevo_bits_per_sample = 16
    byte_rate = sample_rate * nuevo_num_channels * nuevo_bits_per_sample // 8
    block_align = nuevo_num_channels * nuevo_bits_per_sample // 8
    data_size = len(left) * 2 * 2  # 2 canales * 2 bytes por muestra
    chunk_size = 36 + data_size

    nueva_cabecera = (
        b'RIFF' +
        struct.pack('<I', chunk_size) +
        b'WAVE' +
        b'fmt ' +
        struct.pack('<I', 16) +
        struct.pack('<H', 1) +
        struct.pack('<H', nuevo_num_channels) +
        struct.pack('<I', sample_rate) +
        struct.pack('<I', byte_rate) +
        struct.pack('<H', block_align) +
        struct.pack('<H', nuevo_bits_per_sample) +
        b'data' +
        struct.pack('<I', data_size)
    )

    # Intercalar las muestras L y R
    intercaladas = [val for par in zip(left, right) for val in par]

    with open(ficEste, 'wb') as f:
        f.write(nueva_cabecera)
        f.write(struct.pack('<' + 'h' * len(intercaladas), *intercaladas))
