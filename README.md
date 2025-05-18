# Sonido estéreo y ficheros WAVE

## Arnau Piñero Masegosa

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
    Esta funcion lee el fichero 'ficEste', que contiene una señal estereo, y devuelve una
    señal monofonica en el fichero 'ficMono'. El tipo de señal monofonica depende del argumento
    'canal':
    canal = 0 ==> Se almacena en el canal izquierdo (L).
    canal = 1 ==> Se almacena en el canal derecho (R).
    canal = 2 ==> Se almacena la semisuma (L+R)/2. (Default)
    canal = 3 ==> Se almacena la semidiferencia (L-R)/2.
    """

    with open(ficEste, 'rb') as fpEstero:
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerData = list(st.unpack(formato, datos))
        # chunkID[0], chunkSize[1], format[2], chunk1ID[3], chunk1Size[4], audFormat[5], nChannels[6], sampleRate[7], bitRate[8], bAlign[9], bps[10], chunk2ID[11], fileSize[12]  
      
        if headerData[0] != b'RIFF' or headerData[2] != b'WAVE':
            raise Exception(f'El fichero {ficEste} no tiene formato WAVE.')
      
        with open(ficMono, 'wb') as fpMono:
            fpEstero.seek(44, 0) # Posicionamos el puntero de lectura al principio de los datos (byte 44)
            for i in range(0, headerData[12]):
                L = fpEstero.read(2)
                R = fpEstero.read(2)
          
            # Cambiamos el numero de canales en la cabecera
            headerData[6] = 1
            fpMono.write(headerData)

            if canal == 0:
                fpMono.write(L)

            elif canal == 1:
                fpMono.write(R)
              
            elif canal == 2:
                mono = (L+R)/2 
                fpMono.write(mono)
              
            elif canal == 3:
                mono = (L-R)/2
                fpMono.write(mono)
```

##### Código de `mono2estereo()`

```python
def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Esta funcion construye a partir de las señales monofonicas 'ficIzq' (L) y 'ficDer' (R)
    una señal estereo, que se almacena en el fichero 'ficEste'.
    """

    with open(ficIzq, 'rb') as fpIzq:
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerDataL = list(st.unpack(formato, datos))

        with open(ficDer, 'rb') as fpDer:
            formato = '<4sI4s4sIHHIIH4sI'
            datos = ficEste.read(st.calcsize(formato))
            headerDataR = list(st.unpack(formato, datos)) 

            # Comprovamos coincidencias por orden: RIFF, sampleRate, fileSize
            if headerDataL[0] != b'RIFF' or headerDataR[0] != b'RIFF':
                raise Exception(f'Los ficheros de entrada no tienen formato WAVE.')
            if headerDataL[7] != headerDataR[7]:
                raise Exception(f'La frequencia de muestro de los ficheros no coincide.')
            if headerDataL[12] != headerDataR[12]:
                raise Exception(f'El tamaño de los ficheros no coincide.')

            with open(ficEste, 'wb') as fpEste:
                # Cambiamos el numero de canales a 2 y añadimos la cabecera al fichero de salida
                headerDataL[6] = 2 
                fpEste.write(headerDataL)

                for i in range(0, len(fpDer)):
                    L = fpIzq.read(2)
                    R = fpDer.read(2)
                    fpEste.write(L)
                    fpEste.write(R)
```

##### Código de `codEstereo()`

```python
def codEstereo(ficEste, ficCod):
    """
    Esta funcion lee la señal estereo contenida en 'ficEste' codificada con PCM lineal de
    16 bits, y construye una señal codificada con 32 bits que permita su reproduccion tanto en 
    sistemas monofonicos cono en sistemas estero que lo permitan.
    """
  
    with open(ficEste, 'rb') as fpEste:
        # leemos la cabecera
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerData = list(st.unpack(formato, datos))

        if headerData[0] != b'RIFF' or headerData[2] != b'WAVE':
            raise Exception(f'El fichero {ficEste} no tiene formato WAVE.')

        for i in range(0, headerData[12]):
                L = fpEste.read(2)
                R = fpEste.read(2)

        semiSum = (L+R)/2
        semiDif = (L-R)/2

        with open(ficCod, 'wb') as fpCod:
            for i in range(0, len(semiSum), 2):
                fpCod.write(semiSum[i], semiSum[i+1])
                fpCod.write(semiDif[i], semiDif[i+1])
```

##### Código de `decEstereo()`

```python
def decEstereo(ficCod, ficEste):
    """
    Esta funcion lee la señal monofonnica de 32 bits contenida en 'ficCod' en la que los 
    16 MSB contienen la semisuma de los canales L y R, y los 16 LSB contienen la semidiferencia
    y escribe en 'ficEste' los dos canales por separado en formato WAVE estereo.
    """
  
    with open(ficCod, 'rb') as fpCod:
        # leemos la cabecera
        formato = '<4sI4s4sIHHIIH4sI'
        datos = ficEste.read(st.calcsize(formato))
        headerData = list(st.unpack(formato, datos))

        if headerData[0] != b'RIFF' or headerData[2] != b'WAVE':
            raise Exception(f'El fichero {ficEste} no tiene formato WAVE.')
      
        for i in range(0, headerData[12]):
            semiSum = fpCod.read(2)
            semiDif = fpCod.read(2)
      
        for i in range(0, len(semiSum)):
            R = -(4 * semiDif[i] - 4 * semiSum[i]) / 3
            L = 2 * semiSum[i] + 2 * (semiDif[i] - semiSum[i]) / 3

        with open(ficEste, 'wb') as fpEste:
            for i in range(0, len(semiSum), 2):
                fpEste.write(L[i], L[i+1])
                fpEste.write(R[i], R[i+1])
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
