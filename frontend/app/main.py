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
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Centro
        )

        # Título
        titulo = Paragraph(f"FACTURA {factura['numero_factura']}", title_style)
        elements.append(titulo)
        elements.append(Spacer(1, 20))

        # Información de la factura
        info_data = [
            ["Fecha:", factura["fecha_emision"]],
            ["Cliente:", factura["cliente_nombre"]],
            ["Email:", factura["cliente_email"]],
            ["Teléfono:", factura["cliente_telefono"]],
            ["Dirección:", factura["cliente_direccion"]],
            ["Ciudad:", factura["cliente_ciudad"]],
        ]

        info_table = Table(info_data)
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                    ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )
        elements.append(info_table)
        elements.append(Spacer(1, 30))

        # Detalle de items
        detalle_data = [["Descripción", "Cantidad", "Precio Unit.", "Subtotal"]]
        for item in factura["items"]:
            detalle_data.append(
                [
                    item["descripcion"],
                    str(item["cantidad"]),
                    f"${item['precio_unitario']:,.2f} COP",
                    f"${item['subtotal']:,.2f} COP",
                ]
            )

        detalle_table = Table(detalle_data)
        detalle_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(detalle_table)
        elements.append(Spacer(1, 30))

        # Totales
        totales_data = [
            ["Subtotal:", f"${factura['subtotal']:,.2f} COP"],
            ["IVA (19%):", f"${factura['iva']:,.2f} COP"],
            ["TOTAL:", f"${factura['total']:,.2f} COP"],
        ]

        totales_table = Table(totales_data, colWidths=[100, 80])
        totales_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 1), "Helvetica"),
                    ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ]
            )
        )
        elements.append(totales_table)

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
