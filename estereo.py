"""
estereo.py
Nom i cognoms: Josep Esquerra bayo

Aquest mòdul proporciona funcions per al maneig de fitxers WAVE estèreo, permetent:
- Convertir les senyals estèreo a mono.
- Construir uns fitxers estèreo a partir de canals mono.
- Codificar senyals estèreo en 32 bits.
- Decodificar fitxers codificats en 32 bits per recuperar els canals esquerre i dret.
"""

import struct

def _read_wave_header(f):
    # lectura dels primers bytes
    riff, size, wave = struct.unpack('<4sI4s', f.read(12))
    # Certificació del format Wav
    if riff != b'RIFF' or wave != b'WAVE':
        raise ValueError("No és un fitxer WAVE vàlid.")
    # declaració del valor
    chunks = {}
    #localització i emmagatzematge de la fmt i la data
    while True:
        header = f.read(8)
        if not header:
            break
        chunk_id, chunk_size = struct.unpack('<4sI', header)
        chunks[chunk_id] = (f.tell(), chunk_size)
        f.seek(chunk_size, 1)
    #retorn dels valors
    return chunks

def _read_fmt_chunk(f, offset):
    f.seek(offset)
    # lectura de les dades que descriuen el fitxer llegit
    data = f.read(16)
    return struct.unpack('<HHIIHH', data)

