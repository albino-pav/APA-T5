# Sonido estéreo y ficheros WAVE

## Biel Bernal Pratdesaba

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
def estereo2mono(ficEste, ficMono, canal=2):
    """
    La funció llegeix el fitxer ficEste, que ha de contenir un senyal estèreo, i escriu el fitxer 
    ficMono, amb un senyal monofònic. El tipus concret de senyal que s'emmagatzemarà a ficMono
    depèn de l'argument canal:

    - canal=0: S'emmagatzema el canal esquerre (L).
    - canal=1: S'emmagatzema el canal dret (R).
    - canal=2: S'emmagatzema la semisuma (L + R) / 2.
    - canal=3: S'emmagatzema la semidiferència (L - R) / 2.

    """

    with open(ficEste, "rb") as fpEste:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpEste.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpEste.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpEste.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 2 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, estèreo i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpEste.seek(36, 0)
        formato = "<4sI"
        datos = fpEste.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpEste.read(st.calcsize(formato))
        mostres = st.unpack(formato, dades)

    # Passem de stereo a mono
    mostStereo = list(zip(mostres[::2], mostres[1::2]))
    if canal == 0:
        senyalMono = [L for L, R in mostStereo]
    elif canal == 1:
        senyalMono = [R for L, R in mostStereo]
    elif canal == 2:
        senyalMono = [(L + R) // 2 for L, R in mostStereo]
    elif canal == 3:
        senyalMono = [(L - R) // 2 for L, R in mostStereo]
    else:
        raise ValueError("El canal ha de ser 0, 1, 2 o 3")
    
    # Calcular mides per la capçalera mono
    subChunk2SizeMono = len(senyalMono) * 2
    chunkSizeMono = 36 + subChunk2SizeMono

    # Escriure el nou fitxer 
    with open(ficMono, "wb") as fpMono:
        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        fpMono.write(st.pack(formato, b"RIFF", chunkSizeMono, b"WAVE"))

        # Subchunk1 (fmt)
        formato = "<4sIHHIIHH"
        fpMono.write(st.pack(formato, b"fmt ", 16, 1, 1,
                             sampleRate, sampleRate * 2, 2, 16))

        # Subchunk2 (data)
        formato = "<4sI"
        fpMono.write(st.pack(formato, b"data", subChunk2SizeMono))

        # Dades mono
        formato = f"<{len(senyalMono)}h"
        fpMono.write(st.pack(formato, *senyalMono))
```

##### Código de `mono2estereo()`
```python
def mono2stereo(ficIzq, ficDer, ficEste):
    """
    Llegeix els fitxers ficIzq i ficDer, que contenen els senyals monofònics corresponents als
    canals esquerre i dret, respectivament, i construeix amb ells un senyal estèreo que s'emmagatzema 
    al fitxer ficEste.

    """

    # Llegir el fitxer del canal L
    with open(ficIzq, "rb") as fpIzq:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpIzq.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpIzq.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpIzq.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRateL, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, mono i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpIzq.seek(36, 0)
        formato = "<4sI"
        datos = fpIzq.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # Nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpIzq.read(st.calcsize(formato))
        mostresL = st.unpack(formato, dades)

    # Llegir el fitxer del canal R
    with open(ficDer, "rb") as fpDer:

        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpDer.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpDer.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpDer.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRateR, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, mono i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpDer.seek(36, 0)
        formato = "<4sI"
        datos = fpDer.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres mono
        numMostres = subChunk2Size // 2  # Nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpDer.read(st.calcsize(formato))
        mostresR = st.unpack(formato, dades)

    # Comvinem les mostres en una sola senyal de 2 canals
    mostresStereo = []
    for L, R in zip(mostresL, mostresR):
        mostresStereo.append(L)
        mostresStereo.append(R)

    # Calcular mides per la capçalera stereo
    subChunk2SizeStereo = len(mostresStereo) * 2
    chunkSizeStereo = 36 + subChunk2SizeStereo

    # Escriure el nou fitxer 
    with open(ficEste, "wb") as fpEste:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpEste.write(st.pack(formato, b"RIFF", chunkSizeStereo, b"WAVE"))

        # Subchunk1 'fmt ' (estèreo, 2 canals, 16 bits)
        formato = "<4sIHHIIHH"
        fpEste.write(st.pack(formato, b"fmt ", 16, 1, 2, sampleRateL, sampleRateL * 4, 4, 16))

        # Subchunk2 'data'
        formato = "<4sI"
        fpEste.write(st.pack(formato, b"data", subChunk2SizeStereo))

        # Mostres
        formato = f"<{len(mostresStereo)}h"
        fpEste.write(st.pack(formato, *mostresStereo))
```

##### Código de `codEstereo()`
```python
def codEstereo(ficEste, ficCod):
    """
    Llegeix un fitxer WAVE estèreo de 16 bits i genera un fitxer mono de 32 bits on:
    - Els 16 bits alts contenen la semisuma (L+R)//2
    - Els 16 bits baixos contenen la semidiferència (L-R)//2
    """
    with open(ficEste, "rb") as fpEste:
        # Capçalera inicial (RIFF)
        formato = "<4sI4s"
        datos = fpEste.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, datos)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"El fitxer {ficEste} no té un format WAVE vàlid.")

        # Subchunk1 'fmt ' (offset 12)
        fpEste.seek(12, 0)
        formato = "<4sIHHIIHH"
        datos = fpEste.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, datos)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 2 or bitsPerSample != 16:
            raise Exception("El fitxer ha de ser PCM, estèreo i de 16 bits.")

        # Subchunk2 'data' (offset 36)
        fpEste.seek(36, 0)
        formato = "<4sI"
        datos = fpEste.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, datos)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")
        
        # Llegim les mostres stereo
        numMostres = subChunk2Size // 2  # nombre total de valors de 2 bytes
        formato = f"<{numMostres}h"
        dades = fpEste.read(st.calcsize(formato))
        mostres = st.unpack(formato, dades)

    # Codifiquem les mostres L, R en 32 bits
    codificats = []
    for R, L in zip(mostres[::2], mostres[1::2]):
        semisuma = (L + R) // 2
        semidiferencia = (L - R) // 2
        valor32bits = st.unpack("<I", st.pack("<hh", semisuma, semidiferencia))[0]
        codificats.append(valor32bits) 
    
    subChunk2Size = len(codificats) * 4  # 4 bytes per mostra
    chunkSize = 36 + subChunk2Size

    with open(ficCod, "wb") as fpCod:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpCod.write(st.pack(formato, b"RIFF", chunkSize, b"WAVE"))

        # Subchunk1 'fmt ' (PCM 32 bits mono)
        formato = "<4sIHHIIHH"
        fpCod.write(st.pack(formato, b"fmt ", 16, 1, 1,
                            sampleRate, sampleRate * 4, 4, 32))

        # Subchunk2 'data'
        formato = "<4sI"
        fpCod.write(st.pack(formato, b"data", subChunk2Size))

        # Dades codificades (32 bits unsigned int)
        formato = f"<{len(codificats)}I"
        fpCod.write(st.pack(formato, *codificats))
