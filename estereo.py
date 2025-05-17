"""
Biel Bernal Pratdesaba


"""
import struct as st
import matplotlib.pyplot as plt
import numpy as np
import struct as st

def estereo2mono(ficEste, ficMono, canal=2):
    with open(ficEste, "rb") as fpEste:
        formato = "<4sI4s"
        datos = fpEste.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {fpEste} no te un format WAVE")
        fpEste.seek(36, 0)
        formato = "<4sI"
        datos = fpEste.read(st.calcsize(format))
        subChunkID, subChunkSize, format = st.unpack(formato, datos)
        numMostres = subChunkSize // 2

        formato = f"<{numMostres}h"
        datos = fpEste.read(st.calcsize(formato))
        mostres = st.unpack(formato, datos)
    return mostres
