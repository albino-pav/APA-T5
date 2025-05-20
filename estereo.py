"""
Biel Bernal Pratdesaba

Aquest fitxer conté les funcions per al tractament d'àudio estèreo en format WAVE:
- Conversió d'àudio estèreo a mono (estereo2mono)
- Conversió d'àudio mono a estèreo (mono2stereo)
- Codificació d'àudio estèreo en una sola pista de 32 bits (codEstereo)
- Decodificació d'àudio mono de 32 bits en dues pistes estèreo (decEstereo)
"""
import struct as st

def estereo2mono(ficEste, ficMono, canal=2):
    """
    La funció llegeix el fitxer ficEste, que ha de contenir un senyal estèreo, i escriu el fitxer 
    ficMono, amb un senyal monofònic. El tipus concret de senyal que s'emmagatzemarà a ficMono
    depèn de l'argument canal:

    - canal=0: S'emmagatzema el canal esquerre (L).
    - canal=1: S'emmagatzema el canal dret (R).
    - canal=2: S'emmagatzema la semisuma (L + R) / 2.
    - canal=3: S'emmagatzema la semidiferència (L - R) / 2.

    """

    with open(ficEste, "rb") as fpEste:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpEste.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpEste.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpEste.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 2 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, estèreo i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpEste.seek(36, 0)
        formato = "<4sI"
        datos = fpEste.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpEste.read(st.calcsize(formato))
        mostres = st.unpack(formato, dades)

    # Passem de stereo a mono
    mostStereo = list(zip(mostres[::2], mostres[1::2]))
    if canal == 0:
        senyalMono = [L for L, R in mostStereo]
    elif canal == 1:
        senyalMono = [R for L, R in mostStereo]
    elif canal == 2:
        senyalMono = [(L + R) // 2 for L, R in mostStereo]
    elif canal == 3:
        senyalMono = [(L - R) // 2 for L, R in mostStereo]
    else:
        raise ValueError("El canal ha de ser 0, 1, 2 o 3")
    
    # Calcular mides per la capçalera mono
    subChunk2SizeMono = len(senyalMono) * 2
    chunkSizeMono = 36 + subChunk2SizeMono

    # Escriure el nou fitxer 
    with open(ficMono, "wb") as fpMono:
        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        fpMono.write(st.pack(formato, b"RIFF", chunkSizeMono, b"WAVE"))

        # Subchunk1 (fmt)
        formato = "<4sIHHIIHH"
        fpMono.write(st.pack(formato, b"fmt ", 16, 1, 1,
                             sampleRate, sampleRate * 2, 2, 16))

        # Subchunk2 (data)
        formato = "<4sI"
        fpMono.write(st.pack(formato, b"data", subChunk2SizeMono))

        # Dades mono
        formato = f"<{len(senyalMono)}h"
        fpMono.write(st.pack(formato, *senyalMono))
    


def mono2stereo(ficIzq, ficDer, ficEste):
    """
    Llegeix els fitxers ficIzq i ficDer, que contenen els senyals monofònics corresponents als
    canals esquerre i dret, respectivament, i construeix amb ells un senyal estèreo que s'emmagatzema 
    al fitxer ficEste.

    """

    # Llegir el fitxer del canal L
    with open(ficIzq, "rb") as fpIzq:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpIzq.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpIzq.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpIzq.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRateL, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, mono i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpIzq.seek(36, 0)
        formato = "<4sI"
        datos = fpIzq.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # Nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpIzq.read(st.calcsize(formato))
        mostresL = st.unpack(formato, dades)

    # Llegir el fitxer del canal R
    with open(ficDer, "rb") as fpDer:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpDer.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpDer.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpDer.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRateR, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, mono i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpDer.seek(36, 0)
        formato = "<4sI"
        datos = fpDer.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres mono
        numMostres = subChunk2Size // 2  # Nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpDer.read(st.calcsize(formato))
        mostresR = st.unpack(formato, dades)

    # Comvinem les mostres en una sola senyal de 2 canals
    mostresStereo = []
    for L, R in zip(mostresL, mostresR):
        mostresStereo.append(L)
        mostresStereo.append(R)

    # Calcular mides per la capçalera stereo
    subChunk2SizeStereo = len(mostresStereo) * 2
    chunkSizeStereo = 36 + subChunk2SizeStereo

    # Escriure el nou fitxer 
    with open(ficEste, "wb") as fpEste:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpEste.write(st.pack(formato, b"RIFF", chunkSizeStereo, b"WAVE"))

        # Subchunk1 'fmt ' (estèreo, 2 canals, 16 bits)
        formato = "<4sIHHIIHH"
        fpEste.write(st.pack(formato, b"fmt ", 16, 1, 2, sampleRateL, sampleRateL * 4, 4, 16))

        # Subchunk2 'data'
        formato = "<4sI"
        fpEste.write(st.pack(formato, b"data", subChunk2SizeStereo))

        # Mostres
        formato = f"<{len(mostresStereo)}h"
        fpEste.write(st.pack(formato, *mostresStereo))


def codEstereo(ficEste, ficCod):
    """
    Llegeix un fitxer WAVE estèreo de 16 bits i genera un fitxer mono de 32 bits on:
    - Els 16 bits alts contenen la semisuma (L+R)//2
    - Els 16 bits baixos contenen la semidiferència (L-R)//2
    """
    with open(ficEste, "rb") as fpEste:
        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpEste.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpEste.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpEste.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 2 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, estèreo i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpEste.seek(36, 0)
        formato = "<4sI"
        datos = fpEste.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpEste.read(st.calcsize(formato))
        mostres = st.unpack(formato, dades)

    # Codifiquem les mostres L, R en 32 bits
    codificats = []
    for R, L in zip(mostres[::2], mostres[1::2]):
        semisuma = (L + R) // 2
        semidiferencia = (L - R) // 2
        valor32bits = st.unpack("<I", st.pack("<hh", semisuma, semidiferencia))[0]
        codificats.append(valor32bits) 
    
    subChunk2Size = len(codificats) * 4  # 4 bytes per mostra
    chunkSize = 36 + subChunk2Size

    with open(ficCod, "wb") as fpCod:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpCod.write(st.pack(formato, b"RIFF", chunkSize, b"WAVE"))

        # Subchunk1 'fmt ' (PCM 32 bits mono)
        formato = "<4sIHHIIHH"
        fpCod.write(st.pack(formato, b"fmt ", 16, 1, 1,
                            sampleRate, sampleRate * 4, 4, 32))

        # Subchunk2 'data'
        formato = "<4sI"
        fpCod.write(st.pack(formato, b"data", subChunk2Size))

        # Dades codificades (32 bits unsigned int)
        formato = f"<{len(codificats)}I"
        fpCod.write(st.pack(formato, *codificats))


def decEstereo(ficCod, ficEste):
    """
    Llegeix un fitxer WAVE mono de 32 bits amb semisuma i semidiferència codificades,
    i reconstrueix un fitxer estèreo de 16 bits amb els canals esquerre i dret originals.
    """
    with open(ficCod, "rb") as fpCod:
        # Capçalera RIFF
        formato = "<4sI4s"
        dades = fpCod.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, dades)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"{ficCod} no és un fitxer WAVE vàlid.")

        # Subchunk1 'fmt '
        fpCod.seek(12)
        formato = "<4sIHHIIHH"
        dades = fpCod.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, dades)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 32:
            raise Exception("El fitxer ha de ser mono, PCM i de 32 bits.")

        # Subchunk2 'data'
        fpCod.seek(36)
        formato = "<4sI"
        dades = fpCod.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, dades)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")

        # Llegim les mostres codificades (32 bits cada una)
        numMostres = subChunk2Size // 4
        formato = f"<{numMostres}I"
        dades = fpCod.read(st.calcsize(formato))
        codificats = st.unpack(formato, dades)

    # Reconstruïm L i R
    mostresStereo = []
    for cod in codificats:
        bytes32 = st.pack("<I", cod)
        semisuma, semidiferencia = st.unpack("<hh", bytes32)
        L = semisuma + semidiferencia
        R = semisuma - semidiferencia
        mostresStereo.extend([R, L])  

    # Capçaleres del fitxer estèreo (16 bits, 2 canals)
    subChunk2SizeStereo = len(mostresStereo) * 2
    chunkSizeStereo = 36 + subChunk2SizeStereo

    with open(ficEste, "wb") as fpEste:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpEste.write(st.pack(formato, b"RIFF", chunkSizeStereo, b"WAVE"))

        # Subchunk1 'fmt '
        formato = "<4sIHHIIHH"
        fpEste.write(st.pack(formato, b"fmt ", 16, 1, 2,
                             sampleRate, sampleRate * 4, 4, 16))

        # Subchunk2 'data'
        formato = "<4sI"
        fpEste.write(st.pack(formato, b"data", subChunk2SizeStereo))

        # Dades L-R de 16 bits
        formato = f"<{len(mostresStereo)}h"
        fpEste.write(st.pack(formato, *mostresStereo))