```

##### Código de `decEstereo()`
```python
def decEstereo(ficCod, ficEste):
    """
    Llegeix un fitxer WAVE mono de 32 bits amb semisuma i semidiferència codificades,
    i reconstrueix un fitxer estèreo de 16 bits amb els canals esquerre i dret originals.
    """
    with open(ficCod, "rb") as fpCod:
        # Capçalera RIFF
        formato = "<4sI4s"
        dades = fpCod.read(st.calcsize(formato))
        chunkID, chunkSize, format = st.unpack(formato, dades)

        if chunkID != b"RIFF" or format != b"WAVE":
            raise Exception(f"{ficCod} no és un fitxer WAVE vàlid.")

        # Subchunk1 'fmt '
        fpCod.seek(12)
        formato = "<4sIHHIIHH"
        dades = fpCod.read(st.calcsize(formato))
        subChunk1ID, subChunk1Size, audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = st.unpack(formato, dades)

        if subChunk1ID != b"fmt " or audioFormat != 1 or numChannels != 1 or bitsPerSample != 32:
            raise Exception("El fitxer ha de ser mono, PCM i de 32 bits.")

        # Subchunk2 'data'
        fpCod.seek(36)
        formato = "<4sI"
        dades = fpCod.read(st.calcsize(formato))
        subChunk2ID, subChunk2Size = st.unpack(formato, dades)

        if subChunk2ID != b"data":
            raise Exception("No s'ha trobat el subchunk 'data' on esperat (offset 36).")

        # Llegim les mostres codificades (32 bits cada una)
        numMostres = subChunk2Size // 4
        formato = f"<{numMostres}I"
        dades = fpCod.read(st.calcsize(formato))
        codificats = st.unpack(formato, dades)

    # Reconstruïm L i R
    mostresStereo = []
    for cod in codificats:
        bytes32 = st.pack("<I", cod)
        semisuma, semidiferencia = st.unpack("<hh", bytes32)
        L = semisuma + semidiferencia
        R = semisuma - semidiferencia
        mostresStereo.extend([R, L])  

    # Capçaleres del fitxer estèreo (16 bits, 2 canals)
    subChunk2SizeStereo = len(mostresStereo) * 2
    chunkSizeStereo = 36 + subChunk2SizeStereo

    with open(ficEste, "wb") as fpEste:
        # Capçalera RIFF
        formato = "<4sI4s"
        fpEste.write(st.pack(formato, b"RIFF", chunkSizeStereo, b"WAVE"))

        # Subchunk1 'fmt '
        formato = "<4sIHHIIHH"
        fpEste.write(st.pack(formato, b"fmt ", 16, 1, 2,
                             sampleRate, sampleRate * 4, 4, 16))

        # Subchunk2 'data'
        formato = "<4sI"
        fpEste.write(st.pack(formato, b"data", subChunk2SizeStereo))

        # Dades L-R de 16 bits
        formato = f"<{len(mostresStereo)}h"
        fpEste.write(st.pack(formato, *mostresStereo))
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
