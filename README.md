# Sonido estéreo y ficheros WAVE

## Àlex Segura Medina

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

```python
def estereo2mono(ficEste, ficMono, canal = 2):

    """
    
    Convierte un archivo WAVE estéreo a mono en función del canal indicado:
    0 = izquierdo, 1 = derecho, 2 = semisuma, 3 = semidiferencia.

    """
    with open(ficEste, 'rb') as fe:
        cabecera = fe.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido")

        fmt_tag, n_channels, sample_rate, byte_rate, block_align, bps = struct.unpack('<HHIIHH', cabecera[20:36])
        if n_channels != 2 or fmt_tag != 1 or bps != 16:
            raise ValueError("El fichero no es estéreo o no usa PCM lineal de 16 bits")

        data_size = struct.unpack('<I', cabecera[40:44])[0]
        num_frames = data_size // 4  # 4 bytes por muestra estéreo (2 bytes por canal)
        datos = fe.read()

    muestras = struct.unpack('<' + 'hh'*num_frames, datos)
    if canal == 0:
        canal_mono = [muestras[i] for i in range(0, len(muestras), 2)]
    elif canal == 1:
        canal_mono = [muestras[i] for i in range(1, len(muestras), 2)]
    elif canal == 2:
        canal_mono = [(muestras[i] + muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
    elif canal == 3:
        canal_mono = [(muestras[i] - muestras[i+1]) // 2 for i in range(0, len(muestras), 2)]
    else:
        raise ValueError("Parámetro 'canal' no válido. Usa 0, 1, 2 o 3.")

    nuevo_data_size = len(canal_mono) * 2  # 2 bytes por muestra
    nuevo_byte_rate = sample_rate * 2
    nuevo_block_align = 2
    with open(ficMono, 'wb') as fm:
        fm.write(b'RIFF')
        fm.write(struct.pack('<I', 36 + nuevo_data_size))
        fm.write(b'WAVE')
        fm.write(b'fmt ')
        fm.write(struct.pack('<IHHIIHH', 16, 1, 1, sample_rate,
                             nuevo_byte_rate, nuevo_block_align, 16))
        fm.write(b'data')
        fm.write(struct.pack('<I', nuevo_data_size))
        fm.write(struct.pack('<' + 'h'*len(canal_mono), *canal_mono))
```

##### Código de `mono2estereo()`

```python
def mono2estereo(ficIzq, ficDer, ficEste):
    """

    Genera un archivo WAVE estéreo combinando dos archivos WAVE mono.

    """
    with open(ficIzq, 'rb') as fz:
        header_izq = fz.read(44)
        if header_izq[0:4] != b'RIFF' or header_izq[8:12] != b'WAVE':
            raise ValueError("ficIzq no es un fichero WAVE válido")
        fmt_tag, nchannels, sample_rate, _, _, bps = struct.unpack('<HHIIHH', header_izq[20:36])
        if nchannels != 1 or fmt_tag != 1 or bps != 16:
            raise ValueError("ficIzq no es un fichero mono PCM 16-bit válido")
        data_izq = fz.read()

    with open(ficDer, 'rb') as fd:
        header_der = fd.read(44)
        if header_der[0:4] != b'RIFF' or header_der[8:12] != b'WAVE':
            raise ValueError("ficDer no es un fichero WAVE válido")
        fmt_tag_d, nchannels_d, sample_rate_d, _, _, bps_d = struct.unpack('<HHIIHH', header_der[20:36])
        if nchannels_d != 1 or fmt_tag_d != 1 or bps_d != 16:
            raise ValueError("ficDer no es un fichero mono PCM 16-bit válido")
        if sample_rate_d != sample_rate or bps_d != bps:
            raise ValueError("Los ficheros mono no tienen la misma configuración")
        data_der = fd.read()

    muestras_izq = struct.unpack('<' + 'h' * (len(data_izq) // 2), data_izq)
    muestras_der = struct.unpack('<' + 'h' * (len(data_der) // 2), data_der)
    if len(muestras_izq) != len(muestras_der):
        raise ValueError("Los ficheros mono no tienen el mismo número de muestras")

    intercaladas = [val for pair in zip(muestras_izq, muestras_der) for val in pair]
    data_size = len(intercaladas) * 2  # 2 bytes por muestra
    byte_rate = sample_rate * 4        # 2 canales x 2 bytes
    block_align = 4                    # 2 canales x 2 bytes

    with open(ficEste, 'wb') as fe:
        fe.write(b'RIFF')
        fe.write(struct.pack('<I', 36 + data_size))
        fe.write(b'WAVE')
        fe.write(b'fmt ')
        fe.write(struct.pack('<IHHIIHH', 16, 1, 2, sample_rate,
                             byte_rate, block_align, 16))
        fe.write(b'data')
        fe.write(struct.pack('<I', data_size))
        fe.write(struct.pack('<' + 'h' * len(intercaladas), *intercaladas))

```

##### Código de `codEstereo()`

