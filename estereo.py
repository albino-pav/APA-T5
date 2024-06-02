#DIDAC BASSAS


Dídac
#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

La función lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, con una señal monofónica. El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:

#### mono2estereo(ficIzq, ficDer, ficEste)

Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero ficEste.


#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas monofónicos como por sistemas estéreo preparados para ello.


#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los ficheros WAVE estéreo.

# Be estereo2mono

import struct as st
def estereo2mono(ficEste, ficMono, canal=2):
    f = open(ficEste, mode = 'rb')
    format = "<4sI4s4sIhhIIhhII"
    data_fich = f.read(st.calcsize(format))
    chunk_id, chunk_size, riff_format, subchunk1_ID, Subchunk1Size, AudioFormat, NumChannels,SampleRate, ByteRate, BlockAlign,BitsPerSample, Subchunk2ID, Subchunk2Size = st.unpack(format,data_fich)
    noufile = open(ficMono, "wb")
    chunk_size = int(chunk_size/2)
    NumChannels = 1
    estructura = st.pack(format, chunk_id, chunk_size, riff_format, subchunk1_ID, Subchunk1Size, AudioFormat, NumChannels,SampleRate, ByteRate, BlockAlign,BitsPerSample, Subchunk2ID, Subchunk2Size)
    noufile.write(estructura)


    if(canal == 0):
        f.read(2)
        data = f.read(2)
        while (data != b''):
            noufile.write(data)
            f.read(2)
            data  =  f.read(2)
        noufile.close()

    elif(canal == 1):
        data = f.read(2)
        while (data != b''):
            noufile.write(data)
            f.read(2)
            data  =  f.read(2)
        noufile.close()

    elif(canal == 2):
        dataL = f.read(2)
        dataR = f.read(2)
        
        while (dataL != b'' and dataR != b''):
            dataLint = int.from_bytes(dataL, byteorder='little', signed=False)
            dataRint = int.from_bytes(dataR, byteorder='little', signed=False)
            dataEnInt= int((dataLint+dataRint)/2)
            dataEnBytes = dataEnInt.to_bytes(2, byteorder='little', signed=False)
            noufile.write(dataEnBytes)
            dataL = f.read(2)
            dataR = f.read(2)
    
        noufile.close()
    
    elif(canal == 3):
        dataL = f.read(2)
        dataR = f.read(2)

        while (dataL != b'' and dataR != b''):

            dataLint = int.from_bytes(dataL, byteorder='little', signed=False)
            dataRint = int.from_bytes(dataR, byteorder='little', signed=False)
            dataEnInt= int(abs(dataLint-dataRint)/2)
            dataEnBytes = dataEnInt.to_bytes(2, byteorder='little', signed=False)
            noufile.write(dataEnBytes)
            dataL = f.read(2)
            dataR = f.read(2)
        noufile.close()


estereo2mono("C:\\Users\\didac\\github\\APA-T5\\wav\\komm.wav","C:\\Users\\didac\\github\\APA-T5\\wav\\Mono.wav",1)

#Be mono2estereo

def mono2estereo(ficIzq, ficDer, ficEste):
    FL = open(ficIzq, mode = 'rb')
    FR = open(ficDer, mode = 'rb')
    f  = open(ficEste, mode = 'wb')
    format = "<4sI4s4sIhhIIhhII"
    data_fich = FL.read(st.calcsize(format))
    FR.read(st.calcsize(format))
    chunk_id, chunk_size, riff_format, subchunk1_ID, Subchunk1Size, AudioFormat, NumChannels,SampleRate, ByteRate, BlockAlign,BitsPerSample, Subchunk2ID, Subchunk2Size = st.unpack(format,data_fich)
    chunk_size = int(chunk_size*2)
    NumChannels = 2
    estructura = st.pack(format, chunk_id, chunk_size, riff_format, subchunk1_ID, Subchunk1Size, AudioFormat, NumChannels,SampleRate, ByteRate, BlockAlign,BitsPerSample, Subchunk2ID, Subchunk2Size)
    f.write(estructura)
    dataL = FL.read(2)
    dataR = FR.read(2)
    while (dataL != b'' and dataR != b''):
        f.write(dataL)
        f.write(dataR)
        dataL = FL.read(2)
        dataR = FR.read(2)
    f.close()

