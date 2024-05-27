import struct


def read_wave_file(file_path):
    """
   LLegeix un fitxer wave i retorna la informació de la capçalera i les dades d'àudio.

    Args:
        file_path (str): El path del fitxer wave.

    Returns:
        dict: Un diccionari amb la informació de la capçalera i les dades d'àudio.
    """
    
    with open(file_path, 'rb') as file:
        riff_header = file.read(12)
        format_chunk_header = file.read(24)

        # Extreu la informació de la capçalera
        riff_id, riff_size, riff_format = struct.unpack('<4sI4s', riff_header)
        format_id, format_size, audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<4sIHHIIHH', format_chunk_header)
        data_chunk_header = file.read(8)
        data_id, data_size = struct.unpack('<4sI', data_chunk_header)

        # Llegeix les dades d'àudio
        audio_data = file.read(data_size)
        
        # Verifica que el fitxer sigui un fitxer wave vàlid
        if riff_id != b'RIFF' or riff_format != b'WAVE' or format_id != b'fmt ' or data_id != b'data':
            raise ValueError(' wave file invalida')
        
        # Comprovació de la mida de les dades
        if bits_per_sample == 8:
            audio_data = struct.unpack('<{}B'.format(len(audio_data)), audio_data)
        elif bits_per_sample == 16:
            audio_data = struct.unpack('<{}h'.format(len(audio_data) // 2), audio_data)
        elif bits_per_sample == 32:
            audio_data = struct.unpack('<{}i'.format(len(audio_data) // 4), audio_data)
        else:
            raise ValueError(' bits per sample invalids')
        
        # Torna la informació de la capçalera i les dades d'àudio
        return {
            'riff_id': riff_id,
            'riff_size': riff_size,
            'riff_format': riff_format,
            'format_id': format_id,
            'format_size': format_size,
            'audio_format': audio_format,
            'num_channels': num_channels,
            'sample_rate': sample_rate,
            'byte_rate': byte_rate,
            'block_align': block_align,
            'bits_per_sample': bits_per_sample,
            'data_id': data_id,
            'data_size': data_size,
            'audio_data': audio_data
        }
   
        
# Escriu un fitxer wave amb la capçalera i les dades d'àudio especificades. 
def write_wave_file(file_path, header, audio_data):
    with open(file_path, 'wb') as file:
        # Escriu la capçalera
        file.write(struct.pack('<4sI4s', header['riff_id'], header['riff_size'], header['riff_format']))
        file.write(struct.pack('<4sIHHIIHH', header['format_id'], header['format_size'], header['audio_format'], header['num_channels'], header['sample_rate'], header['byte_rate'], header['block_align'], header['bits_per_sample']))

        # Escriu les dades d'àudio
        file.write(struct.pack('<4sI', header['data_id'], header['data_size']))
        file.write(audio_data)
 
        
def estereo2mono(input_file_path, output_file_path, channel='L'):
    """
    Funció que llegeix un fitxer wave estereo i escriu un fitxer wave mono amb el canal especificat (L, R, +, -), per defecte L

        Args: input_file_path (str): El path del fitxer wave estereo, output_file_path (str): El path del fitxer wave mono, 
            channel (str): El canal a extreure (L, R, +, -)
        Returns: None, simplement escriu el fitxer wave mono
        
    """
    wave_file = read_wave_file(input_file_path)
    
    # Comprova si el fitxer és estereo
    if wave_file['num_channels'] != 2:
        raise ValueError('The input file is not stereo')
    
    # Calcula la nova informació de la capçalera
    new_header = wave_file.copy()
    new_header['num_channels'] = 1
    new_header['byte_rate'] = wave_file['byte_rate'] // 2
    new_header['block_align'] = wave_file['block_align'] // 2
    new_header['data_size'] = wave_file['data_size'] // 2
    
    # Converteix les dades d'àudio a mono
    mono_audio_data = []
    for i in range(0, len(wave_file['audio_data']), 2):
        if channel == 'L':
            mono_audio_data.append(wave_file['audio_data'][i])
        elif channel == 'R':
            mono_audio_data.append(wave_file['audio_data'][i + 1])
        elif channel == '+':
            mono_audio_data.append((wave_file['audio_data'][i] + wave_file['audio_data'][i + 1]) // 2 )
        elif channel == '-':
            mono_audio_data.append((wave_file['audio_data'][i] - wave_file['audio_data'][i + 1]) // 2 )
        else:
            raise ValueError('Invalid channel')
    
    # Escriu el nou fitxer wave
    write_wave_file(output_file_path, new_header, struct.pack('<{}h'.format(len(mono_audio_data)), *mono_audio_data))

                    
def mono2estereo(input_file_path1, input_file_path2, output_file_path):
    """
    Converteix dos fitxers d'àudio mono en un fitxer d'àudio estèreo.

    Arguments:
    - input_file_path1 (str): Ruta del primer fitxer d'àudio mono.
    - input_file_path2 (str): Ruta del segon fitxer d'àudio mono.
    - output_file_path (str): Ruta del fitxer d'àudio estèreo de sortida.

    Returns:
    None
    """
    # Llegeix els fitxers wave
    wave_file1 = read_wave_file(input_file_path1)
    wave_file2 = read_wave_file(input_file_path2)
    
    # Comprova si els fitxers són mono
    if wave_file1['num_channels'] != 1 or wave_file2['num_channels'] != 1:
        raise ValueError('Els fitxers d\'entrada no són mono')
    
    # Calcula la nova informació de la capçalera
    new_header = wave_file1.copy()
    new_header['num_channels'] = 2
    new_header['byte_rate'] = wave_file1['byte_rate'] * 2
    new_header['block_align'] = wave_file1['block_align'] * 2
    new_header['data_size'] = wave_file1['data_size'] * 2
    
    # Converteix les dades d'àudio a estereo
    stereo_audio_data = []
    for i in range(len(wave_file1['audio_data'])):
        stereo_audio_data.append(wave_file1['audio_data'][i])
        stereo_audio_data.append(wave_file2['audio_data'][i])
    
    # Escriu el nou fitxer wave
    write_wave_file(output_file_path, new_header, struct.pack('<{}h'.format(len(stereo_audio_data)), *stereo_audio_data))
                    


def codEstereo(input_file_path, output_file_path):
    """
    Converteix un fitxer wave estereo de 16 bits a un fitxer wave de 32 bits amb un únic canal.

    Arguments:
    - input_file_path (str): Ruta del fitxer wave d'entrada.
    - output_file_path (str): Ruta del fitxer wave de sortida.

    Returns:
    None
    """
    # Llegeix el fitxer wave
    wave_file = read_wave_file(input_file_path)
    
    # Comprova si el fitxer és estereo
    if wave_file['num_channels'] != 2:
        raise ValueError('El fitxer d\'entrada no és estereo')
    
    # Comprova si el fitxer és de 16 bits
    if wave_file['bits_per_sample'] != 16:
        raise ValueError('El fitxer d\'entrada no és de 16 bits')
    
    # Calcula la nova informació de la capçalera, el fitxer de sortida serà de 32 bits però només amb 1 canal
    new_header = wave_file.copy()
    new_header['num_channels'] = 1
    new_header['bits_per_sample'] = 32
    
    # Converteix les dades d'àudio a 32 bits
    audio_data = wave_file['audio_data']
    data_este_sum = [ round((audio_data[i] + audio_data[i+1]) / 2) for i in range(0,len(audio_data), 2) ]
    data_este_sub = [ round((audio_data[i] - audio_data[i+1]) / 2) for i in range(0,len(audio_data), 2) ]
    audio_data = [ (data_este_sub[i] << 16) | (data_este_sum[i] & 0xFFFF) for i in range(len(data_este_sum)) ]
    
    # Escriu el nou fitxer wave
    write_wave_file(output_file_path, new_header, struct.pack('<{}i'.format(len(audio_data)), *audio_data))


def decEstereo(input_file_path, output_file_path):
    """
    Converteix un fitxer wave mono de 32 bits a un fitxer wave estereo de 16 bits.

    Arguments:
    - input_file_path (str): Ruta del fitxer wave d'entrada.
    - output_file_path (str): Ruta del fitxer wave de sortida.

    Returns:
    None
    """
    # Llegeix el fitxer wave
    wave_file = read_wave_file(input_file_path)
    
    # Comprova si el fitxer és mono
    if wave_file['num_channels'] != 1:
        raise ValueError('El fitxer d\'entrada no és mono')
    
    # Comprova si el fitxer és de 32 bits
    if wave_file['bits_per_sample'] != 32:
        raise ValueError('El fitxer d\'entrada no és de 32 bits')
    
    # Calcula la nova informació de la capçalera, el fitxer de sortida serà estereo de 16 bits
    new_header = wave_file.copy()
    new_header['num_channels'] = 2
    new_header['bits_per_sample'] = 16
    
    # Converteix les dades d'àudio a estereo de 16 bits
    audio_data = wave_file['audio_data']
    data_este_sub = [ (sample >> 16) for sample in audio_data ]
    data_este_sum = [ struct.unpack('h', struct.pack('H', sample & 0xFFFF))[0] for sample in audio_data ]

    # Imprimeix els valors màxims i mínims de les dades d'àudio

   
    # Calcula les dades d'àudio per al canal dret i esquerra
    right = [data_este_sum - data_este_sub for data_este_sum, data_este_sub in zip(data_este_sum, data_este_sub)]
    left = [data_este_sum + data_este_sub for data_este_sum, data_este_sub in zip(data_este_sum, data_este_sub)]
    
    # Combina les dades d'àudio del canal dret i esquerra en un sol array
    audio_data = [sample for pair in zip(left, right) for sample in pair]
    
    # Escriu el nou fitxer wave
    write_wave_file(output_file_path, new_header, struct.pack('<{}h'.format(len(audio_data)), *audio_data))
    
    
    
    


#Banc de proves 
if __name__ == '__main__':
    estereo2mono('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_L.wav', 'L')
    estereo2mono('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_R.wav', 'R')
    estereo2mono('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_+.wav', '+')
    estereo2mono('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_-.wav', '-')
    
    mono2estereo('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_L.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_R.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_stereo_l_r.wav')
    mono2estereo('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_+.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_mono_-.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_stereo_-_+.wav')
        
    codEstereo('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_coded.wav')
    decEstereo('C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_coded.wav', 'C:\\Users\\ferra\\Documents\\UPC\\APA\\cinquena\\komm_decoded.wav')
    
    
    print('Done')