```python

def codEstereo(ficEste, ficCod):
    """

    Lee un fichero estéreo de 16 bits por canal (ficEste) y genera un fichero ficCod
    de 32 bits por muestra.
    El resultado permite ser reproducido como mono (semisuma) o reconstruido como estéreo.

    """
    with open(ficEste, 'rb') as f:
        cabecera = f.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido.")
        fmt = cabecera[20:22]
        nchannels = struct.unpack('<H', cabecera[22:24])[0]
        sampwidth = struct.unpack('<H', cabecera[34:36])[0]

        if fmt != b'\x01\x00' or nchannels != 2 or sampwidth != 16:
            raise ValueError("El fichero debe ser PCM, estéreo, 16 bits por muestra.")

        datos = f.read()

    # Extraer muestras como enteros de 16 bits
    muestras = struct.unpack('<' + 'h'*(len(datos)//2), datos)
    left = muestras[::2]
    right = muestras[1::2]

    # Calcular semisuma y semidiferencia
    sumas = [(l + r) // 2 for l, r in zip(left, right)]
    diffs = [(l - r) // 2 for l, r in zip(left, right)]

    # Combinar en 32 bits (semisuma << 16) | (semidiferencia & 0xFFFF)
    samples_32bit = [(suma << 16) | (diff & 0xFFFF) for suma, diff in zip(sumas, diffs)]

    # Crear nueva cabecera WAVE para 1 canal, 32 bits por muestra
    nuevo_num_channels = 1
    nuevo_bits_per_sample = 32
    sample_rate = struct.unpack('<I', cabecera[24:28])[0]
    byte_rate = sample_rate * nuevo_num_channels * nuevo_bits_per_sample // 8
    block_align = nuevo_num_channels * nuevo_bits_per_sample // 8
    data_size = len(samples_32bit) * 4
    chunk_size = 36 + data_size

    nueva_cabecera = (
        b'RIFF' +
        struct.pack('<I', chunk_size) +
        b'WAVE' +
        b'fmt ' +
        struct.pack('<I', 16) +             # Subchunk1Size
        struct.pack('<H', 1) +              # AudioFormat: PCM
        struct.pack('<H', nuevo_num_channels) +
        struct.pack('<I', sample_rate) +
        struct.pack('<I', byte_rate) +
        struct.pack('<H', block_align) +
        struct.pack('<H', nuevo_bits_per_sample) +
        b'data' +
        struct.pack('<I', data_size)
    )

    with open(ficCod, 'wb') as f:
        f.write(nueva_cabecera)
        f.write(struct.pack('<' + 'i'*len(samples_32bit), *samples_32bit))

```


##### Código de `decEstereo()`

```python
def decEstereo(ficCod, ficEste):
    """

    Decodifica un fichero codificado en 32 bits por muestra (ficCod), donde:
    - Los 16 bits más significativos contienen la semisuma (L + R) // 2
    - Los 16 bits menos significativos contienen la semidiferencia (L - R) // 2
    para obtener los canales izquierdo y derecho originales.

    Guarda el resultado en un fichero estéreo de 16 bits por muestra (ficEste).

    """
    with open(ficCod, 'rb') as f:
        cabecera = f.read(44)
        if cabecera[0:4] != b'RIFF' or cabecera[8:12] != b'WAVE':
            raise ValueError("El fichero de entrada no es un WAVE válido.")

        num_channels = struct.unpack('<H', cabecera[22:24])[0]
        bits_per_sample = struct.unpack('<H', cabecera[34:36])[0]

        if num_channels != 1 or bits_per_sample != 32:
            raise ValueError("El fichero debe tener 1 canal y 32 bits por muestra.")

        sample_rate = struct.unpack('<I', cabecera[24:28])[0]
        data = f.read()

    muestras_32bit = struct.unpack('<' + 'i' * (len(data) // 4), data)

    semisumas = [(m >> 16) for m in muestras_32bit]
    semidiffs = [((m & 0xFFFF) ^ 0x8000) - 0x8000 for m in muestras_32bit]  # Convertir a signed short

    left = [s + d for s, d in zip(semisumas, semidiffs)]
    right = [s - d for s, d in zip(semisumas, semidiffs)]

    # Crear nueva cabecera WAVE para 2 canales de 16 bits
    nuevo_num_channels = 2
    nuevo_bits_per_sample = 16
    byte_rate = sample_rate * nuevo_num_channels * nuevo_bits_per_sample // 8
    block_align = nuevo_num_channels * nuevo_bits_per_sample // 8
    data_size = len(left) * 2 * 2  # 2 canales * 2 bytes por muestra
    chunk_size = 36 + data_size

    nueva_cabecera = (
        b'RIFF' +
        struct.pack('<I', chunk_size) +
        b'WAVE' +
        b'fmt ' +
        struct.pack('<I', 16) +
        struct.pack('<H', 1) +
        struct.pack('<H', nuevo_num_channels) +
        struct.pack('<I', sample_rate) +
        struct.pack('<I', byte_rate) +
        struct.pack('<H', block_align) +
        struct.pack('<H', nuevo_bits_per_sample) +
        b'data' +
        struct.pack('<I', data_size)
    )

    # Intercalar las muestras L y R
    intercaladas = [val for par in zip(left, right) for val in par]

    with open(ficEste, 'wb') as f:
        f.write(nueva_cabecera)
        f.write(struct.pack('<' + 'h' * len(intercaladas), *intercaladas))

```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
