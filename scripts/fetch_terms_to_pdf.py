from __future__ import annotations

import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SOURCE_URL = "https://encuestas.registrocivil.gob.ec/terminos.html"
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "source" / "terminos_registro_civil.pdf"

FALLBACK_TEXT = """
Términos y Condiciones de Agencia Virtual

El uso, servicios y transacciones de este portal Web se rige bajo los términos y condiciones contenidos en este documento, sujeto a la normativa vigente, los usuarios del portal Web podrán solicitar lo servicios electrónicos conforme los términos, condiciones y normativa aplicable al servicio solicitado.
Se entenderá que los usuarios prestan su consentimiento, expreso, libre y voluntario, a los términos y condiciones aquí establecidos, mediante la aceptación de los mismos a través de los medios establecidos en este portal Web.

CONTENIDO
1. OBJETO
2. CONDICIONES DE SERVICIOS
3. SERVICIOS DISPONIBLES
4. FORMAS DE PAGO
5. DISPONIBILIDAD
6. CAMBIOS Y DEVOLUCIONES
7. SOPORTE
8. RESPONSABILIDAD
9. CAMBIO EN LOS TÉRMINOS
10. ACEPTACIÓN

1. OBJETO
El presente documento de términos y condiciones de uso del servicio regula el acceso y la utilización del portal Web de la institución, incluyendo los contenidos y los servicios puestos a disposición de los usuarios.

2. CONDICIONES DE SERVICIO
a. Acceso al portal:
El Usuario se obliga a no acceder a los contenidos y/o servicios del portal Web, por ningún otro medio que no sea la interfaz que la institución proporcione al Usuario para acceder a los mismos.

b. Identidad del Usuario:
El usuario se obliga a proporcionar única y exclusivamente los datos individuales y personales respecto de su identidad, no falsear la identidad de terceros haciéndose pasar por otra persona, ficticia o real.

c. Actividades contrarias a la Ley, la moral y el orden público:
El usuario se obliga a proporcionar única y exclusivamente los datos individuales y personales respecto de su identidad, no falsear la identidad de terceros haciéndose pasar por otra persona, ficticia o real.

d. Registro del Usuario:
En relación al proceso de registro, el usuario está obligado a facilitar información veraz, exacta y completa sobre su identidad, en relación con los datos que le sean solicitados, así como a mantener actualizada dicha información.
Si el usuario facilitará inexactitud de datos, información falsa, datos incompletos, falta de concordancia, e indicios de vulneración de seguridades, la institución podrá cancelar, suspender, e incluso investigar la o las cuentas registradas, conforme la Ley, Reglamentos o Instructivos lo consideren pertinente.

e. Contraseña:
El usuario definirá, durante su registro la contraseña que le permitirá el acceso personalizado, confidencial y seguro. El usuario registrado tendrá la posibilidad de cambiar la contraseña de acceso, para lo cual deberá sujetarse al procedimiento establecido en el portal Web.

f. Uso de los datos personales registrados en el portal Web:
Los datos referidos en estos términos y condiciones para el registro y solicitud de servicios electrónicos, tendrán como finalidad validar las órdenes de compra o pedidos.
Esta información es de carácter confidencial y su manejo se rige por la Política de Seguridad y de Confidencialidad de la Institución.

g. Código de validación:
La institución por medio del portal Web, realiza la generación de códigos de validación, el usuario deberá registrar el código de validación generado que le permitirá realizar sus transacciones de manera segura y confidencial.
El código de validación tendrá 6 caracteres y estará compuesta por números y letras en mayúsculas/minúsculas.

h. Bloqueo de usuario:
Por seguridad, la cuenta de usuario se bloqueará automáticamente luego de detectar 3 intentos fallidos de ingreso de datos en la pantalla de Ingreso. La Institución se reserva la posibilidad de bloquear usuarios de los cuales se identifique el mal uso del Portal Web.
Para desbloquear la cuenta, el usuario deberá ingresar a la opción de Restaurar contraseña, responder las preguntas de seguridad definidas para el efecto.

i. Cancelación de Cuentas:
El usuario reconoce y acepta que la Institución se reserva el derecho a cancelar las cuentas que se hallen inactivas durante un periodo de tiempo razonable.

3. SERVICIOS DISPONIBLES
a. Solicitud de Certificados Electrónicos de Datos o Actos Civiles.
El usuario puede solicitar en línea los siguientes certificados:
- Certificados electrónicos de Nacimiento, Matrimonio, Unión de Hecho, Identidad y Estado Civil para el titular de la información.
- Certificados electrónicos de Nacimiento, Matrimonio, Unión de Hecho, Identidad y Estado Civil, Defunción para familiares (hijos menores de 18 años, padres fallecidos, cónyuge/conviviente legalmente constituido).
Los certificados en formato electrónico tienen plena validez jurídica, son firmados digitalmente por la máxima autoridad de la institución. Esto de conformidad con el artículo 4 numeral 1 de la Ley Orgánica de Gestión de Identidad y Datos Civiles y la Ley de Comercio Electrónico; en consecuencia, no requieren ser legalizados o materializados adicionalmente.
Es importante indicar que la institución pública o privada donde se presenta el certificado electrónico debe validarlo en el portal WEB: virtual.registrocivil.gob.ec, ingresando el número de certificado ubicado en la parte inferior izquierda del mismo o a su vez la Institución puede escanear el código QR, habilitado para dispositivos móviles.

b. Consulta de condición de donante de órganos, tejidos y células
La Institución por medio del portal Web, garantiza el acceso rápido y gratuito a la consulta de la condición de Donante de Órganos, Tejidos y Células.
Se podrá visualizar las siguientes condiciones de donante:
- SI DONANTE: Significa que el usuario(a) ha manifestado de forma voluntaria ante la Dirección General de Registro Civil, Identificación y Cedulación (DIGERCIC) al momento de obtener su documento de identidad, ya sea por primera vez o renovación, su afirmación respecto al donar sus órganos, tejidos y células. Acorde a la ley aplica a mayores de edad.
- SI DONANTE POR LEY: Significa que por Ley Orgánica de Donación y Trasplante de Órganos, Tejidos y Células, las ecuatorianas, ecuatorianos y extranjeros residentes legales en el país, mayores de dieciocho años, al fallecer se convertirán automáticamente en donantes de los órganos, tejidos o células. Acorde a la ley aplica a mayores de edad.
- DONATE SOLO TEJIDOS: Significa que el usuario(a) ha manifestado de forma voluntaria ante la Dirección General de Registro Civil, Identificación y Cedulación (DIGERCIC) al momento de obtener su documento de identidad, ya sea por primera vez o renovación, su afirmación respecto al donar parcialmente sus órganos, tejidos y células. Acorde a la ley aplica para mayores de edad.
- NO DONANTE. Significa que el usuario(a) ha manifestado de forma voluntaria ante la Dirección General de Registro Civil, Identificación y Cedulación (DIGERCIC) al momento de obtener su documento de identidad, ya sea por primera vez o renovación, su negativa respecto al donar sus órganos, tejidos y células. Acorde a la ley aplica para mayores de edad.
Para los casos de menores de edad: La Donación de Órganos, Tejidos y Células NO APLICA, conforme lo establece el Artículo 10 del Reglamento de la LEY ORGÁNICA DE DONACIÓN Y TRASPLANTES DE ÓRGANOS, TEJIDOS Y CÉLULAS.

c. Solicitud de Duplicado de Cédula de Identidad
Servicio al que podrán acogerse todos los ciudadanos ecuatorianos mayores de edad que han obtenido la cédula de identidad electrónica en policarbonato y que deseen un duplicado por reposición del último documento emitido.
Al acceder al servicio de duplicado, se estará aceptando que la impresión del documento de identidad será con los mismos datos biométricos y biográficos de la última cédula emitida.
Es importante indicar que para la solicitud de este servicio se aplican condiciones de validación interna, que se detallan a continuación:
- El servicio de duplicado únicamente se podrá generar siempre que el último documento entregado sea el del Sistema de Emisión de Documentos de Identidad y Pasaportes (SEDIP).
- No se podrá emitir duplicado de cédulas de para usuarios menores de edad.
- No se podrá emitir duplicado de cédulas si la fecha de emisión y la de actualización son diferentes.
- No se podrá emitir duplicado de cédulas a usuarios extranjeros residentes permanentes y/o temporales.
- No se podrá emitir duplicado de cédulas a usuarios que cuenten en su último documento emitido, la fecha de expiración 2 días posteriores a la fecha de solicitud.
- No se podrá emitir duplicado de cédulas para usuarios que el último documento de identificación se encuentre invalidado por caducidad o contribución de cualquier índole.
- No se podrá emitir un duplicado si la última entrega de la cédula se la realizó en el Corporación del Registro Civil de Guayaquil.
Condiciones de entrega del duplicado de cédula de identidad:
La entrega del duplicado de cédula de identidad se realizará luego de dos (2) horas laborables, una vez recibida la confirmación del pago del servicio, de lunes a viernes, de 08:30 a 17:00, en las agencias habilitadas.
La entrega del duplicado de la cédula se realiza en la agencia escogida y de manera presencial, mediante la validación de huella digital. No es factible que el documento de identidad sea retirado por un tercero, a pesar de que tenga una autorización simple.
El duplicado de cédula de identidad podrá ser destruido en caso de que no sea retirado luego de tres (3) meses posteriores a la fecha de impresión y el mismo no haya sido retirado.

4. FORMAS DE PAGO
La forma de pago disponible en el Portal Web es:
1. Tarjetas de crédito Visa o Mastercard.
La entidad emisora de la tarjeta recibirá una solicitud de pago, y responderá con una autorización o rechazo. En caso de que la entidad no autorice la compra la misma será cancelada y se le enviará un mensaje al usuario indicándole que la compra no fue autorizada por la entidad correspondiente.
Luego de haber realizado la validación del pago, el usuario podrá acceder a los servicios electrónicos adquiridos y se actualizará el estado del pedido a «Pagado». Para el efecto, se utilizarán los mecanismos de facturación electrónica legalmente permitidos.

5. DISPONIBILIDAD
La Institución realizará todos los esfuerzos que sean razonables para garantizar la disponibilidad y accesibilidad al portal Web, veinticuatro horas al día durante todos los días del año.
No obstante, en ocasiones, y, por ejemplo, debido a causas como el suministro de nuevas conexiones, los cambios de direccionamiento, operaciones de mantenimiento y, en general, situaciones que estén fuera del control de la Institución, podrán producirse interrupciones en el acceso, o utilización del portal Web, por el tiempo que resulte necesario para solucionar tales inconvenientes.

6. CAMBIOS Y DEVOLUCIONES
Una vez que el servicio fue pagado, éste no es susceptible de devolución.

7. SOPORTE
En caso de incidentes o preguntas acerca de sus transacciones, y si se considera que hubo un error en relación con sus transacciones electrónicas, contáctenos al número (593) 023731110 o al correo electrónico enlinea@registrocivil.gob.ec

8. RESPONSABILIDAD
El usuario registrado asume totalmente la responsabilidad por la confidencialidad de su contraseña registrada en el portal Web de la DIGERCIC, garantizando el adecuado acceso a los servicios electrónicos relacionados a su Identidad, a los registros de sus Hechos y Actos Civiles.
El usuario tendrá la posibilidad de recuperar o cambiar su contraseña, para lo cual deberá sujetarse al procedimiento establecido en este portal Web.
La contraseña es de uso personal y su entrega y uso por terceros no involucra responsabilidad de la institución, en caso de mala utilización.
El usuario es el único responsable del uso autorizado de sus credenciales de acceso al portal Web.
El usuario reconoce y acepta que la utilización del portal web será efectuada con fines estrictamente personales, privados y particulares.
Queda expresamente prohibido el uso o aplicación de cualquier recurso técnico, lógico o tecnológico en cuya virtud los usuarios puedan beneficiarse, directa o indirectamente, con o sin fines de lucro, de la explotación no autorizada de los contenidos y/o servicios del portal Web.

9. CAMBIO EN LOS TÉRMINOS
La DIGERCIC, se reserva la facultad para (agregar, eliminar o modificar) estos términos de uso y condiciones previa notificación al usuario.

10. ACEPTACIÓN
La aceptación por parte del usuario, implica su sometimiento a las condiciones aquí descritas para el uso del portal Web, sin que pueda alegarse desconocimiento alguno sobre las mismas.
""".strip()


