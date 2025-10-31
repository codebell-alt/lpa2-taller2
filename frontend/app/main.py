import os
from io import BytesIO

import requests
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # Cambiar en producción
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


@app.route("/")
def index():
    """Página principal con formulario"""
    return render_template("index.html")


@app.route("/api/factura/<numero_factura>")
def obtener_factura(numero_factura):
    """Endpoint para obtener datos de factura (para AJAX)"""
    try:
        response = requests.get(f"{BACKEND_URL}/facturas/v1/{numero_factura}")

        if response.status_code != 200:
            return jsonify({"error": "Factura no encontrada"}), 404

        return response.json()

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Error de conexión con el servidor"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generar-pdf", methods=["POST"])
def generar_pdf():
    """Genera PDF de la factura"""
    try:
        numero_factura = request.form["numero_factura"]
        response = requests.get(f"{BACKEND_URL}/facturas/v1/{numero_factura}")

        if response.status_code != 200:
            flash("Factura no encontrada", "error")
            return redirect(url_for("index"))

        factura = response.json()

        # Crear buffer para PDF
        buffer = BytesIO()
        
        # Configurar documento con márgenes apropiados
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=20,
            spaceAfter=20,
            spaceBefore=10,
            alignment=1,  # Centro
            textColor=colors.darkblue
        )
        
        section_style = ParagraphStyle(
            "SectionStyle",
            parent=styles["Heading2"],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        )

        # Título principal
        titulo = Paragraph(f"FACTURA {factura['numero_factura']}", title_style)
        elements.append(titulo)
        elements.append(Spacer(1, 30))

        # Sección información del cliente
        info_titulo = Paragraph("Información del Cliente", section_style)
        elements.append(info_titulo)
        
        # Información de la factura con anchos específicos
        info_data = [
            ["Fecha:", factura["fecha_emision"]],
            ["Cliente:", factura["cliente_nombre"]],
            ["Email:", factura["cliente_email"]],
            ["Teléfono:", factura["cliente_telefono"]],
            ["Dirección:", factura["cliente_direccion"]],
            ["Ciudad:", factura["cliente_ciudad"]],
        ]

        # Tabla de información con anchos definidos
        info_table = Table(info_data, colWidths=[120, 300])
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.darkblue),
                    ("ALIGN", (0, 0), (0, -1), "RIGHT"),
                    ("ALIGN", (1, 0), (1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 11),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        elements.append(info_table)
        elements.append(Spacer(1, 30))

        # Sección detalle de productos/servicios
        detalle_titulo = Paragraph("Detalle de Productos/Servicios", section_style)
        elements.append(detalle_titulo)

        # Detalle de items con anchos específicos
        detalle_data = [["Descripción", "Cant.", "Precio Unitario", "Subtotal"]]
        for item in factura["items"]:
            # Truncar descripción si es muy larga
            descripcion = item["descripcion"]
            if len(descripcion) > 40:
                descripcion = descripcion[:37] + "..."
                
            detalle_data.append(
                [
                    descripcion,
                    str(item["cantidad"]),
                    f"${item['precio_unitario']:,.0f} COP",
                    f"${item['subtotal']:,.0f} COP",
                ]
            )

        # Tabla de detalles con anchos específicos
        detalle_table = Table(detalle_data, colWidths=[200, 50, 100, 120])
        detalle_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, 0), 11),
                    ("FONTSIZE", (0, 1), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]
            )
        )
        elements.append(detalle_table)
        elements.append(Spacer(1, 30))

        # Sección totales
        totales_titulo = Paragraph("Resumen de Totales", section_style)
        elements.append(totales_titulo)

        # Totales con formato mejorado
        totales_data = [
            ["Subtotal:", f"${factura['subtotal']:,.0f} COP"],
            ["IVA (19%):", f"${factura['iva']:,.0f} COP"],
            ["", ""],  # Línea separadora
            ["TOTAL:", f"${factura['total']:,.0f} COP"],
        ]

        totales_table = Table(totales_data, colWidths=[150, 120])
        totales_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 2), "Helvetica"),
                    ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 2), 12),
                    ("FONTSIZE", (0, 3), (-1, 3), 14),
                    ("TEXTCOLOR", (0, 3), (-1, 3), colors.darkblue),
                    ("BACKGROUND", (0, 3), (-1, 3), colors.lightblue),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LINEABOVE", (0, 2), (-1, 2), 1, colors.grey),
                    ("LINEABOVE", (0, 3), (-1, 3), 2, colors.darkblue),
                    ("SPAN", (0, 2), (-1, 2)),  # Línea separadora
                ]
            )
        )
        
        # Alinear totales a la derecha
        elements.append(Spacer(1, 20))
        
        # Crear tabla contenedora para alinear totales a la derecha
        container_data = [["", totales_table]]
        container_table = Table(container_data, colWidths=[200, 270])
        container_table.setStyle(
            TableStyle([
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        
        elements.append(container_table)

        # Pie de página
        elements.append(Spacer(1, 40))
        footer_style = ParagraphStyle(
            "FooterStyle",
            parent=styles["Normal"],
            fontSize=9,
            alignment=1,  # Centro
            textColor=colors.grey
        )
        footer = Paragraph(
            "Gracias por su preferencia - Este documento es válido como factura electrónica",
            footer_style
        )
        elements.append(footer)

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"factura_{numero_factura}.pdf",
            mimetype="application/pdf",
        )

    except requests.exceptions.ConnectionError:
        flash("Error de conexión con el servidor", "error")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Error generando PDF: {str(e)}", "error")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
