# Convertir Notebooks a .py, outputs e imágenes con Streamlit

Este proyecto permite subir archivos `.ipynb` y extraer:
1. Un archivo `.py` consolidado con todo el código de las celdas.
2. Un archivo `outputs.txt` con la salida de texto de cada celda.
3. Las imágenes generadas durante la ejecución de cada notebook en formato `.png`.

## Requisitos

- [Python 3.7+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) (ver `requirements.txt`)

## Uso

1. Clona o descarga este repositorio.
2. Instala las dependencias con:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación con:
   ```bash
   streamlit run app.py
   ```
   O bien, en Windows, haz doble clic en `run_app.bat`.

4. En el navegador, arrastra tus archivos `.ipynb`. El sistema creará una carpeta por cada archivo subido.

## Estructura de salida

Por cada archivo `.ipynb` subido, se creará una carpeta con el mismo nombre (sin extensión), y dentro:
- `<nombre>.py`
- `outputs.txt`
- `image_1.png`, `image_2.png`, etc. (si hubo imágenes)

¡Disfruta!
```

---

### Notas finales

- Este ejemplo asume que solo quieres **concatenar** todo el código en un único `.py`. Ten en cuenta que no se mantiene la separación por celdas ni se incluyen magic commands de IPython (como `%matplotlib inline`) de forma especial. Solo se copian literalmente.
- Para los **outputs**, se toma la salida textual o imágenes base64 encontradas en los metadatos del notebook. Si hay otros tipos de output (HTML, JavaScript), se omiten o tendrás que personalizar la extracción.  
- Asegúrate de tener los permisos de escritura en la carpeta donde corres la app.  

¡Listo! Con este contenido ya tienes todo lo necesario para crear tu repositorio en GitHub y un `.bat` para que puedas correr tu aplicación de Streamlit desde tu Escritorio en Windows. ¡Éxito con tu proyecto!