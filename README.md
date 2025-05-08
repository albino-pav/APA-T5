# Sonido estéreo y ficheros WAVE

## Nom i cognoms

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.

### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios
para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de
pantalla, debe hacerse en formato *markdown*).

##### Código de `estereo2mono()`

```py
def estereo2mono(ficEste, ficMono, canal=2):
    # Open the input file for reading
    infile = open(ficEste, 'rb')
    header = read_wav_header(infile)
    num_channels = header[6]
    bits_per_sample = header[10]
    if num_channels != 2 or bits_per_sample != 16:
        infile.close()
        raise ValueError("The input file must be 16-bit stereo")
    subchunk2_size = header[12]
    frame_size = num_channels * (bits_per_sample // 8)
    n_frames = subchunk2_size // frame_size
    data = infile.read(subchunk2_size)
    infile.close()
    
    # Manually extract left and right samples
    stereo_samples = struct.unpack('<' + 'h' * (n_frames * 2), data)
    left = []
    right = []
    for i in range(n_frames):
        left.append(stereo_samples[2*i])
        right.append(stereo_samples[2*i+1])
    
    # Determine the output channel
    mono_samples = []
    if canal == 0:
        mono_samples = left
    elif canal == 1:
        mono_samples = right
    elif canal == 2:
        # Half-sum of L and R
        for i in range(n_frames):
            mono_samples.append((left[i] + right[i]) // 2)
    elif canal == 3:
        # Half-difference of L and R
        for i in range(n_frames):
            mono_samples.append((left[i] - right[i]) // 2)
    else:
        raise ValueError("Incorrect channel value")
    
    # Prepare the new header for the mono file
    new_num_channels = 1
    new_block_align = new_num_channels * (bits_per_sample // 8)
    new_subchunk2_size = n_frames * new_block_align
    new_chunk_size = 36 + new_subchunk2_size
    mono_data = struct.pack('<' + 'h' * n_frames, *mono_samples)
    
    outfile = open(ficMono, 'wb')
    write_wav_header(outfile, new_chunk_size, new_subchunk2_size, new_num_channels, header[7], bits_per_sample)
    outfile.write(mono_data)
    outfile.close()
```

##### Código de `mono2estereo()`
```py
def mono2estereo(ficIzq, ficDer, ficEste):
    # Read the left file
    f_izq = open(ficIzq, 'rb')
    header_izq = read_wav_header(f_izq)
    if header_izq[6] != 1 or header_izq[10] != 16:
        f_izq.close()
        raise ValueError("The left file must be 16-bit mono")
    subchunk2_size_izq = header_izq[12]
    n_frames = subchunk2_size_izq // (header_izq[10] // 8)
    data_izq = f_izq.read(subchunk2_size_izq)
    f_izq.close()
    
    # Read the right file
    f_der = open(ficDer, 'rb')
    header_der = read_wav_header(f_der)
    if header_der[6] != 1 or header_der[10] != 16:
        f_der.close()
        raise ValueError("The right file must be 16-bit mono")
    subchunk2_size_der = header_der[12]
    n_frames_der = subchunk2_size_der // (header_der[10] // 8)
    if n_frames_der != n_frames:
        f_der.close()
        raise ValueError("Mono files have a different number of samples")
    data_der = f_der.read(subchunk2_size_der)
    f_der.close()
    
    # Extract individual samples with a simple loop
    samples_izq = list(struct.unpack('<' + 'h' * n_frames, data_izq))
    samples_der = list(struct.unpack('<' + 'h' * n_frames, data_der))
    
    # Combine the samples of both channels in an alternating fashion
    stereo_samples = []
    for i in range(n_frames):
        stereo_samples.append(samples_izq[i])
        stereo_samples.append(samples_der[i])
    
    new_num_channels = 2
    bits = header_izq[10]  # 16 bits
    new_block_align = new_num_channels * (bits // 8)
    new_subchunk2_size = n_frames * new_block_align
    new_chunk_size = 36 + new_subchunk2_size
    stereo_data = struct.pack('<' + 'h' * (n_frames * 2), *stereo_samples)
    
    f_out = open(ficEste, 'wb')
    write_wav_header(f_out, new_chunk_size, new_subchunk2_size, new_num_channels, header_izq[7], bits)
    f_out.write(stereo_data)
    f_out.close()
```

##### Código de `codEstereo()`
```py
def codEstereo(ficEste, ficCod):
    f_in = open(ficEste, 'rb')
    header = read_wav_header(f_in)
    if header[6] != 2 or header[10] != 16:
        f_in.close()
        raise ValueError("The input file must be 16-bit stereo")
    subchunk2_size = header[12]
    frame_size = 2 * (header[10] // 8)
    n_frames = subchunk2_size // frame_size
    data = f_in.read(subchunk2_size)
    f_in.close()
    
    stereo_samples = struct.unpack('<' + 'h' * (n_frames * 2), data)
    
    left = []
    right = []
    for i in range(n_frames):
        left.append(stereo_samples[2*i])
        right.append(stereo_samples[2*i+1])
    
    codes = []
    for i in range(n_frames):
        # Calculate half-sum and half-difference
        s = (left[i] + right[i]) // 2
        d = (left[i] - right[i]) // 2
        # Combine into 32 bits (not very optimized, but okay)
        code = (s << 16) | (d & 0xFFFF)
        codes.append(code)
    
    new_num_channels = 1
    bits = 32
    new_block_align = new_num_channels * (bits // 8)
    new_subchunk2_size = n_frames * new_block_align
    new_chunk_size = 36 + new_subchunk2_size
    cod_data = struct.pack('<' + 'i' * n_frames, *codes)
    
    f_out = open(ficCod, 'wb')
    write_wav_header(f_out, new_chunk_size, new_subchunk2_size, new_num_channels, header[7], bits)
    f_out.write(cod_data)
    f_out.close()
```

##### Código de `decEstereo()`
```py
def decEstereo(ficCod, ficEste):
    f_in = open(ficCod, 'rb')
    header = read_wav_header(f_in)
    if header[6] != 1 or header[10] != 32:
        f_in.close()
        raise ValueError("The encoded file must be 32-bit mono")
    subchunk2_size = header[12]
    n_samples = subchunk2_size // (header[10] // 8)
    data = f_in.read(subchunk2_size)
    f_in.close()
    
    codes = struct.unpack('<' + 'i' * n_samples, data)
    
    left = []
    right = []
    for code in codes:
        s = code >> 16
        d = code & 0xFFFF
        if d >= 0x8000:
            d = d - 0x10000
        left.append(s + d)
        right.append(s - d)
    
    stereo_samples = []
    for i in range(n_samples):
        stereo_samples.append(left[i])
        stereo_samples.append(right[i])
    
    new_num_channels = 2
    bits = 16
    new_block_align = new_num_channels * (bits // 8)
    new_subchunk2_size = n_samples * new_block_align
    new_chunk_size = 36 + new_subchunk2_size
    stereo_data = struct.pack('<' + 'h' * (n_samples * 2), *stereo_samples)
    
    f_out = open(ficEste, 'wb')
    write_wav_header(f_out, new_chunk_size, new_subchunk2_size, new_num_channels, header[7], bits)
    f_out.write(stereo_data)
    f_out.close()
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
