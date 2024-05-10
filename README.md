# Sonido estéreo y ficheros WAVE

#### Nom i cognoms: Ona Bonastre

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión de señales de audio. En el fondo, se trata de un tipo particular de fichero [RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho, o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho, seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena `'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres, se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos *subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página [WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos, están dotados de dos órganos que actúan como transductores cústico-sensoriales (es decir, tienen dos *oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o *monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you* y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas. De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil, apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.

### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`, con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento `canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero `ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero \python{ficEste}, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero \python{ficCod} con una señal monofónica de 32 bits en la que los 16 bits más significativos contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la semidiferencia, y escribe el fichero \python{ficEste} con los dos canales por separado en el formato de los ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta. Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto. De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar innecesariamente la canción.

#### Código desarrollado

Inserte a continuación el código de los métodos desarrollados en esta tarea, usando los comandos necesarios para que se realice el realce sintáctico en Python del mismo (no vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).

##### Código de `leer_datos()`
```py
def leer_datos(fichero, num_canales):
    with open(fichero, 'rb') as fp_fichero:
        cabecera = fp_fichero.read(44)
        (riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, sample_rate, byte_rate, 
         block_align, bits_per_sample, data_id, data_size) = st.unpack(formato_cabecera, cabecera)
        
        cabecera = [riff, riff_size, wave, fmt, fmt_size, audio_format, n_channels, sample_rate, 
                    byte_rate, block_align, bits_per_sample, data_id, data_size]
        
        if n_channels != num_canales:
            raise ValueError("El archivo debe ser estéreo.")
        
        if riff != b"RIFF" or wave != b"WAVE":
            raise TypeError("File '{fp_estereo}' is not WAV file")
        
        data = fp_fichero.read(data_size)

        formato_datos = f'<{data_size // (bits_per_sample // 8)}h'
        datos = st.unpack(formato_datos, data)

    return cabecera, datos
```

##### Código de `escribir_fichero()`
```py
def escribir_fichero(fichero_out, n_channels, canal, cabecera, datos):
    with open(fichero_out, 'wb') as fp_out:
        if canal == 2 or canal == 3:
            cabecera[7] *= 2 
        byte_rate = cabecera[7] * n_channels * cabecera[10] // 8
        block_align = n_channels * cabecera[10] // 8
        data_size = len(datos) * (cabecera[10] // 8)
        riff_size = 36 + data_size

        nueva_cabecera = st.pack(formato_cabecera, cabecera[0], riff_size, cabecera[2], cabecera[3], cabecera[4], cabecera[5], 
                                 n_channels, cabecera[7], byte_rate, block_align, cabecera[10], cabecera[11], data_size)
        
        fp_out.write(nueva_cabecera)

        formato_out = f'<{len(datos)}h'
        datos_packed = st.pack(formato_out, *datos)
        fp_out.write(datos_packed)
```

##### Código de `estereo2mono()`
```py
def estereo2mono(ficEste, ficMono, canal=2):
    cabecera, datos_estereo = leer_datos(ficEste, 2)

    datos_mono = []
    if canal == 0:
        # Canal izquierdo
        datos_mono = datos_estereo[0::2]
    elif canal == 1:
        # Canal derecho
        datos_mono = datos_estereo[1::2]
    elif canal == 2:
        # Promedio de ambos canales
        datos_mono = [(datos_estereo[i] + datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
    elif canal == 3:
        # Diferencia entre ambos canales
        datos_mono = [(datos_estereo[i] - datos_estereo[i + 2]) // 2 for i in range(0, len(datos_estereo)-2)]
    else:
        raise ValueError("Canal inválido. Debe ser 0, 1, 2 o 3.")
    
    escribir_fichero(ficMono, 1, canal, cabecera, datos_mono)
```

##### Código de `mono2estereo()`
```py
def mono2estereo(ficIzq, ficDer, ficEste):
    cabeceraI, datos_Izq = leer_datos(ficIzq, 1)
    cabeceraD, datos_Der = leer_datos(ficDer, 1)

    if cabeceraI[7] != cabeceraD[7] or cabeceraI[10] != cabeceraD[10]:
        raise ValueError("Ambos archivos mono deben tener los mismos parámetros de audio.")
    
    if cabeceraI[5] != 16 or cabeceraD[5] != 16 or cabeceraI[6] != 1 or cabeceraD[6] != 1:
        raise ValueError("Ambos archivos mono deben estar codificados con PCM lineal con 16 bits.")

    datos_estereo = []
    for mostraI, mostraD in zip(datos_Izq, datos_Der):
        datos_estereo.append(mostraI)
        datos_estereo.append(mostraD)

    escribir_fichero(ficEste, 2, -1, cabeceraI, datos_estereo)
```

##### Código de `codEstereo()`
```py
def codEstereo(ficEste, ficCod):
    canalIz = "APA-T5\wav\semisuma_estereo.wav"
    canalDer = "APA-T5\wav\semidiferencia_estereo.wav"
    estereo2mono(ficEste, canalIz, 2)
    estereo2mono(ficEste, canalDer, 3)
    mono2estereo(canalIz, canalDer, ficCod)
```

##### Código de `decEstereo()`
```py
def decEstereo(ficCod, ficEste):
    ficCod_monoI = "APA-T5\wav\ficCod_monoI.wav"
    ficCod_monoD = "APA-T5\wav\ficCod_monoD.wav"
    estereo2mono(ficCod, ficCod_monoI, 0)
    estereo2mono(ficCod, ficCod_monoD, 1)
    mono2estereo(ficCod_monoI, ficCod_monoD, ficEste)
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en el repositorio, incluyendo el realce sintáctico del código fuente insertado.
