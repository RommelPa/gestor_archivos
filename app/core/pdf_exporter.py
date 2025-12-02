from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime

def export_history_to_pdf(history, output_path):
    """
    Genera un PDF con el historial de archivos procesados.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("<b>Historial de Archivos Procesados</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.3 * inch))

    for entry in history:
        line = (
            f"<b>Archivo:</b> {entry['filename']}<br/>"
            f"<b>Destino:</b> {entry['destino']}<br/>"
            f"<b>Fecha:</b> {entry['fecha']}<br/><br/>"
        )
        story.append(Paragraph(line, styles['BodyText']))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    return output_path