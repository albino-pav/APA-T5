"""
estereo.py

Guillem Perez Sanchez
Manejo de señales estéreo en ficheros WAVE. Conversión estéreo ↔ mono,
codificación/decodificación compatible con sistemas monofónicos usando 32 bits.
"""

import struct

def estereo2mono(ficEste, ficMono, canal=2):
    """
    Convierte un fichero WAVE estéreo en uno monofónico.
    
    Parámetros:
    ficEste -- nombre del fichero de entrada (estéreo)
    ficMono -- nombre del fichero de salida (monofónico)
    canal -- tipo de conversión:
             0: canal izquierdo
             1: canal derecho
             2: semisuma (L + R) // 2 (por defecto)
             3: semidiferencia (L - R) // 2
    """
    with open(ficEste, 'rb') as fe:
        cabecera = fe.read(44)
        if cabecera[22:24] != b'\x02\x00':  # NumChannels = 2
            raise ValueError("El fichero de entrada no es estéreo (2 canales)")

        # Extraer parámetros
        tam_muestras = struct.unpack('<I', cabecera[40:44])[0]
        num_muestras = tam_muestras // 4  # 2 bytes por canal → 4 bytes por muestra estéreo
        datos = fe.read(tam_muestras)
        muestras = struct.unpack('<' + 'hh'*num_muestras, datos)

        # Separar canales y aplicar operación
        if canal == 0:  # canal izquierdo
            mono = [muestras[i] for i in range(0, len(muestras), 2)]
        elif canal == 1:  # canal derecho
            mono = [muestras[i] for i in range(1, len(muestras), 2)]
        elif canal == 2:  # semisuma
            mono = [(muestras[i] + muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
        elif canal == 3:  # semidiferencia
            mono = [(muestras[i] - muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
        else:
            raise ValueError("Parámetro 'canal' no válido (debe ser 0, 1, 2 o 3)")

    # Crear nueva cabecera monofónica
    nuevo_tam_datos = len(mono) * 2
    nueva_cabecera = bytearray(cabecera)
    nueva_cabecera[22:24] = b'\x01\x00'  # NumChannels = 1
    nueva_cabecera[32:34] = b'\x02\x00'  # BlockAlign = 2 bytes (1 canal * 2 bytes)
    nueva_cabecera[34:36] = b'\x10\x00'  # BitsPerSample = 16
    nueva_cabecera[40:44] = struct.pack('<I', nuevo_tam_datos)
    nueva_cabecera[4:8] = struct.pack('<I', 36 + nuevo_tam_datos)

    with open(ficMono, 'wb') as fm:
        fm.write(nueva_cabecera)
        fm.write(struct.pack('<' + 'h'*len(mono), *mono))

def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Crea un fichero estéreo a partir de dos ficheros monofónicos.

    Parámetros:
    ficIzq -- fichero de canal izquierdo (mono)
    ficDer -- fichero de canal derecho (mono)
    ficEste -- fichero de salida (estéreo)
    """
    with open(ficIzq, 'rb') as fz, open(ficDer, 'rb') as fd:
        cab_izq = fz.read(44)
        cab_der = fd.read(44)

        # Verificación de cabeceras mono
        if cab_izq[22:24] != b'\x01\x00' or cab_der[22:24] != b'\x01\x00':
            raise ValueError("Ambos ficheros deben ser monofónicos (1 canal)")

        datos_izq = fz.read()
        datos_der = fd.read()

        num_muestras_izq = len(datos_izq) // 2
        num_muestras_der = len(datos_der) // 2

        if num_muestras_izq != num_muestras_der:
            raise ValueError("Los ficheros de entrada deben tener el mismo número de muestras")

        izq = struct.unpack('<' + 'h'*num_muestras_izq, datos_izq)
        der = struct.unpack('<' + 'h'*num_muestras_der, datos_der)

    # Intercalar muestras L, R
    estereo = [val for par in zip(izq, der) for val in par]

    nuevo_tam_datos = len(estereo) * 2
    nueva_cabecera = bytearray(cab_izq)
    nueva_cabecera[22:24] = b'\x02\x00'  # NumChannels = 2
    nueva_cabecera[32:34] = b'\x04\x00'  # BlockAlign = 4 (2 canales x 2 bytes)
    nueva_cabecera[34:36] = b'\x10\x00'  # BitsPerSample = 16
    nueva_cabecera[40:44] = struct.pack('<I', nuevo_tam_datos)
    nueva_cabecera[4:8] = struct.pack('<I', 36 + nuevo_tam_datos)

    with open(ficEste, 'wb') as fe:
        fe.write(nueva_cabecera)
        fe.write(struct.pack('<' + 'h'*len(estereo), *estereo))

def codEstereo(ficEste, ficCod):
    """
    Codifica una señal estéreo en una señal de 32 bits compatible con sistemas mono/estéreo.

    Parámetros:
    ficEste -- fichero de entrada estéreo (wav, 16 bits)
    ficCod -- fichero de salida codificado (wav, 32 bits)
    """
    with open(ficEste, 'rb') as fe:
        cabecera = fe.read(44)

        if cabecera[22:24] != b'\x02\x00':  # NumChannels = 2
            raise ValueError("El fichero de entrada no es estéreo (2 canales)")

        datos = fe.read()
        num_muestras = len(datos) // 4  # 4 bytes por muestra estéreo
        muestras = struct.unpack('<' + 'hh'*num_muestras, datos)

        # Calcular semisuma y semidiferencia
        codificadas = [((l + r) << 16) | ((l - r) & 0xFFFF)
                       for l, r in zip(muestras[::2], muestras[1::2])]

    # Crear nueva cabecera: 1 canal, 32 bits
    nuevo_tam_datos = len(codificadas) * 4
    nueva_cabecera = bytearray(cabecera)
    nueva_cabecera[22:24] = b'\x01\x00'  # NumChannels = 1
    nueva_cabecera[32:34] = b'\x04\x00'  # BlockAlign = 4
    nueva_cabecera[34:36] = b'\x20\x00'  # BitsPerSample = 32
    nueva_cabecera[40:44] = struct.pack('<I', nuevo_tam_datos)
    nueva_cabecera[4:8] = struct.pack('<I', 36 + nuevo_tam_datos)

    with open(ficCod, 'wb') as fc:
        fc.write(nueva_cabecera)
        fc.write(struct.pack('<' + 'I'*len(codificadas), *codificadas))

def decEstereo(ficCod, ficEste):
    """
    Decodifica un fichero codificado con 32 bits en una señal estéreo de 16 bits por canal.

    Parámetros:
    ficCod -- fichero de entrada codificado (mono, 32 bits)
    ficEste -- fichero de salida estéreo (wav, 16 bits por canal)
    """
    with open(ficCod, 'rb') as fc:
        cabecera = fc.read(44)

        if cabecera[22:24] != b'\x01\x00' or cabecera[34:36] != b'\x20\x00':
            raise ValueError("El fichero de entrada debe ser mono de 32 bits")

        datos = fc.read()
        num_muestras = len(datos) // 4
        codificadas = struct.unpack('<' + 'I'*num_muestras, datos)

        # Extraer semisuma y semidiferencia
        estereo = []
        for cod in codificadas:
            suma = (cod >> 16)
            dif = struct.unpack('<h', struct.pack('<H', cod & 0xFFFF))[0]  # signo correcto
            l = suma + dif
            r = suma - dif
            estereo.extend([l, r])

    nuevo_tam_datos = len(estereo) * 2
    nueva_cabecera = bytearray(cabecera)
    nueva_cabecera[22:24] = b'\x02\x00'  # NumChannels = 2
    nueva_cabecera[32:34] = b'\x04\x00'  # BlockAlign = 4 bytes
    nueva_cabecera[34:36] = b'\x10\x00'  # BitsPerSample = 16
    nueva_cabecera[40:44] = struct.pack('<I', nuevo_tam_datos)
    nueva_cabecera[4:8] = struct.pack('<I', 36 + nuevo_tam_datos)

    with open(ficEste, 'wb') as fe:
        fe.write(nueva_cabecera)
        fe.write(struct.pack('<' + 'h'*len(estereo), *estereo))
