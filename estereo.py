"""
Autor: Pau Reyes Boix

Aquest fitxer conté un recull de funcions per llegir, escriure i transformar fitxers d'àudio WAVE
amb codificació PCM (els típics fitxers de so sense compressió). L'objectiu és poder fer coses com:

- Passar un arxiu estèreo a mono (amb diverses opcions de conversió),
- Tornar-lo a convertir en estèreo a partir de dos canals mono,
- Codificar estèreo en un sol canal de 32 bits,
- I després poder reconstruir-lo.

Funcions:
- llegir_capcalera_wave
- escriure_capcalera_wave
- tractar_mostra
- estereo_a_mono
- mono_a_estereo
- codificar_estereo
- descodificar_estereo
"""

import struct

def llegir_capcalera_wave(f):
    """
    Llegeix la capçalera d'un fitxer WAVE i comprova que sigui del tipus RIFF/WAVE amb PCM.

    Paràmetre:
    - f: fitxer obert en mode binari ('rb')

    Retorna:
    - Un diccionari amb la informació de la capçalera
    """
    if f.read(4) != b'RIFF':
        raise ValueError('No és un fitxer RIFF')
    _ = f.read(4)  # mida del fitxer, no cal de moment
    if f.read(4) != b'WAVE':
        raise ValueError('No és un fitxer WAVE')

    if f.read(4) != b'fmt ':
        raise ValueError('No trobat bloc fmt')
    if struct.unpack('<I', f.read(4))[0] != 16:
        raise ValueError('No és format PCM (esperava 16 bytes)')

    audio_fmt, canals, freq, byte_rate, bloc_align, bits = struct.unpack('<HHIIHH', f.read(16))

    if f.read(4) != b'data':
        raise ValueError('No trobat bloc de dades')
    mida_dades = struct.unpack('<I', f.read(4))[0]

    return {
        'canals': canals,
        'freq_mostreig': freq,
        'bits_per_mostra': bits,
        'data_mida': mida_dades
    }

def escriure_capcalera_wave(f, canals, freq, bits, mida_dades):
    """
    Escriu una capçalera WAVE bàsica (PCM).

    Paràmetres:
    - f: fitxer obert en mode escriptura binària ('wb')
    - canals: 1 per mono, 2 per estèreo
    - freq: freqüència de mostreig (Hz)
    - bits: bits per mostra (16 o 32)
    - mida_dades: mida de les dades d'àudio (en bytes)
    """
    byte_rate = freq * canals * bits // 8
    bloc_align = canals * bits // 8
    mida_total = 36 + mida_dades

    f.write(b'RIFF')
    f.write(struct.pack('<I', mida_total))
    f.write(b'WAVE')
    f.write(b'fmt ')
    f.write(struct.pack('<I', 16))  # mida bloc fmt
    f.write(struct.pack('<HHIIHH', 1, canals, freq, byte_rate, bloc_align, bits))
    f.write(b'data')
    f.write(struct.pack('<I', mida_dades))

def tractar_mostra(mostra, tamany, mode):
    """
    Rep una mostra estèreo (L + R) i retorna la versió mono segons el mode.

    Modes:
    - 0 → canal esquerre
    - 1 → canal dret
    - 2 → (L + R) // 2  → mitjana
    - 3 → (L - R) // 2  → diferència

    Retorna la nova mostra com a bytes.
    """
    L = int.from_bytes(mostra[:tamany], 'little', signed=True)
    R = int.from_bytes(mostra[tamany:], 'little', signed=True)

    if mode == 0:
        val = L
    elif mode == 1:
        val = R
    elif mode == 2:
        val = (L + R) // 2
    elif mode == 3:
        val = (L - R) // 2
    else:
        raise ValueError('Mode de conversió no vàlid')

    return val.to_bytes(tamany, 'little', signed=True)

