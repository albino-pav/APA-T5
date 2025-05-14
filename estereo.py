"""   
    Quinta tarea de APA - Sonido estéreo y ficheros WAVE

    Àlex Segura

"""

import struct

def estereo2mono(ficEste, ficMono, canal = 2):

    """Convierte un archivo WAVE estéreo a mono en función del canal indicado:
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


def mono2estereo(ficIzq, ficDer, ficEste):
    """Genera un archivo WAVE estéreo combinando dos archivos WAVE mono.

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


def decEstereo(ficCodif, ficEste):
    """Decodifica un archivo mono codificado diferencialmente a estéreo PCM 16-bit.

    ficCodif debe contener las diferencias dL, dR. El resultado se guarda en ficEste.
    """
    with open(ficCodif, 'rb') as f:
        cabecera = f.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("ficCodif no es un fichero WAVE válido")

        fmt_tag, nchannels, sample_rate, _, _, bps = struct.unpack('<HHIIHH', cabecera[20:36])
        if fmt_tag != 1 or nchannels != 1 or bps != 16:
            raise ValueError("ficCodif no es mono PCM 16-bit")

        data = f.read()

    diffs = struct.unpack('<' + 'h' * (len(data) // 2), data)
    if len(diffs) % 2 != 0:
        raise ValueError("Número impar de diferencias. Se esperaban pares dL, dR")

    # Reconstrucción de L y R: L = (dL + dR)/2, R = (dR + dL)/2 (equivalente)
    canal_izq = [(dl - dr) // 2 for dl, dr in zip(diffs[::2], diffs[1::2])]
    canal_der = [(dr - dl) // 2 for dl, dr in zip(diffs[::2], diffs[1::2])]

    intercalado = [val for par in zip(canal_izq, canal_der) for val in par]
    data_size = len(intercalado) * 2
    byte_rate = sample_rate * 4  # 2 canales * 2 bytes
    block_align = 4

    with open(ficEste, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<IHHIIHH', 16, 1, 2, sample_rate,
                            byte_rate, block_align, 16))
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        f.write(struct.pack('<' + 'h' * len(intercalado), *intercalado))
