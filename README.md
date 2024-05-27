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

```python

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

```

##### Código de `mono2estereo()`


```python

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


```

##### Código de `codEstereo()`

```python

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


```

##### Código de `decEstereo()`

```python

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
    

```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
