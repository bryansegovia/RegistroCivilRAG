# RAG Local Para Terminos Del Registro Civil

Aplicacion web local de Retrieval Augmented Generation (RAG) para consultar el documento de terminos y condiciones de la Agencia Virtual del Registro Civil de Ecuador.

El asistente responde preguntas usando el contenido del PDF incluido en el proyecto. Si una pregunta no puede responderse con ese documento, debe indicarlo claramente y no inventar informacion.

## Arquitectura De La Solucion

El flujo implementado es:

1. `scripts/fetch_terms_to_pdf.py` obtiene el contenido desde `https://encuestas.registrocivil.gob.ec/terminos.html` y genera un PDF textual en `data/source/terminos_registro_civil.pdf`.
2. `app/document_loader.py` lee documentos PDF o CSV y los convierte en documentos procesables.
3. `app/ingest.py` divide el contenido en fragmentos, genera embeddings con Gemini y crea un indice vectorial local con Chroma en `data/vectorstore/`.
4. `app/rag.py` recupera los fragmentos mas relevantes y usa Gemini con un prompt estricto para responder solo con informacion del documento.
5. `app/main.py` expone la API con FastAPI y sirve la interfaz web.
6. `static/` contiene una interfaz tipo chat, sin historial persistente ni base de datos.

## Tecnologias Y Herramientas

- Python
- FastAPI
- LangChain
- Gemini API
- Chroma como vector store local
- pypdf para leer PDF
- pandas para leer CSV
- ReportLab para generar el PDF fuente
- HTML, CSS y JavaScript para la interfaz web
- pytest para pruebas automatizadas

Modelos configurados por defecto:

- Chat: `gemini-3.5-flash`
- Embeddings: `gemini-embedding-2`

## Instrucciones Para Ejecutar El Proyecto

1. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Instala dependencias:

```powershell
pip install -r requirements.txt
```

3. Configura tu API key de Gemini en el archivo `.env`:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

4. Regenera el PDF fuente si quieres actualizarlo desde la pagina oficial:

```powershell
python scripts\fetch_terms_to_pdf.py
```

5. Crea el indice vectorial:

```powershell
python -m app.ingest
```

6. Levanta la aplicacion:

```powershell
uvicorn app.main:app --reload
```

7. Abre la app en el navegador:

```text
http://127.0.0.1:8000
```

Si el indice vectorial no existe y `GEMINI_API_KEY` esta configurada, la aplicacion intentara crearlo al iniciar.

## Deploy En Streamlit Cloud

Para desplegar en Streamlit Cloud usa estos valores:

- Main file path: `streamlit_app.py`
- Python version: `3.12`
- Secrets:

```toml
GEMINI_API_KEY = "tu_api_key_aqui"
GEMINI_CHAT_MODEL = "gemini-3-flash-preview"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-2"
```

En TOML, los valores de texto deben ir entre comillas. No incluyas el archivo `.env` en GitHub; Streamlit Cloud usa los secrets anteriores como variables seguras en runtime.

## Ejemplos De Preguntas

- Quienes pueden solicitar el duplicado de cedula de identidad?
- Formas de pago disponibles
- Indicame los servicios disponibles
- Que pasa si fallo 3 veces al ingresar?
- Se puede devolver un servicio pagado?
- Donde contacto soporte si tengo problemas con una transaccion?

## Ejemplos De Respuestas Generadas

**Pregunta:** Formas de pago disponibles

**Respuesta esperada:**

De acuerdo con los terminos y condiciones de la Agencia Virtual del Registro Civil, la forma de pago disponible en el Portal Web es mediante tarjetas de credito Visa o Mastercard. La entidad emisora de la tarjeta debe autorizar la solicitud de pago; si no la autoriza, la compra se cancela y se notifica al usuario. Luego de validar el pago, el usuario puede acceder a los servicios electronicos adquiridos y el pedido se actualiza a estado "Pagado".

**Pregunta:** Existen formas que mi cuenta sea bloqueada?

**Respuesta esperada:**

Si. Segun el documento, la cuenta puede bloquearse automaticamente despues de 3 intentos fallidos de ingreso de datos en la pantalla de acceso. La institucion tambien se reserva la posibilidad de bloquear usuarios si identifica mal uso del Portal Web. Ademas, puede cancelar o suspender cuentas si el usuario proporciona informacion falsa, inexacta o incompleta, o si existen indicios de vulneracion de seguridad. Para desbloquear una cuenta bloqueada por intentos fallidos, el usuario debe usar la opcion de restaurar contrasena y responder las preguntas de seguridad definidas.

**Pregunta:** Cual es el horario de visita del hospital universitario?

**Respuesta esperada:**

No lo se con la informacion disponible. Solo cuento con informacion del documento de terminos y condiciones de la Agencia Virtual del Registro Civil de Ecuador.

## Pruebas

Ejecuta:

```powershell
pytest
```

Las pruebas no llaman a Gemini. Validan carga de documentos, fragmentacion, prompt anti-alucinacion y contrato del endpoint `/api/chat` con un servicio simulado.

## Estructura Del Proyecto

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