def estereo2mono(ficEste, ficMono, canal=2):
    # lectura binaria
    with open(ficEste, 'rb') as f:
        # proces executat anteriorment
        chunks = _read_wave_header(f)
        # sertificar de que el fitxer és estereo
        if b'fmt ' not in chunks or b'data' not in chunks:
            raise ValueError("Falten els chunks essencials.")
        #buscar data
        fmt_offset, _ = chunks[b'fmt ']
        audio_fmt, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = _read_fmt_chunk(f, fmt_offset)
        # càlcul previ per a la rectura de les dades
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("Només es permet estèreo amb 16 bits per mostra.")

        # desenpaquetat de les dades
        data_offset, data_size = chunks[b'data']
        f.seek(data_offset)
        raw_data = f.read(data_size)
        samples = struct.unpack('<' + 'h' * (data_size // 2), raw_data)

    # Conversió a mono depent del nombre de canals [1, 2, 3, 4]
    L, R = samples[::2], samples[1::2]
    if canal == 0:
        mono = L
    elif canal == 1:
        mono = R
    elif canal == 2:
        mono = [(l + r) // 2 for l, r in zip(L, R)]
    elif canal == 3:
        mono = [(l - r) // 2 for l, r in zip(L, R)]
    else:
        raise ValueError("Canal ha de ser 0, 1, 2 o 3.")
    
    # empaquetat de les dades i escritura del nou fitxer mono
    byte_data = struct.pack('<' + 'h' * len(mono), *mono)
    with open(ficMono, 'wb') as out:
        # Header
        out.write(struct.pack('<4sI4s', b'RIFF', 36 + len(byte_data), b'WAVE'))
        out.write(struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, 1, sample_rate,
                              sample_rate * 2, 2, 16))
        out.write(struct.pack('<4sI', b'data', len(byte_data)))
        out.write(byte_data)

def mono2estereo(ficIzq, ficDer, ficEste):
    def read_mono(fic):
        # lectura del fitxer
        with open(fic, 'rb') as f:
            # dades del cap del fitxer
            chunks = _read_wave_header(f)
            # Certificació de les dades
            if b'fmt ' not in chunks or b'data' not in chunks:
                raise ValueError("Falten els chunks essencials.")
            # Calculs prèvis
            fmt_offset, _ = chunks[b'fmt ']
            fmt = _read_fmt_chunk(f, fmt_offset)
            if fmt[1] != 1 or fmt[5] != 16:
                raise ValueError("Només es permet mono amb 16 bits per mostra.")
            # cerca de les dades a obtindre
            data_offset, data_size = chunks[b'data']
            f.seek(data_offset)
            raw = f.read(data_size)
            return struct.unpack('<' + 'h' * (data_size // 2), raw), fmt[2]

    L, rateL = read_mono(ficIzq)
    R, rateR = read_mono(ficDer)
    # Càlculs del nobmre de mostres
    if rateL != rateR or len(L) != len(R):
        raise ValueError("Els fitxers mono han de tenir la mateixa taxa i longitud.")
    intercalat = [s for pair in zip(L, R) for s in pair]
    # Desempaquetat de les mostres
    byte_data = struct.pack('<' + 'h' * len(intercalat), *intercalat)

    # empaquetat de les mostres estereo i escritura del nou fitxer WAV estèreo
    with open(ficEste, 'wb') as out:
        out.write(struct.pack('<4sI4s', b'RIFF', 36 + len(byte_data), b'WAVE'))
        out.write(struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, 2, rateL,
                              rateL * 4, 4, 16))
        out.write(struct.pack('<4sI', b'data', len(byte_data)))
        out.write(byte_data)

def codEstereo(ficEste, ficCod):
    # lectura del fitxer en binari
    with open(ficEste, 'rb') as f:
        # llegir i localitzar la fmt i la data
        chunks = _read_wave_header(f)
        fmt_offset, _ = chunks[b'fmt ']
        audio_fmt, num_channels, sample_rate, _, _, bits_per_sample = _read_fmt_chunk(f, fmt_offset)
        # fem els calculs posteriors per tractar les dades correctament
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El fitxer ha de ser estèreo de 16 bits.")
        # agafem les dades
        data_offset, data_size = chunks[b'data']
        f.seek(data_offset)
        # desenpaquetem les mostres estèreo
        samples = struct.unpack('<' + 'h' * (data_size // 2), f.read(data_size))

    # Apliquem la codificació assignada en l'activitat
    L, R = samples[::2], samples[1::2]
    codificats = [((l + r) << 16) | ((l - r) & 0xFFFF) for l, r in zip(L, R)]
    byte_data = struct.pack('<' + 'i' * len(codificats), *codificats)

    # Escribim el nou model Wav estereo
    with open(ficCod, 'wb') as out:
        out.write(struct.pack('<4sI4s', b'RIFF', 36 + len(byte_data), b'WAVE'))
        out.write(struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, 1, sample_rate,
                              sample_rate * 4, 4, 32))
        out.write(struct.pack('<4sI', b'data', len(byte_data)))
        out.write(byte_data)

def decEstereo(ficCod, ficEste):
    # lectura del fitxer en binari
    with open(ficCod, 'rb') as f:
        # aconseguim size i localització de la fmt i les dades
        chunks = _read_wave_header(f)
        # Certifiquem els valors rebuts
        fmt_offset, _ = chunks[b'fmt ']
        fmt = _read_fmt_chunk(f, fmt_offset)
        # apliquem uns càlculs inicials per al tractament de les dades
        if fmt[1] != 1 or fmt[5] != 32:
            raise ValueError("Cal un fitxer mono de 32 bits.")
        # Cerca de les dades de audio i la seva lectura
        sample_rate = fmt[2]
        data_offset, data_size = chunks[b'data']
        f.seek(data_offset)
        # càlcul del nombre de mostres
        codificats = struct.unpack('<' + 'i' * (data_size // 4), f.read(data_size))

    # descodificar el fitxer segons el valor de codificació entrats com a input
    L = [((x >> 16) + ((x & 0xFFFF) if (x & 0x8000) == 0 else (x & 0xFFFF) - 0x10000)) // 2 for x in codificats]
    R = [((x >> 16) - ((x & 0xFFFF) if (x & 0x8000) == 0 else (x & 0xFFFF) - 0x10000)) // 2 for x in codificats]
    intercalat = [s for pair in zip(L, R) for s in pair]
    # desempaquetat de les mostres estèreo
    byte_data = struct.pack('<' + 'h' * len(intercalat), *intercalat)

    # Escritura del nou fitxer Wav Estèreo
    with open(ficEste, 'wb') as out:
        out.write(struct.pack('<4sI4s', b'RIFF', 36 + len(byte_data), b'WAVE'))
        out.write(struct.pack('<4sIHHIIHH', b'fmt ', 16, 1, 2, sample_rate,
                              sample_rate * 4, 4, 16))
        out.write(struct.pack('<4sI', b'data', len(byte_data)))
        out.write(byte_data)
