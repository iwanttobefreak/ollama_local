**Uso de RAG para gestionar conextos**
RAG (Retrieval-Augmented Generation) es un sistema que almacena datos y documentos en una base de datos vectorial y luego los puede buscar y generar LLM.

Vamos a crear una API para poder introducir frases como si fuera un diario personal y luego poder ir preguntando

Primero creamos un directorio para nuestro RAG dentro del docker:
```bash
docker exec -ti ollama bash
```

```bash
mkdir /app/datos/diario
```

Instalamos el modelo que usa la API para RAG:
```bash
ollama pull nomic-embed-text
```

Entramos en el directorio de leccion05:
```bash
cd /app/lecciones/leccion05
```

Tenemos los ficheros:
- diario.txt
  Fichero con entradas del tipo: **"tal día hice esto en este lugar y fué así"**
- procesar_entrada_batch.py
  Procesa las entradas de diario.txt y las mete en el RAG creado en /app/datos/diario
  Crea BBDD y datos vectoriales en /app/datos/diario/diario_chroma_db/. También crea un fichero a modo de resumen en  /app/datos/diario/diario_personal_vida.txt donde saca las palabras clave de cada entrada del diario y un resumen. Tiene el formato:

```
[FECHA: 01-05-2024] [TIPO: Concierto] [LUGAR: San Vicente do Mar]
El 1 de mayo del 2024 fui con mi pareja al concierto de Iván Ferreiro en el Nautico de San Vicente do Mar
```

**Introducir entradas en el diario**
El diario tiene el contenido:

```/app/lecciones/leccion05/diario.txt```
```
Hoy tuve una reunión muy importante en la oficina de Barcelona sobre el nuevo proyecto de IA.
Fui al concierto de Rosalía en el Palau Sant Jordi el pasado 2 de noviembre de 2025, fue espectacular.
El 1 de mayo del 2024 fui con mi pareja al concierto de Iván Ferreiro en el Nautico de San Vicente do Mar
```

Desde el dicrectorio de leccion05 ejecutamos:
>> NOTA: con el modelo llama3.1:8b a veces me da error que no tiene memoria: \
>> model requires more system memory (20.0 GiB) than is available (13.9 GiB) (status code: 500)

```bash
python procesar_entrada_batch.py diario.txt
```

Resultado:
```
--- INICIANDO PROCESAMIENTO DE: diario.txt ---

Procesando: 'Hoy tuve una reunión muy importante en la oficina ...'
-> Entrada guardada con etiquetas: [FECHA: ] [TIPO: Trabajo] [LUGAR: Barcelona]

Procesando: 'Fui al concierto de Rosalía en el Palau Sant Jordi...'
-> Entrada guardada con etiquetas: [FECHA: 2025-11-02] [TIPO: Concierto] [LUGAR: Barcelona]

Procesando: 'El 1 de mayo del 2024 fui con mi pareja al concier...'
-> Entrada guardada con etiquetas: [FECHA: 2024-05-01] [TIPO: Concierto] [LUGAR: San Vicente do Mar]

--- PROCESAMIENTO DE ARCHIVO FINALIZADO ---
-> 4. Re-indexando RAG...
Base de datos RAG actualizada con 1 fragmentos.

¡El archivo RAG ha sido actualizado y está listo para ser consultado!
```

Si vamos a **/app/datos/diario/** ha creado el resumen del diario y el RAG:
```
/app/datos/diario/diario_personal_vida.txt

/app/datos/diario/diario_chroma_db
/app/datos/diario/diario_chroma_db/chroma.sqlite3
/app/datos/diario/diario_chroma_db/24a62497-881a-492c-9ba9-3638cdf0cd8f
/app/datos/diario/diario_chroma_db/24a62497-881a-492c-9ba9-3638cdf0cd8f/data_level0.bin
/app/datos/diario/diario_chroma_db/24a62497-881a-492c-9ba9-3638cdf0cd8f/length.bin
/app/datos/diario/diario_chroma_db/24a62497-881a-492c-9ba9-3638cdf0cd8f/link_lists.bin
/app/datos/diario/diario_chroma_db/24a62497-881a-492c-9ba9-3638cdf0cd8f/header.bin
```

El contenido de **diario_personal_vida.txt** es:
```
[FECHA: ] [TIPO: Trabajo] [LUGAR: Barcelona]
Hoy tuve una reunión muy importante en la oficina de Barcelona sobre el nuevo proyecto de IA.

---
[FECHA: 2025-11-02] [TIPO: Concierto] [LUGAR: Barcelona]
Fui al concierto de Rosalía en el Palau Sant Jordi el pasado 2 de noviembre de 2025, fue espectacular.

---
[FECHA: 2024-05-01] [TIPO: Concierto] [LUGAR: San Vicente do Mar]
El 1 de mayo del 2024 fui con mi pareja al concierto de Iván Ferreiro en el Nautico de San Vicente do Mar

---
```

Vemos que la fecha de la primera entrada que decía **hoy** no la ha cogido, se tendría que mejorar la API.

Ahora se podría crear otro fichero diario.txt e ir metiendo mas entradas.

Para consultar entradas del diario:
```bash
python consultar_diario.py "Como fue el concierto de Rosalia?"
```

```
Cargando el modelo de embeddings: nomic-embed-text...
Cargando la Base de Datos Vectorial desde /app/datos/diario/diario_chroma_db...
Base de datos cargada correctamente.

--- CONSULTA ---
Como fue el concierto de Rosalia?

--- RESPUESTA DEL DIARIO ---

Fue espectacular. (Se encuentra en la entrada [FECHA: 2025-11-02] [TIPO: Concierto] [LUGAR: Barcelona])
```