import wave
import numpy as np

def estereo2mono(ficEste, ficMono, canal=2):
    with wave.open(ficEste, 'rb') as estereo_file:
        params = estereo_file.getparams()
        num_frames = params.nframes
        sample_width = params.sampwidth
        sample_rate = params.framerate
        channels = params.nchannels
        data = estereo_file.readframes(num_frames)
        estereo_array = np.frombuffer(data, dtype=np.int16)
        
        if canal == 0:
            mono_array = estereo_array[::channels]
        elif canal == 1:
            mono_array = estereo_array[1::channels]
        elif canal == 2:
            mono_array = (estereo_array[::channels] + estereo_array[1::channels]) // 2
        elif canal == 3:
            mono_array = (estereo_array[::channels] - estereo_array[1::channels]) // 2
        
        with wave.open(ficMono, 'wb') as mono_file:
            mono_file.setparams((1, sample_width, sample_rate, num_frames, params.comptype, params.compname))
            mono_file.writeframes(mono_array.tobytes())

def mono2estereo(ficIzq, ficDer, ficEste):
    with wave.open(ficIzq, 'rb') as izq_file, wave.open(ficDer, 'rb') as der_file:
        izq_params = izq_file.getparams()
        der_params = der_file.getparams()
        izq_data = izq_file.readframes(izq_params.nframes)
        der_data = der_file.readframes(der_params.nframes)
        izq_array = np.frombuffer(izq_data, dtype=np.int16)
        der_array = np.frombuffer(der_data, dtype=np.int16)
        
        estereo_array = np.zeros((izq_params.nframes * 2,), dtype=np.int16)
        estereo_array[::2] = izq_array
        estereo_array[1::2] = der_array
        
        with wave.open(ficEste, 'wb') as estereo_file:
            estereo_file.setparams((2, izq_params.sampwidth, izq_params.framerate, izq_params.nframes, izq_params.comptype, izq_params.compname))
            estereo_file.writeframes(estereo_array.tobytes())

def codEstereo(ficEste, ficCod):
    with wave.open(ficEste, 'rb') as estereo_file:
        params = estereo_file.getparams()
        num_frames = params.nframes
        sample_width = params.sampwidth
        sample_rate = params.framerate
        channels = params.nchannels
        data = estereo_file.readframes(num_frames)
        estereo_array = np.frombuffer(data, dtype=np.int16)
        
        semisuma = (estereo_array[::channels] + estereo_array[1::channels]) // 2
        semidiferencia = (estereo_array[::channels] - estereo_array[1::channels]) // 2
        
        cod_array = np.zeros((num_frames * 2,), dtype=np.int32)
        cod_array[::2] = semisuma
        cod_array[1::2] = semidiferencia
        
        with wave.open(ficCod, 'wb') as cod_file:
            cod_file.setparams((2, sample_width * 2, sample_rate, num_frames, params.comptype, params.compname))
            cod_file.writeframes(cod_array.tobytes())

def decEstereo(ficCod, ficEste):
    with wave.open(ficCod, 'rb') as cod_file:
        params = cod_file.getparams()
        num_frames = params.nframes
        sample_width = params.sampwidth
        sample_rate = params.framerate
        channels = params.nchannels
        data = cod_file.readframes(num_frames)
        cod_array = np.frombuffer(data, dtype=np.int32)
        
        semisuma = cod_array[::2]
        semidiferencia = cod_array[1::2]
        
        estereo_array = np.zeros((num_frames * 2,), dtype=np.int16)
        estereo_array[::channels] = semisuma + semidiferencia
        estereo_array[1::channels] = semisuma - semidiferencia
        
        with wave.open(ficEste, 'wb') as estereo_file:
            estereo_file.setparams((2, sample_width // 2, sample_rate, num_frames, params.comptype, params.compname))
            estereo_file.writeframes(estereo_array.tobytes())