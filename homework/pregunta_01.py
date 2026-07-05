# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import zipfile
import os
import pandas as pd

def pregunta_01():# 1. Creamos dos listas vacías para ir acumulando los textos de cada grupo
    datos_train = []
    datos_test = []
    
    # Definimos cuáles son las carpetas "hijo" que nos interesan
    hijos_validos = ['negative', 'positive', 'neutral']
    
    # 2. Abrimos el archivo .zip
    with zipfile.ZipFile("files/input.zip", 'r') as archivo_zip:
        
        # Recorremos absolutamente todos los archivos dentro del ZIP
        for ruta_interna in archivo_zip.namelist():
            
            # Filtro básico: Solo nos interesan los archivos .txt
            if ruta_interna.endswith('.txt'):
                
                # --- AQUÍ APRENDEMOS A USAR LOS NOMBRES DE LAS CARPETAS ---
                # Si la ruta es "datos/train/positive/archivo123.txt", la rompemos por sus barras '/'
                partes_ruta = ruta_interna.split('/')
                # partes_ruta se convierte en: ['datos', 'train', 'positive', 'archivo123.txt']
                
                # Necesitamos asegurarnos de que la ruta tenga suficientes carpetas para analizar
                if len(partes_ruta) >= 3:
                    
                    # Recorremos los nombres de las carpetas para buscar los pares Padre e Hijo
                    for i in range(len(partes_ruta) - 2):
                        padre = partes_ruta[i].lower()      # Puede ser 'train' o 'test'
                        hijo = partes_ruta[i+1].lower()     # Puede ser 'negative', 'positive', etc.
                        
                        # VALIDACIÓN: ¿Cumple con tu regla de negocio?
                        if padre in ['train', 'test'] and hijo in hijos_validos:
                            
                            # 3. LEER EL TEXTO: Como queremos TODO el texto del archivo en una sola celda,
                            # usamos .read() en lugar de recorrer línea por línea.
                            with archivo_zip.open(ruta_interna) as f:
                                texto_completo = f.read().decode('utf-8').strip()
                            
                            # 4. CREAR EL REGISTRO: Aquí es donde usas los nombres de las carpetas
                            registro = {
                                "phrase": texto_completo,  # Tu requerimiento: el texto va aquí
                                "target": hijo             # ¡Aquí usas el nombre de la carpeta hijo! (e.g., 'positive')
                            }
                            
                            # 5. CLASIFICACIÓN: Dependiendo del padre, lo mandas a una lista o a la otra
                            if padre == 'train':
                                datos_train.append(registro)
                            elif padre == 'test':
                                datos_test.append(registro)
                            
                            break # Ya encontramos su clasificación, no necesitamos seguir buscando en esta ruta
                            
    # --- FIN DEL BUCLE: HORA DE CREAR LOS DOS CSV ---
    
    # Nos aseguramos de que la carpeta de salida exista en tu computadora
    if not os.path.exists('files/output'):
        os.makedirs('files/output')
        
    # Convertimos la lista de TRAIN en su CSV correspondiente
    if datos_train:
        df_train = pd.DataFrame(datos_train)
        ruta_train_csv = os.path.join('files/output', "train_dataset.csv")
        df_train.to_csv(ruta_train_csv, index=False, encoding='utf-8')
        
        
    # Convertimos la lista de TEST en su CSV correspondiente
    if datos_test:
        df_test = pd.DataFrame(datos_test)
        ruta_test_csv = os.path.join('files/output', "test_dataset.csv")
        df_test.to_csv(ruta_test_csv, index=False, encoding='utf-8')
        
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
