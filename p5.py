import wave
import struct

def estereo2mono(ficEste, ficMono, canal=2):
    with wave.open(ficEste, 'rb') as f_in:
        params = f_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        assert n_channels == 2, "El fichero de entrada debe ser estéreo."
        frames = f_in.readframes(n_frames)

    samples = struct.unpack('<' + 'h' * (n_frames * 2), frames)
    left_channel = samples[0::2]
    right_channel = samples[1::2]

    if canal == 0:
        mono_channel = left_channel
    elif canal == 1:
        mono_channel = right_channel
    elif canal == 2:
        mono_channel = [(l + r) // 2 for l, r in zip(left_channel, right_channel)]
    elif canal == 3:
        mono_channel = [(l - r) // 2 for l, r in zip(left_channel, right_channel)]

    mono_frames = struct.pack('<' + 'h' * len(mono_channel), *mono_channel)
    
    with wave.open(ficMono, 'wb') as f_out:
        f_out.setparams((1, sampwidth, framerate, len(mono_channel), comptype, compname))
        f_out.writeframes(mono_frames)

def mono2estereo(ficIzq, ficDer, ficEste):
    with wave.open(ficIzq, 'rb') as f_left, wave.open(ficDer, 'rb') as f_right:
        params_left = f_left.getparams()
        params_right = f_right.getparams()
        assert params_left == params_right, "Los ficheros de entrada deben tener los mismos parámetros."
        
        left_frames = f_left.readframes(params_left.nframes)
        right_frames = f_right.readframes(params_right.nframes)

    left_channel = struct.unpack('<' + 'h' * params_left.nframes, left_frames)
    right_channel = struct.unpack('<' + 'h' * params_right.nframes, right_frames)
    
    stereo_frames = struct.pack('<' + 'h' * (2 * params_left.nframes), *sum(zip(left_channel, right_channel), ()))

    with wave.open(ficEste, 'wb') as f_out:
        f_out.setparams((2, params_left.sampwidth, params_left.framerate, params_left.nframes, params_left.comptype, params_left.compname))
        f_out.writeframes(stereo_frames)

def codEstereo(ficEste, ficCod):
    with wave.open(ficEste, 'rb') as f_in:
        params = f_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        assert n_channels == 2, "El fichero de entrada debe ser estéreo."
        frames = f_in.readframes(n_frames)

    samples = struct.unpack('<' + 'h' * (n_frames * 2), frames)
    left_channel = samples[0::2]
    right_channel = samples[1::2]

    semisuma = [(l + r) // 2 for l, r in zip(left_channel, right_channel)]
    semidiferencia = [(l - r) // 2 for l, r in zip(left_channel, right_channel)]
    
    combined = [(semisuma[i] << 16) | (semidiferencia[i] & 0xFFFF) for i in range(len(semisuma))]
    combined_frames = struct.pack('<' + 'i' * len(combined), *combined)
    
    with wave.open(ficCod, 'wb') as f_out:
        f_out.setparams((1, 4, framerate, len(combined), comptype, compname))
        f_out.writeframes(combined_frames)

def decEstereo(ficCod, ficEste):
    with wave.open(ficCod, 'rb') as f_in:
        params = f_in.getparams()
        n_channels, sampwidth, framerate, n_frames, comptype, compname = params
        assert n_channels == 1 and sampwidth == 4, "El fichero de entrada debe ser mono y de 32 bits."
        frames = f_in.readframes(n_frames)

    combined = struct.unpack('<' + 'i' * n_frames, frames)
    
    semisuma = [(sample >> 16) for sample in combined]
    semidiferencia = [(sample & 0xFFFF) for sample in combined]
    
    left_channel = [(s + d) for s, d in zip(semisuma, semidiferencia)]
    right_channel = [(s - d) for s, d in zip(semisuma, semidiferencia)]
    
    stereo_frames = struct.pack('<' + 'h' * (2 * n_frames), *sum(zip(left_channel, right_channel), ()))
    
    with wave.open(ficEste, 'wb') as f_out:
        f_out.setparams((2, 2, framerate, n_frames, comptype, compname))
        f_out.writeframes(stereo_frames)

