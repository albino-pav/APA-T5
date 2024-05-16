## Albert Batlló

import struct

def pack_wav_header(num_channels, sample_width, sample_rate, num_frames):
    return struct.pack('<4sI8sIHHIIHH4sI', b'RIFF', 36 + num_frames * num_channels * sample_width, b'WAVEfmt ', 16, 1, num_channels, sample_rate, sample_rate * num_channels * sample_width, num_channels * sample_width, sample_width * 8, b'data', num_frames * num_channels * sample_width)

def unpack_wav_header(header):
    return struct.unpack('<4sI8sIHHIIHH4sI', header)

def estereo2mono(fic_este, fic_mono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, y escribe el fichero ficMono, con una señal monofónica. El tipo concreto de señal que se almacenará en ficMono depende del argumento canal:

    .   canal=0: Se almacena el canal izquierdo L

    .   canal=1: Se almacena el canal derecho R

    .   canal=2: Se almacena la semisuma (L + R)/2 Ha de ser la opción por defecto.
    
    .   canal=3: Se almacena la semidiferencia (L - R)/2

    """
    if canal not in [0, 1, 2, 3]:
        raise ValueError("El valor de 'canal' debe ser 0, 1, 2 o 3.")

    with open(fic_este, 'rb') as file_in, open(fic_mono, 'wb') as file_out:
        header = file_in.read(44)  
        riff, size, wavefmt, fmt_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample, data, data_size = unpack_wav_header(header)

        if num_channels != 2:
            raise ValueError("El archivo de entrada no es estéreo.")

        if canal == 0:
            offset = 0
        elif canal == 1:
            offset = 1
        elif canal == 2:
            offset = 0.5
        else:
            offset = 0.5

        num_frames = data_size // (num_channels * (bits_per_sample // 8))
        samples = struct.unpack('<{}h'.format(num_frames * num_channels), file_in.read())

        mono_samples = [samples[i + offset] for i in range(0, len(samples), num_channels)]

        file_out.write(pack_wav_header(1, bits_per_sample // 8, sample_rate, len(mono_samples)))
        file_out.write(struct.pack('<{}h'.format(len(mono_samples)), *mono_samples))

def mono2estereo(fic_izq, fic_der, fic_este):
    """
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas correspondientes a los canales izquierdo y derecho,
    respectivamente, y construye con ellas una señal estéreo que almacena en el fichero ficEste.
    
    """
    with open(fic_izq, 'rb') as file_izq, open(fic_der, 'rb') as file_der, open(fic_este, 'wb') as file_out:
        header_izq = file_izq.read(44)
        header_der = file_der.read(44)

        riff_izq, size_izq, wavefmt_izq, fmt_size_izq, audio_format_izq, num_channels_izq, sample_rate_izq, byte_rate_izq, block_align_izq, bits_per_sample_izq, data_izq, data_size_izq = unpack_wav_header(header_izq)
        riff_der, size_der, wavefmt_der, fmt_size_der, audio_format_der, num_channels_der, sample_rate_der, byte_rate_der, block_align_der, bits_per_sample_der, data_der, data_size_der = unpack_wav_header(header_der)

        if num_channels_izq != 1 or num_channels_der != 1:
            raise ValueError("Los archivos de entrada no son mono.")

        samples_izq = struct.unpack('<{}h'.format(data_size_izq // (bits_per_sample_izq // 8)), file_izq.read())
        samples_der = struct.unpack('<{}h'.format(data_size_der // (bits_per_sample_der // 8)), file_der.read())

        if len(samples_izq) != len(samples_der):
            raise ValueError("Las señales mono tienen diferente longitud.")

        stereo_samples = [samples_izq[i] for i in range(len(samples_izq))] + [samples_der[i] for i in range(len(samples_der))]

        file_out.write(pack_wav_header(2, bits_per_sample_izq // 8, sample_rate_izq, len(stereo_samples) // 2))
        file_out.write(struct.pack('<{}h'.format(len(stereo_samples)), *stereo_samples))

def cod_estereo(fic_este, fic_cod):
    """
    Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, 
    y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
    monofónicos como por sistemas estéreo preparados para ello.
    """
    with open(fic_este, 'rb') as file_in, open(fic_cod, 'wb') as file_out:
        header = file_in.read(44)

        riff, size, wavefmt, fmt_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample, data, data_size = unpack_wav_header(header)

        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El archivo de entrada no es estéreo o no está codificado con PCM lineal de 16 bits.")

        samples = struct.unpack('<{}h'.format(data_size // (bits_per_sample // 8)), file_in.read())

        coded_samples = [((samples[i] << 16) & 0xFFFF0000) | (samples[i+1] & 0x0000FFFF) for i in range(0, len(samples), 2)]

        file_out.write(pack_wav_header(1, 4, sample_rate, len(coded_samples)))
        file_out.write(struct.pack('<{}I'.format(len(coded_samples)), *coded_samples))

def dec_estereo(fic_cod, fic_este):
    """
    Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos contienen la semisuma de los dos canales
    de una señal estéreo y los 16 bits menos significativos la semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en 
    el formato de los ficheros WAVE estéreo.
    """
    with open(fic_cod, 'rb') as file_in, open(fic_este, 'wb') as file_out:
        header = file_in.read(44)

        riff, size, wavefmt, fmt_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample, data, data_size = unpack_wav_header(header)

        if bits_per_sample != 32 or num_channels != 1:
            raise ValueError("El archivo de entrada no está codificado como señal estéreo.")

        samples = struct.unpack('<{}I'.format(data_size // 4), file_in.read())

        decoded_samples = [(sample >> 16) | ((sample & 0xFFFF) << 16) for sample in samples]

        file_out.write(pack_wav_header(2, 16, sample_rate, len(decoded_samples) * 2))
        file_out.write(struct.pack('<{}h'.format(len(decoded_samples) * 2), *decoded_samples))
