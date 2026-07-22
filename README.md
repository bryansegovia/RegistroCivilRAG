# RAG Local Para Términos Del Registro Civil

Aplicación local de Retrieval Augmented Generation (RAG) para conversar con el documento de términos y condiciones de la Agencia Virtual del Registro Civil de Ecuador.

El sistema no guarda conversaciones en base de datos. El historial existe solo en el navegador mientras la página está abierta.

## Arquitectura

- `scripts/fetch_terms_to_pdf.py` descarga los términos desde `https://encuestas.registrocivil.gob.ec/terminos.html` y genera un PDF textual en `data/source/terminos_registro_civil.pdf`.
- `app/document_loader.py` lee documentos PDF o CSV y los divide en fragmentos.
- `app/ingest.py` crea embeddings con Gemini y guarda el índice local en Chroma (`data/vectorstore/`).
- `app/rag.py` recupera fragmentos relevantes y responde con Gemini usando un prompt estricto para no inventar datos.
- `app/main.py` expone FastAPI y sirve la interfaz web.
- `static/` contiene la UI tipo chat.

## Tecnologías

- Python
- FastAPI
- LangChain
- Gemini API
- Chroma como vector store local
- pypdf para PDF
- pandas para CSV
- ReportLab para generar el PDF fuente

Modelos por defecto:

- Chat: `gemini-3.5-flash`
- Embeddings: `gemini-embedding-2`

## Configuración

1. Crea y activa el entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instala dependencias:

```powershell
pip install -r requirements.txt
```

3. Pega tu API key en `.env`:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

También puedes ajustar los modelos en `.env` si tu cuenta no tiene acceso a los modelos por defecto.

## Uso

Regenerar el PDF fuente:

```powershell
python scripts\fetch_terms_to_pdf.py
```

Crear el índice vectorial:

```powershell
python -m app.ingest
```

Levantar la aplicación:

```powershell
uvicorn app.main:app --reload
```

Abre `http://127.0.0.1:8000`.

Si el índice no existe y `GEMINI_API_KEY` está configurada, la app lo crea al iniciar.

## Ejemplos De Preguntas

- ¿Qué servicios están disponibles?
- ¿Qué pasa si fallo 3 veces al ingresar?
- ¿Qué formas de pago acepta el portal?
- ¿Se puede devolver un servicio pagado?
- ¿Dónde contacto soporte si tengo problemas con una transacción?

Para preguntas fuera del documento, el asistente debe indicar que no conoce la respuesta con la información disponible y aclarar que solo cuenta con el contenido de los términos y condiciones.

## Pruebas

```powershell
pytest
```

Las pruebas no llaman a Gemini. Validan carga de documentos, fragmentación, prompt anti-alucinación y contrato del endpoint `/api/chat` con un servicio simulado.

## Estructura

```text
app/
  config.py
  document_loader.py
  ingest.py
  main.py
  prompts.py
  rag.py
data/
  source/
    terminos_registro_civil.pdf
scripts/
  fetch_terms_to_pdf.py
static/
  index.html
  styles.css
  app.js
tests/
```
