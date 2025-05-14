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


