import struct as st

def estereo2mono(ficEste, ficMono, canal=2):

    with open(ficEste, 'rb') as fpwave:
        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)
        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es .wav') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        if numchannels != 2 :
             raise Exception('Fichero no estereo') from None
        
        if canal not in [0,1,2,3]:
             raise Exception('Canal no válido') from None


        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign

        formato = f'<{nummuestras*2}h'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datos = st.unpack(formato,buffer4)

         

    #Salida
    with open(ficMono,'wb') as fout :

        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * blockalign, b'WAVE', b'fmt ', 16, 1, 1, samplerate, byterate // numchannels , blockalign // numchannels, bitspersample, b'data', nummuestras * 2)
        pack1 =  st.pack(cabecera_fmt, *cabecera)
        fout.write(pack1)

        if bitspersample==16 : formato = 'h'
        else : formato = 'b'

        if canal == 0:
            datosout = datos[0::2]  #izq
        elif canal == 1:
            datosout = datos[1::2]  #der
        elif canal == 2:
            datosout = [(dataizq + datader) // 2 for dataizq, datader in zip(datos[0::2], datos[1::2])]
        else:
            datosout = [(dataizq - datader) // 2 for dataizq, datader in zip(datos[0::2], datos[1::2])]

        for dato in datosout:
            fout.write(st.pack(formato,dato))

def mono2estereo(ficIzq, ficDer, ficEste) :
    """
    Lee  ficIzq y ficDer. Ambos contiene señales mono y construye  una señal estéreo en el fichero ficEste.
    """

    #Canal Izq
    with open(ficIzq, 'rb') as fin :
        cabecera1 = '<4sI4s'
        buffer1 = fin.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1, buffer1)
        if ChunkID != b'RIFF' or format != b'WAVE' :
            raise Exception('El fichero no es .wav') from None
        
        cabecera2 = '<4sI2H2I2H'
        buffer2 = fin.read(st.calcsize(cabecera2))
        ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample = st.unpack(cabecera2, buffer2)
        if numchannels != 1:
            raise Exception('El fichero no es mono')

        cabecera3 = '<4sI'
        buffer3 = fin.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3, buffer3)
        nummuestras = ChunkSize3 // blockalign
        formato = f'<{nummuestras}h'
        size = st.calcsize(formato)
        buffer4 = fin.read(size)

        datosizq= st.unpack(formato, buffer4) #el tamany del buffer no es l'adequat

    #Canal Der
    with open(ficDer, 'rb') as fin :
        cabecera1 = '<4sI4s'
        buffer1 = fin.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1, buffer1)
        if ChunkID != b'RIFF' or format != b'WAVE' :
            raise Exception('El fichero no es WAVE') from None
        
        cabecera2 = '<4sI2H2I2H'
        buffer2 = fin.read(st.calcsize(cabecera2))
        ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample = st.unpack(cabecera2, buffer2)
        if numchannels != 1:
            raise Exception('El fichero no es mono')
        
        cabecera3 = '<4sI'
        buffer3 = fin.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3, buffer3)
        nummuestras = ChunkSize3 // blockalign
        formato = f'<{nummuestras}h'
        buffer4 = fin.read(st.calcsize(formato))
        datosder= st.unpack(formato, buffer4)
    
    #Escritura Fichero
    with open(ficEste, 'wb') as fout:
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras * 4)
        fout.write(st.pack(cabecera_fmt, *cabecera))

        for muestrasizq, muestrasder in zip(datosizq, datosder):
            muestrasEstereo = st.pack('<hh' , muestrasizq, muestrasder) #<hh cada muestra son 16 bits
            fout.write(muestrasEstereo)

def codEstereo(ficEste, ficCod) :
    """
    Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y construye con ellas una señal codificada con 32 bits.
    """

    with open(ficEste, 'rb') as fpwave:
        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)
        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es .wav') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign       
        formato = f'<{nummuestras*2}h'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datos = st.unpack(formato,buffer4)


    datosizq = []
    datosder = []

    for iter in range(nummuestras) :
        datosizq.append(datos[2* iter])
        datosder.append(datos[iter * 2 + 1]) 

    datos_cod = bytearray()
    for muestraL, muestraR in zip(datosizq, datosder) :
        semisuma = (muestraL + muestraR) // 2
        semidif = (muestraL - muestraR) // 2
        muestracod = (semisuma << 16) | (semidif >> 16)
        datos_cod.extend(st.pack('<i',muestracod))

    
    #Escritura fichero
    with open(ficCod, 'wb') as fout:
        cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
        cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras *4)
        fout.write(st.pack(cabecera_fmt, *cabecera))
        fout.write(datos_cod)


def decEstereo(ficCod, ficEste) :
    """
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos contienen la 
    semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia.
    """

    with open(ficCod, 'rb') as fpwave:
       
        cabecera1 = '<4sI4s'
        buffer1 = fpwave.read(st.calcsize(cabecera1))
        ChunkID, ChunkSize, format = st.unpack(cabecera1,buffer1)
        if ChunkID != b'RIFF' or format != b'WAVE' :
                raise Exception('Fichero no es .wav') from None

        cabecera2 ='<4sI2H2I2H'
        buffer2 = fpwave.read(st.calcsize(cabecera2))
        (ChunkID2, ChunkSize2, format2, numchannels, samplerate, byterate, blockalign, bitspersample)   = st.unpack(cabecera2,buffer2)

        cabecera3 = '<4sI'
        buffer3 = fpwave.read(st.calcsize(cabecera3))
        ChunkID3, ChunkSize3 = st.unpack(cabecera3,buffer3)
        nummuestras = ChunkSize3//blockalign    
        formato = f'<{nummuestras}i'
        size = st.calcsize(formato)
        buffer4 = fpwave.read(size)
        datoscod = st.unpack(formato,buffer4)
   
        datosizq =[]
        datosder = []

        for i in range(nummuestras) :
            semisuma = (datoscod[i] >> 16) 
            semidif =  datoscod[i] & 0x0000ffff      
            muestraR = (semisuma - semidif)  
            muestraL = (semidif + semisuma)  
            datosizq.append(muestraL)
            datosder.append(muestraR)



        #Escritura fichero 
        with open(ficEste,'wb') as fout :
            cabecera_fmt = '<4sI4s4sIHHIIHH4sI'
            cabecera = (b'RIFF', 36 + nummuestras * 4, b'WAVE', b'fmt ', 16, 1, 2, 16000, 64000 , 4, 16, b'data', nummuestras * 4)
            fout.write(st.pack(cabecera_fmt, *cabecera))

            for muestra_L, muestra_R in zip(datosizq,datosder) :         
                muestracodi =   muestra_L << 16 | muestra_R 
                fout.write(st.pack('<i',muestracodi))


estereo2mono('wav\komm.wav','wav\kommMono0.wav',canal=0)
estereo2mono('wav\komm.wav','wav\kommMono1.wav',canal=1)
estereo2mono('wav\komm.wav','wav\kommMono2.wav',canal=2)

mono2estereo("wav\kommMono0.wav","wav\kommMono1.wav","wav\kommStOut.wav")

codEstereo('wav\komm.wav','wav\kommCodec.wav')
decEstereo('wav\kommCodec.wav','wav\kommDeCodec.wav')