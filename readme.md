# Generador de Facturas

Este proyecto muestra cómo armar una app sencilla en Flask que genera facturas en PDF usando flask, flask-sqlalchemy, bootstrap y weasyprint. La forma más común de crear PDFs con Python puro es Reportlab, pero lleva bastante tiempo lograr que el diseño quede como uno quiere. Aquí uso weasyprint para generar la factura en PDF a partir de una plantilla HTML.

## Primeros pasos

### Instalar dependencias

#### Python 3.7

Instala la versión de Python que corresponda a tu plataforma siguiendo la [documentación de Python](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Entorno virtual

Conviene trabajar dentro de un entorno virtual en cualquier proyecto de Python. Así las dependencias de cada proyecto quedan separadas y ordenadas. Las instrucciones para crear uno en tu plataforma están en la [documentación de Python](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Dependencias con PIP

Con el entorno virtual activo, entra a la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instala todos los paquetes listados en `requirements.txt`.

##### Dependencias principales

- [Flask](http://flask.pocoo.org/) es un framework ligero para el backend. Se encarga de las peticiones y respuestas.

- [SQLAlchemy](https://www.sqlalchemy.org/) es el ORM que usamos para manejar la base de datos SQLite. Casi todo el trabajo está en `app.py`, y los modelos se definen en `models.py`.

- [WeasyPrint](https://weasyprint.readthedocs.io/en/stable/index.html) ayuda a crear documentos PDF a partir de HTML. Aquí convierte una página HTML sencilla en la factura en PDF.

### Correr el servidor

Desde la carpeta del proyecto, con el entorno virtual activo. Las variables de entorno están en el archivo `.flaskenv`:
- Con `FLASK_ENV=development` el servidor se reinicia solo cuando detecta cambios en los archivos.
- Con `FLASK_APP=app.py` Flask sabe qué aplicación debe ejecutar.

Para iniciar el servidor, ejecuta desde la carpeta del proyecto:

```bash
flask run
```

## Modelos
- Positions: cada registro es un concepto de la factura.
- InvoiceDetails: guarda los datos de la factura, como la información del cliente y el periodo facturado.

## Endpoints

### Inicio
```
GET '/'
```
- Devuelve la plantilla `index.html`, que hereda de `main.html` con la herencia de plantillas de jinja2.
### Formulario de conceptos, tabla de conceptos y formulario de factura
```
GET '/invoice_data'
```
- Devuelve la plantilla `invoice_form.html`, que hereda de `main.html`.
- En la primera ejecución solo muestra el `PositionsForm`.
- Si ya hay registros en `Positions`, muestra la tabla de conceptos y el `InvoiceForm`.
- Si ya hay un registro en `InvoiceDetails`, rellena el `InvoiceForm` con esos datos.
### Agregar concepto
```
POST '/invoice_data'
envío del PositionsForm
```
- Valida el `PositionsForm` en el servidor con `flask-wtf`.
- Guarda el concepto nuevo en la base de datos con el método `insert()`.
### Crear factura
```
POST '/invoice_data'
envío del InvoiceForm
```
- Valida el `InvoiceForm` en el servidor con `flask-wtf`.
- Guarda los datos con `insert()` si todavía no hay ningún registro en `InvoiceDetails`.
- Si ya existe uno, lo sobrescribe con el método `update(**kwargs)`.
- Nota: en `InvoiceDetails` solo hay un registro.
### Eliminar conceptos
```
DELETE '/position_delete'
```
- Borra de `Positions` el concepto cuyo id se manda en el cuerpo de la petición.

Cuerpo de la petición:
```
{
    "position_id": "<id del concepto>"
}
```
Respuesta:
```
{
    "url": "<url del formulario de factura (GET)>"
}
```
### Crear PDF de la factura
```
POST '/invoice_pdf'
```
- Consulta los datos guardados en `Positions` y `InvoiceDetails` para rellenar la plantilla de la factura.
- Pasa la plantilla renderizada como cadena al `HTML` de weasyprint y entrega el PDF desde memoria con `send_file` de Flask.
- Se usa BytesIO porque `send_file` necesita un objeto con método `read()`.
