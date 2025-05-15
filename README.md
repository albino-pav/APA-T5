# Sonido estéreo y ficheros WAVE

## Sebastian Pérez Capitano

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
    with open(ficEste, 'rb') as f:
        size, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, byte_rate, block_align, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El fichero no contiene audio estéreo de 16 bits.")
        data_chunk = next(c for c in chunks if c[0] == b'data')
        datos = data_chunk[2]
        muestras = struct.unpack('<' + 'h' * (len(datos) // 2), datos)
        izq = muestras[::2]
        der = muestras[1::2]
        
        if canal == 0:
            mono = izq
        elif canal == 1:
            mono = der
        elif canal == 2:
            mono = [((l + r) // 2) for l, r in zip(izq, der)]
        elif canal == 3:
            mono = [((l - r) // 2) for l, r in zip(izq, der)]
        else:
            raise ValueError("Canal debe ser 0 (izq), 1 (der), 2 (L+R)/2, o 3 (L-R)/2.")

        datos_mono = struct.pack('<' + 'h'*len(mono), *mono)
        fmt_mono = struct.pack('<HHIIHH', audio_format, 1, sample_rate, sample_rate*2, 2, 16) + fmt[16:]
        with open(ficMono, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_mono), fmt_mono),
                (b'data', len(datos_mono), datos_mono)
            ])
```

##### Código de `mono2estereo()`

```py
def mono2estereo(ficIzq, ficDer, ficEste):
    with open(ficIzq, 'rb') as f1, open(ficDer, 'rb') as f2:
        _, c1 = leer_cabecera(f1)
        _, c2 = leer_cabecera(f2)
        fmt1 = next(c for c in c1 if c[0] == b'fmt ')[2]
        fmt2 = next(c for c in c2 if c[0] == b'fmt ')[2]
        if fmt1 != fmt2:
            raise ValueError("Los ficheros mono no tienen el mismo formato.")
        datos1 = struct.unpack('<' + 'h'*(len(c1[-1][2]) // 2), c1[-1][2])
        datos2 = struct.unpack('<' + 'h'*(len(c2[-1][2]) // 2), c2[-1][2])
        if len(datos1) != len(datos2):
            raise ValueError("Los ficheros mono no tienen la misma longitud.")
        intercalado = [val for pair in zip(datos1, datos2) for val in pair]
        datos_stereo = struct.pack('<' + 'h'*len(intercalado), *intercalado)
        audio_format, _, sample_rate, _, _, _ = struct.unpack('<HHIIHH', fmt1[:16])
        fmt_stereo = struct.pack('<HHIIHH', audio_format, 2, sample_rate, sample_rate*4, 4, 16) + fmt1[16:]
        with open(ficEste, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_stereo), fmt_stereo),
                (b'data', len(datos_stereo), datos_stereo)
            ])
``` 

##### Código de `codEstereo()`
```py
def codEstereo(ficEste, ficCod):
    with open(ficEste, 'rb') as f:
        _, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 2 or bits_per_sample != 16:
            raise ValueError("El fichero debe ser estéreo y de 16 bits.")
        datos = struct.unpack('<' + 'h'*(len(chunks[-1][2]) // 2), chunks[-1][2])
        L = datos[::2]
        R = datos[1::2]
        cod = [(int(((l + r) // 2) << 16) | ((l - r) // 2 & 0xFFFF)) for l, r in zip(L, R)]
        datos_cod = struct.pack('<' + 'i'*len(cod), *cod)
        fmt_cod = struct.pack('<HHIIHH', 1, 1, sample_rate, sample_rate*4, 4, 32) + fmt[16:]
        with open(ficCod, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_cod), fmt_cod),
                (b'data', len(datos_cod), datos_cod)
            ])
```

##### Código de `decEstereo()`

```py
def decEstereo(ficCod, ficEste):
    with open(ficCod, 'rb') as f:
        _, chunks = leer_cabecera(f)
        fmt = next(c for c in chunks if c[0] == b'fmt ')[2]
        audio_format, num_channels, sample_rate, _, _, bits_per_sample = struct.unpack('<HHIIHH', fmt[:16])
        if num_channels != 1 or bits_per_sample != 32:
            raise ValueError("El fichero debe ser mono de 32 bits.")
        datos = struct.unpack('<' + 'i'*(len(chunks[-1][2]) // 4), chunks[-1][2])
        L = []
        R = []
        for val in datos:
            sum_ = (val >> 16)
            diff = val & 0xFFFF
            if diff >= 0x8000:
                diff -= 0x10000  # signo
            L.append(sum_ + diff)
            R.append(sum_ - diff)
        intercalado = [val for pair in zip(L, R) for val in pair]
        datos_estereo = struct.pack('<' + 'h'*len(intercalado), *intercalado)
        fmt_stereo = struct.pack('<HHIIHH', 1, 2, sample_rate, sample_rate*4, 4, 16) + fmt[16:]
        with open(ficEste, 'wb') as fout:
            escribir_cabecera(fout, [
                (b'fmt ', len(fmt_stereo), fmt_stereo),
                (b'data', len(datos_estereo), datos_estereo)
            ])
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
