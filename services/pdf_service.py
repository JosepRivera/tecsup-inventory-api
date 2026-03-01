import os
from datetime import datetime
from utils.date_utils import get_now_lima
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

EXPORTS_DIR = "exports"

def _estilos():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="Titulo",
        fontSize=16,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Subtitulo",
        fontSize=10,
        fontName="Helvetica",
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="SeccionHeader",
        fontSize=11,
        fontName="Helvetica-Bold",
        spaceBefore=12,
        spaceAfter=4,
        textColor=colors.HexColor("#1a1a2e"),
    ))
    styles.add(ParagraphStyle(
        name="Celda",
        fontSize=8,
        fontName="Helvetica",
        leading=11,
    ))
    styles.add(ParagraphStyle(
        name="CeldaBold",
        fontSize=8,
        fontName="Helvetica-Bold",
        leading=11,
    ))
    return styles


def _tabla_activos(activos: list, styles) -> Table:
    encabezado = ["#", "Nombre", "Modelo", "N° Serie", "Estado", "Técnico", "Origen", "Hora"]
    filas = [encabezado]

    for i, a in enumerate(activos, start=1):
        # Extraer solo la hora si existe el campo creado_en
        hora = a.get("creado_en", "")[11:16] if a.get("creado_en") and len(a.get("creado_en")) > 16 else a.get("creado_en", "")[-8:-3]
        if not hora and a.get("creado_en"): # Fallback por si el formato varía
             hora = a.get("creado_en", "")[-5:]

        fila = [
            Paragraph(str(i), styles["Celda"]),
            Paragraph(a.get("nombre") or "-", styles["Celda"]),
            Paragraph(a.get("modelo") or "-", styles["Celda"]),
            Paragraph(a.get("numero_serie") or "-", styles["CeldaBold"]),
            Paragraph(a.get("estado") or "-", styles["Celda"]),
            Paragraph(a.get("tecnico") or "-", styles["Celda"]),
            Paragraph(a.get("origen") or "-", styles["Celda"]),
            Paragraph(hora or "-", styles["Celda"]),
        ]
        filas.append(fila)

    # Ajuste de anchos para que quepa en A4 Vertical (Total ~17cm)
    col_widths = [0.7*cm, 3.8*cm, 2.8*cm, 2.7*cm, 1.8*cm, 2.2*cm, 1.2*cm, 1.8*cm]

    tabla = Table(filas, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        # Encabezado
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        # Filas alternas
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        # Bordes
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.HexColor("#1a1a2e")),
        # Padding general
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return tabla


def generar_pdf_sesion(activos: list, sesion: dict = None) -> str:
    """
    Genera el PDF de resumen (de sesión o global) y lo guarda en exports/.
    Retorna la ruta del archivo generado.
    """
    os.makedirs(EXPORTS_DIR, exist_ok=True)

    now = get_now_lima()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    prefijo = f"sesion_{sesion.get('id', 'x')}" if sesion else "inventario_global"
    nombre_archivo = f"{prefijo}_{timestamp}.pdf"
    ruta = os.path.join(EXPORTS_DIR, nombre_archivo)

    doc = SimpleDocTemplate(
        ruta,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = _estilos()
    story = []

    # Encabezado
    story.append(Paragraph("Tecsup — Departamento de Tecnología Digital", styles["Titulo"]))
    story.append(Paragraph("Resumen de Sesión de Inventariado", styles["Subtitulo"]))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a1a2e")))
    story.append(Spacer(1, 0.3*cm))

    # Datos de sesión
    story.append(Paragraph("Resumen de Datos", styles["SeccionHeader"]))

    if sesion:
        ubicacion = " / ".join(filter(None, [
            sesion.get("pabellon"),
            sesion.get("laboratorio"),
            sesion.get("armario"),
        ])) or "No especificada"
        # Incluir hora en la fecha de corte para sesiones
        fecha = sesion.get("creada_en", "")[:16] if sesion.get("creada_en") else ""
        header_text = "Información de la Jornada"
    else:
        ubicacion = "Inventario Completo (Todo el campus)"
        fecha = get_now_lima().strftime("%Y-%m-%d %H:%M")
        header_text = "Reporte Global Consolidado"

    info_sesion = [
        ["Técnico Responsable:", sesion.get("tecnico") or "N/A"] if sesion else ["Generado por:", "Sistema Inventario"],
        ["Ubicación / Alcance:", ubicacion],
        ["Fecha y Hora de corte:", fecha],
        ["Total de activos registrados:", str(len(activos))],
        ["Registrados por OCR:", str(sum(1 for a in activos if a.get("origen") == "ocr"))],
        ["Registrados por voz:", str(sum(1 for a in activos if a.get("origen") == "voz"))],
        ["Registrados manualmente:", str(sum(1 for a in activos if a.get("origen") == "manual"))],
    ]

    tabla_info = Table(info_sesion, colWidths=[6*cm, 10*cm])
    tabla_info.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a1a2e")),
    ]))
    story.append(tabla_info)
    story.append(Spacer(1, 0.5*cm))

    # Tabla de activos
    if activos:
        story.append(Paragraph("Activos Registrados", styles["SeccionHeader"]))
        story.append(_tabla_activos(activos, styles))
    else:
        story.append(Paragraph("No se registraron activos en esta sesión.", styles["Normal"]))

    # Pie de página con fecha de generación
    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.2*cm))
    generado = get_now_lima().strftime("%d/%m/%Y %H:%M:%S")
    story.append(Paragraph(f"Documento generado el {generado}", styles["Subtitulo"]))

    doc.build(story)
    return ruta