mono2estereo("C:\\Users\\didac\\github\\APA-T5\\example2L_.wav","C:\\Users\\didac\\github\\APA-T5\\example2R_.wav","ficEste.wav")


#codEstereo

def codEstereo(ficEste, ficCod):

    f = open(ficEste, mode = 'rb')
    data_fich = f.read(44)
    noufile = open(ficCod, "wb")
    

    dataL1 = f.read(1)
    dataL2 = f.read(1)
    dataR1 = f.read(1)
    dataR2 = f.read(1)



    while (dataL1 != b'' and dataL2 != b'' and dataR1 != b'' and dataR2 != b'' ):

        L1 = int.from_bytes(dataL1, byteorder='little', signed=False)
        R1 = int.from_bytes(dataR1, byteorder='little', signed=False)
        L2 = int.from_bytes(dataL2, byteorder='little', signed=False)
        R2 = int.from_bytes(dataR2, byteorder='little', signed=False)

        D1= int((L1+R1)/2)
        D2= int((L2+R2)/2)
        D3= int(abs(L1-R1)/2)
        D4= int(abs(L2-R2)/2)

        dataEnBytes1 = D1.to_bytes(1, byteorder='little', signed=False)
        dataEnBytes2 = D2.to_bytes(1, byteorder='little', signed=False)
        dataEnBytes3 = D3.to_bytes(1, byteorder='little', signed=False)
        dataEnBytes4 = D4.to_bytes(1, byteorder='little', signed=False)
        
        noufile.write(dataEnBytes1)
        noufile.write(dataEnBytes2)
        noufile.write(dataEnBytes3)
        noufile.write(dataEnBytes4)
        
        dataL1 = f.read(1)
        dataL2 = f.read(1)
        dataR1 = f.read(1)
        dataR2 = f.read(1)

    noufile.close()
    

codEstereo("C:\\Users\\didac\\github\\APA-T5\\wav\\komm.wav", "ficCode.pcm")





    

def  decEstereo(ficCod, ficEste):
     f = open(ficCod, mode = 'rb')
     noufile = open(ficEste,mode = 'wb')

     format = "<4sI4s"
     #b'RIFF' 1860256 b'WAVE' b'fmt ' 16 1 2 16000 64000 4 16 1635017060 1860220
     buffer = st.pack(format, b'RIFF', 36 + os.path.getsize(ficCod), b"WAVE")
     noufile.write(buffer)
     noufile.write(b"fmt")
     format = "<I2H2I2H"
     buffer = st.pack(format, 16, 1, 2, 16000, 64000, 4, 16)

     dataD1 = f.read(1)
     dataD2 = f.read(1)
     dataD3 = f.read(1)
     dataD4 = f.read(1)

     while (dataD1 != b'' and dataD2 != b'' and dataD3 != b'' and dataD4 != b'' ):

          D1 = int.from_bytes(dataD1, byteorder='little', signed=False)
          D2 = int.from_bytes(dataD2, byteorder='little', signed=False)
          D3 = int.from_bytes(dataD3, byteorder='little', signed=False)
          D4 = int.from_bytes(dataD4, byteorder='little', signed=False)

          L1 = D1+D3
          L2 = D2+D4
          R1 = abs(D1-D3)
          R2 = abs(D2-D4)

          dataL1 = L1.to_bytes(1, byteorder='little', signed=False)
          dataL2 = L2.to_bytes(1, byteorder='little', signed=False)
          dataR1 = R1.to_bytes(1, byteorder='little', signed=False)
          dataR2 = R2.to_bytes(1, byteorder='little', signed=False)

          noufile.write(dataL1)
          noufile.write(dataL2)
          noufile.write(dataR1)
          noufile.write(dataR2)

          dataD1 = f.read(1)
          dataD2 = f.read(1)
          dataD3 = f.read(1)
          dataD4 = f.read(1)
     
     noufile.close()

decEstereo("ficCode.pcm", "prova.wav")