def fetch_terms_text() -> str:
    try:
        response = requests.get(SOURCE_URL, timeout=20)
        response.raise_for_status()
    except requests.RequestException:
        return FALLBACK_TEXT

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n", strip=True)
    start = text.find("Términos y Condiciones de Agencia Virtual")
    end = text.find("Entérate")
    if start == -1:
        return FALLBACK_TEXT

    selected = text[start : end if end != -1 else len(text)]
    selected = re.sub(r"\n{3,}", "\n\n", selected)
    return selected.strip()


def paragraph_style(name: str, font_size: int, leading: int, space_after: int, bold: bool = False) -> ParagraphStyle:
    base = getSampleStyleSheet()["Normal"]
    return ParagraphStyle(
        name,
        parent=base,
        fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=font_size,
        leading=leading,
        spaceAfter=space_after,
    )


def build_pdf(text: str, output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Términos y Condiciones de Agencia Virtual",
        author="Registro Civil, Identificación y Cedulación",
    )

    styles = {
        "title": paragraph_style("TitleCustom", 16, 20, 12, True),
        "heading": paragraph_style("HeadingCustom", 12, 16, 8, True),
        "body": paragraph_style("BodyCustom", 9, 13, 6),
        "source": paragraph_style("SourceCustom", 8, 11, 10),
    }

    story = [
        Paragraph("Términos y Condiciones de Agencia Virtual", styles["title"]),
        Paragraph(f"Fuente oficial: {SOURCE_URL}", styles["source"]),
    ]

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue

        escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        is_heading = bool(re.match(r"^(\d{1,2}\.\s|CONTENIDO$|[a-i]\.\s)", line))
        story.append(Paragraph(escaped, styles["heading" if is_heading else "body"]))

    doc.build(story)
    return output_path


if __name__ == "__main__":
    result = build_pdf(fetch_terms_text())
    print(f"PDF generado: {result}")
