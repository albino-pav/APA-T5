"""
estereo.py

Autor: Sebastian Pérez Capitano

Descripción: Funciones para manipular señales estéreo en formato WAVE,
incluyendo conversión mono-estéreo y codificación/decodificación
compatibles con sistemas monofónicos.
"""

import struct

def leer_cabecera(f):
    riff, size, wave = struct.unpack('<4sI4s', f.read(12))
    if riff != b'RIFF' or wave != b'WAVE':
        raise ValueError("Formato incorrecto: no es un fichero WAVE.")
    
    cabeceras = []
    while True:
        chunk = f.read(8)
        if len(chunk) < 8:
            break
        subchunk_id, subchunk_size = struct.unpack('<4sI', chunk)
        data = f.read(subchunk_size)
        cabeceras.append((subchunk_id, subchunk_size, data))
        if subchunk_id == b'data':
            break
    return size, cabeceras

def escribir_cabecera(f, subchunks):
    total_size = 4 + sum(8 + len(data) for _, _, data in subchunks)
    f.write(struct.pack('<4sI4s', b'RIFF', total_size, b'WAVE'))
    for chunk_id, _, data in subchunks:
        f.write(struct.pack('<4sI', chunk_id, len(data)))
        f.write(data)

def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste, 'rb') as f:
        size, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El fichero no contiene audio estéreo de 16 bits.")
        data_chunk = next(c for c in chunks if c[0] == b'data')
        datos = data_chunk[2]
        muestras = struct.unpack('<' + 'h' * (len(datos) // 2), datos)
        izq = muestras[::2]
        der = muestras[1::2]
        
        if canal == 0:
            mono = izq
        elif canal == 1:
            mono = der
        elif canal == 2:
            mono = [((l + r) // 2) for l, r in zip(izq, der)]
        elif canal == 3:
            mono = [((l - r) // 2) for l, r in zip(izq, der)]
        else:
            raise ValueError("Canal debe ser 0 (izq), 1 (der), 2 (L+R)/2, o 3 (L-R)/2.")

        datos_mono = struct.pack('<' + 'h'*len(mono), *mono)
        fmt_mono = struct.pack('<HHIIHH', audio_format, 1, sample_rate, sample_rate*2, 2, 16) + fmt[16:]
        with open(ficMono, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_mono), fmt_mono),
                (b'data', len(datos_mono), datos_mono)
            ])

def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq, 'rb') as f1, open(ficDer, 'rb') as f2:
        _, c1 = leer_cabecera(f1)
        _, c2 = leer_cabecera(f2)
        fmt1 = next(c for c in c1 if c[0] == b'fmt ')[2]
        fmt2 = next(c for c in c2 if c[0] == b'fmt ')[2]
        if fmt1 != fmt2:
            raise ValueError("Los ficheros mono no tienen el mismo formato.")
        datos1 = struct.unpack('<' + 'h'*(len(c1[-1][2]) // 2), c1[-1][2])
        datos2 = struct.unpack('<' + 'h'*(len(c2[-1][2]) // 2), c2[-1][2])
        if len(datos1) != len(datos2):
            raise ValueError("Los ficheros mono no tienen la misma longitud.")
        intercalado = [val for pair in zip(datos1, datos2) for val in pair]
        datos_stereo = struct.pack('<' + 'h'*len(intercalado), *intercalado)
        audio_format, _, sample_rate, _, _, _ = struct.unpack('<HHIIHH', fmt1[:16])
        fmt_stereo = struct.pack('<HHIIHH', audio_format, 2, sample_rate, sample_rate*4, 4, 16) + fmt1[16:]
        with open(ficEste, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_stereo), fmt_stereo),
                (b'data', len(datos_stereo), datos_stereo)
            ])

def codEstereo(ficEste, ficCod):
    with open(ficEste, 'rb') as f:
        _, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El fichero debe ser estéreo y de 16 bits.")
        datos = struct.unpack('<' + 'h'*(len(chunks[-1][2]) // 2), chunks[-1][2])
        L = datos[::2]
        R = datos[1::2]
        cod = [(int(((l + r) // 2) << 16) | ((l - r) // 2 & 0xFFFF)) for l, r in zip(L, R)]
        datos_cod = struct.pack('<' + 'i'*len(cod), *cod)
        fmt_cod = struct.pack('<HHIIHH', 1, 1, sample_rate, sample_rate*4, 4, 32) + fmt[16:]
        with open(ficCod, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_cod), fmt_cod),
                (b'data', len(datos_cod), datos_cod)
            ])

def decEstereo(ficCod, ficEste):
    with open(ficCod, 'rb') as f:
        _, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 1 or bits_per_sample != 32:
            raise ValueError("El fichero debe ser mono de 32 bits.")
        datos = struct.unpack('<' + 'i'*(len(chunks[-1][2]) // 4), chunks[-1][2])
        L = []
        R = []
        for val in datos:
            sum_ = (val >> 16)
            diff = val & 0xFFFF
            if diff >= 0x8000:
                diff -= 0x10000  # signo
            L.append(sum_ + diff)
            R.append(sum_ - diff)
        intercalado = [val for pair in zip(L, R) for val in pair]
        datos_estereo = struct.pack('<' + 'h'*len(intercalado), *intercalado)
        fmt_stereo = struct.pack('<HHIIHH', 1, 2, sample_rate, sample_rate*4, 4, 16) + fmt[16:]
        with open(ficEste, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_stereo), fmt_stereo),
                (b'data', len(datos_estereo), datos_estereo)
            ])
