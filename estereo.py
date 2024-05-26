import struct

#funcion desempaquetar cabecera
def leer_cabecera_wave(f):
    cabecera = f.read(44)
    if len(cabecera) != 44:
        raise ValueError("Cabecera del archivo WAVE incorrecta o incompleta.")
    return struct.unpack('<4sI4s4sIHHIIHH4sI', cabecera)


#funcion empaquetar cabecera
def escribir_cabecera_wave(f, cabecera):
    f.write(struct.pack('<4sI4s4sIHHIIHH4sI', *cabecera))

#funcion convertir de estereo a mono
def estereo2mono(ficEste, ficMono, canal=2):
    """
    Convierte un archivo WAVE estéreo a monofónico.

    Parámetros:
    ficEste: str - Nombre del archivo de entrada (estéreo).
    ficMono: str - Nombre del archivo de salida (monofónico).
    canal: int - Canal a extraer: 0 = izquierdo, 1 = derecho, 2 = semisuma (por defecto), 3 = semidiferencia.
    """
    with open(ficEste, 'rb') as f:
        # Leer y desempaquetar cabecera
        (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        ) = leer_cabecera_wave(f)
        
        # Comprobar que es un archivo estéreo
        if chunk_id != b'RIFF' or format != b'WAVE' or subchunk1_id != b'fmt ' or subchunk2_id != b'data':
            raise ValueError("El archivo de entrada no es un archivo WAVE válido.")
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El archivo de entrada no es estéreo o no tiene 16 bits por muestra.")
        
        # Modificar cabecera para archivo monofónico
        num_channels = 1
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        subchunk2_size = subchunk2_size // 2
        chunk_size = 36 + subchunk2_size
        
        nueva_cabecera = (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        )

        # Escribir cabecera modificada en el archivo de salida
        with open(ficMono, 'wb') as out_f:
            escribir_cabecera_wave(out_f, nueva_cabecera)
            
            # Leer y procesar datos estéreo
            while True:
                datos = f.read(4)
                if not datos:
                    break
                muestra_izq, muestra_der = struct.unpack('<hh', datos)
                
                if canal == 0:
                    muestra_mono = muestra_izq
                elif canal == 1:
                    muestra_mono = muestra_der
                elif canal == 2:
                    muestra_mono = (muestra_izq + muestra_der) // 2
                elif canal == 3:
                    muestra_mono = (muestra_izq - muestra_der) // 2
                else:
                    raise ValueError("Canal no válido. Debe ser 0, 1, 2 o 3.")
                
                out_f.write(struct.pack('<h', muestra_mono))

# Uso estero2mono
if __name__ == "__main__":
    estereo2mono('komm.wav', 'komm_mono.wav', canal=2)

#Crear archivos mono para canal IZQ y DER
estereo2mono('komm.wav', 'komm_izq.wav', canal=0)  # Canal izquierdo
estereo2mono('komm.wav', 'komm_der.wav', canal=1)  # Canal derecho

