# Sonido estéreo y ficheros WAVE

## Albert Batlló Marin

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

Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los
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
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los  datos de las cabeceras de los ficheros para conseguirlo.

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
```
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
```

##### Código de `mono2estereo()`
```
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
```

##### Código de `codEstereo()`
```
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
```

##### Código de `decEstereo()`
```
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

```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