def estereo_a_mono(fitxer_in, fitxer_out, mode=2):
    """
    Converteix un fitxer estèreo de 16 bits a mono, segons el mode escollit.
    """
    with open(fitxer_in, 'rb') as f:
        cap = llegir_capcalera_wave(f)
        if cap['canals'] != 2 or cap['bits_per_mostra'] != 16:
            raise ValueError('El fitxer no és estèreo de 16 bits')
        dades = f.read(cap['data_mida'])

    tam = cap['bits_per_mostra'] // 8
    mostres = [dades[i:i+2*tam] for i in range(0, len(dades), 2*tam)]
    result = b''.join(tractar_mostra(m, tam, mode) for m in mostres)

    with open(fitxer_out, 'wb') as f_out:
        escriure_capcalera_wave(f_out, 1, cap['freq_mostreig'], cap['bits_per_mostra'], len(result))
        f_out.write(result)

def mono_a_estereo(fitxer_L, fitxer_R, fitxer_out):
    """
    A partir de dos fitxers mono (canal esquerre i dret), crea un fitxer estèreo.
    """
    with open(fitxer_L, 'rb') as fL, open(fitxer_R, 'rb') as fR:
        cap_L = llegir_capcalera_wave(fL)
        cap_R = llegir_capcalera_wave(fR)

        if cap_L != cap_R:
            raise ValueError('Els dos fitxers han de tenir el mateix format')

        dades_L = fL.read(cap_L['data_mida'])
        dades_R = fR.read(cap_R['data_mida'])

    tam = cap_L['bits_per_mostra'] // 8
    mostres = [dades_L[i:i+tam] + dades_R[i:i+tam] for i in range(0, len(dades_L), tam)]

    with open(fitxer_out, 'wb') as f:
        escriure_capcalera_wave(f, 2, cap_L['freq_mostreig'], cap_L['bits_per_mostra'], len(mostres) * 2 * tam)
        for m in mostres:
            f.write(m)

def codificar_estereo(fitxer_est, fitxer_cod):
    """
    Codifica un fitxer estèreo de 16 bits a mono de 32 bits, guardant semisuma i semidiferència.
    """
    with open(fitxer_est, 'rb') as f:
        cap = llegir_capcalera_wave(f)
        if cap['canals'] != 2 or cap['bits_per_mostra'] != 16:
            raise ValueError('Fitxer no vàlid per codificar')
        dades = f.read(cap['data_mida'])

    blocs = [dades[i:i+4] for i in range(0, len(dades), 4)]
    mostres = [struct.unpack('<hh', b) for b in blocs]

    result = []
    for L, R in mostres:
        semisuma = (L + R) // 2
        semidif = (L - R) // 2
        codif = ((semisuma & 0xFFFF) << 16) | (semidif & 0xFFFF)
        result.append(struct.pack('<I', codif))

    result_bytes = b''.join(result)

    with open(fitxer_cod, 'wb') as f_out:
        escriure_capcalera_wave(f_out, 1, cap['freq_mostreig'], 32, len(result_bytes))
        f_out.write(result_bytes)

def to_int16(x):
    """Convenció de valors de 16 bits no signats a signats."""
    return x if x < 0x8000 else x - 0x10000

def saturar16(x):
    """Evita desbordaments limitant entre -32768 i 32767."""
    return max(-32768, min(32767, x))

def descodificar_estereo(fitxer_cod, fitxer_out):
    """
    Fa la inversa de la codificació: a partir del mono de 32 bits, torna a tenir dos canals de 16.
    """
    with open(fitxer_cod, 'rb') as f:
        cap = llegir_capcalera_wave(f)
        if cap['canals'] != 1 or cap['bits_per_mostra'] != 32:
            raise ValueError('Fitxer no vàlid per descodificar')
        dades = f.read(cap['data_mida'])

    blocs = [struct.unpack('<I', dades[i:i+4])[0] for i in range(0, len(dades), 4)]
    mostres = []
    for b in blocs:
        semisuma = b >> 16
        semidif = to_int16(b & 0xFFFF)
        L = saturar16(semisuma + semidif)
        R = saturar16(semisuma - semidif)
        mostres.append(struct.pack('<hh', L, R))

    with open(fitxer_out, 'wb') as f_out:
        escriure_capcalera_wave(f_out, 2, cap['freq_mostreig'], 16, len(mostres) * 4)
        f_out.write(b''.join(mostres))