#funcion convertir de mono a estereo
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Convierte dos archivos WAVE monofónicos en un archivo estéreo.

    Parámetros:
    ficIzq: str - Nombre del archivo de entrada para el canal izquierdo.
    ficDer: str - Nombre del archivo de entrada para el canal derecho.
    ficEste: str - Nombre del archivo de salida estéreo.
    """
    with open(ficIzq, 'rb') as f_izq, open(ficDer, 'rb') as f_der:
        # Leer y desempaquetar cabeceras de los archivos monofónicos
        cabecera_izq = leer_cabecera_wave(f_izq)
        cabecera_der = leer_cabecera_wave(f_der)
        
        # Comprobar que ambos archivos monofónicos tienen la misma configuración
        (
            chunk_id_izq, chunk_size_izq, format_izq, subchunk1_id_izq, subchunk1_size_izq, audio_format_izq,
            num_channels_izq, sample_rate_izq, byte_rate_izq, block_align_izq, bits_per_sample_izq,
            subchunk2_id_izq, subchunk2_size_izq
        ) = cabecera_izq

        (
            chunk_id_der, chunk_size_der, format_der, subchunk1_id_der, subchunk1_size_der, audio_format_der,
            num_channels_der, sample_rate_der, byte_rate_der, block_align_der, bits_per_sample_der,
            subchunk2_id_der, subchunk2_size_der
        ) = cabecera_der

        if (chunk_id_izq != b'RIFF' or format_izq != b'WAVE' or subchunk1_id_izq != b'fmt ' or subchunk2_id_izq != b'data' or
            chunk_id_der != b'RIFF' or format_der != b'WAVE' or subchunk1_id_der != b'fmt ' or subchunk2_id_der != b'data'):
            raise ValueError("Uno o ambos archivos de entrada no son archivos WAVE válidos.")
        
        if (audio_format_izq != 1 or audio_format_der != 1 or num_channels_izq != 1 or num_channels_der != 1 or
            sample_rate_izq != sample_rate_der or bits_per_sample_izq != bits_per_sample_der):
            raise ValueError("Los archivos monofónicos no tienen la misma configuración.")
        
        # Modificar la cabecera para archivo estéreo
        num_channels = 2
        byte_rate = sample_rate_izq * num_channels * bits_per_sample_izq // 8
        block_align = num_channels * bits_per_sample_izq // 8
        subchunk2_size = subchunk2_size_izq + subchunk2_size_der
        chunk_size = 36 + subchunk2_size
        
        nueva_cabecera = (
            chunk_id_izq, chunk_size, format_izq, subchunk1_id_izq, subchunk1_size_izq, audio_format_izq,
            num_channels, sample_rate_izq, byte_rate, block_align, bits_per_sample_izq,
            subchunk2_id_izq, subchunk2_size
        )

        # Escribir la nueva cabecera en el archivo estéreo
        with open(ficEste, 'wb') as out_f:
            escribir_cabecera_wave(out_f, nueva_cabecera)

            # Leer y combinar datos de ambos archivos monofónicos
            while True:
                datos_izq = f_izq.read(2)
                datos_der = f_der.read(2)
                
                if not datos_izq or not datos_der:
                    break

                muestra_izq = struct.unpack('<h', datos_izq)[0]
                muestra_der = struct.unpack('<h', datos_der)[0]
                
                datos_estereo = struct.pack('<hh', muestra_izq, muestra_der)
                out_f.write(datos_estereo)

mono2estereo('komm_izq.wav', 'komm_der.wav', 'komm_reconstruido.wav')


#codificar señal con 32 bits
def codEstereo(ficEste, ficCod):
    """
    Convierte un archivo WAVE estéreo a una señal codificada con 32 bits.

    Parámetros:
    ficEste: str - Nombre del archivo de entrada (estéreo).
    ficCod: str - Nombre del archivo de salida (codificado con 32 bits).
    """
    with open(ficEste, 'rb') as f_in:
        # Leer y desempaquetar cabecera
        (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        ) = leer_cabecera_wave(f_in)
        
        # Comprobar que es un archivo estéreo con 16 bits por muestra
        if chunk_id != b'RIFF' or format != b'WAVE' or subchunk1_id != b'fmt ' or subchunk2_id != b'data':
            raise ValueError("El archivo de entrada no es un archivo WAVE válido.")
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El archivo de entrada no es estéreo o no tiene 16 bits por muestra.")
        
        # Modificar cabecera para archivo codificado con 32 bits
        num_channels = 1  # Mono
        bits_per_sample = 32
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        subchunk2_size *= 2  # Duplicar el tamaño de los datos
        
        # Calcular el nuevo tamaño del chunk
        chunk_size = 36 + subchunk2_size
        
        # Nueva cabecera
        nueva_cabecera = (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        )

        # Escribir la nueva cabecera en el archivo de salida
        with open(ficCod, 'wb') as f_out:
            escribir_cabecera_wave(f_out, nueva_cabecera)
            
            # Procesar los datos estéreo
            while True:
                datos = f_in.read(4)
                if not datos:
                    break
                muestra_izq, muestra_der = struct.unpack('<hh', datos)
                
                # Calcular semisuma y semidiferencia
                semisuma = muestra_izq + muestra_der
                semidif = muestra_izq - muestra_der
                
                # Empaquetar datos de 32 bits y escribir en el archivo de salida
                datos_32bits = struct.pack('<ii', semisuma, semidif)
                f_out.write(datos_32bits)

codEstereo('komm.wav', 'komm_codificado.wav')


def decEstereo(ficCod, ficEste):
    """
    Convierte un archivo WAVE monofónico de 32 bits a un archivo estéreo con los dos canales separados.

    Parámetros:
    ficCod: str - Nombre del archivo de entrada (codificado con 32 bits).
    ficEste: str - Nombre del archivo de salida (estéreo).
    """
    with open(ficCod, 'rb') as f_in:
        # Leer y desempaquetar cabecera
        (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        ) = leer_cabecera_wave(f_in)
        
        # Comprobar que es un archivo monofónico con 32 bits por muestra
        if chunk_id != b'RIFF' or format != b'WAVE' or subchunk1_id != b'fmt ' or subchunk2_id != b'data':
            raise ValueError("El archivo de entrada no es un archivo WAVE válido.")
        if num_channels != 1 or bits_per_sample != 32:
            raise ValueError("El archivo de entrada no es monofónico o no tiene 32 bits por muestra.")
        
        # Modificar cabecera para archivo estéreo
        num_channels = 2  # Estéreo
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        subchunk2_size //= 2  # Dividir el tamaño de los datos
        
        # Calcular el nuevo tamaño del chunk
        chunk_size = 36 + subchunk2_size
        
        # Nueva cabecera
        nueva_cabecera = (
            chunk_id, chunk_size, format, subchunk1_id, subchunk1_size, audio_format,
            num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
            subchunk2_id, subchunk2_size
        )

        # Escribir la nueva cabecera en el archivo de salida
        with open(ficEste, 'wb') as f_out:
            escribir_cabecera_wave(f_out, nueva_cabecera)
            
            # Procesar los datos monofónicos
            while True:
                datos = f_in.read(8)  # Leer 8 bytes (4 bytes para semisuma y 4 bytes para semidiferencia)
                if not datos:
                    break
                
                semisuma, semidif = struct.unpack('<ii', datos)
                
                # Calcular los canales izquierdo y derecho
                muestra_izq = (semisuma + semidif) // 2
                muestra_der = (semisuma - semidif) // 2
                
                # Empaquetar datos de 16 bits y escribir en el archivo de salida
                datos_16bits = struct.pack('<hh', muestra_izq, muestra_der)
                f_out.write(datos_16bits)


decEstereo('komm_codificado.wav', 'komm_reconstruido_estereo.wav')