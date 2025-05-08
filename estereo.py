import struct


def estereo2mono(ficEste, ficMono, canal=2):
    """
    La función lee el fichero ficEste, que debe contener una señal estéreo, 
    y escribe el fichero ficMono, con una señal monofónica. El tipo concreto 
    de señal que se almacenará en ficMono depende del argumento canal:
        
        - `canal=0`: Se almacena el canal izquierdo $L$.
        - `canal=1`: Se almacena el canal derecho $R$.
        - `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
        - `canal=3`: Se almacena la semidiferencia $(L-R)/2$.
    """

    # Open and read WAV file
    f_in = open(ficEste, 'rb')
    try:
        header = f_in.read(44)
        if header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
            raise ValueError("File is not a valid WAVE file")
        f_out.write
    finally: 
        f_in.close() 





    f_out = open(ficMono, 'wb')
    try:
        f_out.write(ProcessedContent)
    finally: 
        f_out.close() 


    






def mono2estereo(ficIzq, ficDer, ficEste):
    """
    Lee los ficheros ficIzq y ficDer, que contienen las señales monofónicas 
    correspondientes a los canales izquierdo y derecho, respectivamente, 
    y construye con ellas una señal estéreo que almacena en el fichero ficEste.
    """



def codEstereo(ficEste, ficCod):
    """
    Lee el fichero ficEste, que contiene una señal estéreo codificada con PCM 
    lineal de 16 bits, y construye con ellas una señal codificada con 32 bits 
    que permita su reproducción tanto por sistemas monofónicos como por sistemas 
    estéreo preparados para ello.
    """



def decEstereo(ficCod, ficEste):
    """
    Lee el fichero ficCod con una señal monofónica de 32 bits en la que los 16 
    bits más significativos contienen la semisuma de los dos canales de una señal 
    estéreo y los 16 bits menos significativos la semidiferencia, y escribe el 
    fichero ficEste con los dos canales por separado en el formato de los ficheros 
    WAVE estéreo.
    """