from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from io import BytesIO
import matplotlib.pyplot as plt

def generate_risk_chart(risk_factors):
    """Creates a risk factor bar chart and returns it as an image."""
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(risk_factors.keys(), risk_factors.values(), color=['#E63946', '#F4A261', '#2A9D8F', '#264653'])
    ax.set_ylabel("Risk Level (%)", fontsize=12, fontweight='bold', color='#264653')
    ax.set_title("Risk Factors", fontsize=14, fontweight='bold', color='#264653')
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    return img_buffer

def export_to_pdf(medications, dosages, patient_data, risk_factors, detailed_analysis):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    pdf.setTitle("Drug Interaction Report")
    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(colors.darkblue)
    pdf.drawCentredString(width / 2, height - 80, "MediGuard AI - Drug Interaction Report")
    pdf.setStrokeColor(colors.grey)
    pdf.setLineWidth(2)
    pdf.line(50, height - 90, width - 50, height - 90)
    
    # Patient Information
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(colors.black)
    pdf.drawString(50, height - 130, "Patient Information:")
    pdf.setFont("Helvetica", 12)
    y_position = height - 150

    for i, (key, value) in enumerate(patient_data.items()):
        pdf.setFillColor(colors.darkblue if i % 2 == 0 else colors.darkred)
        pdf.drawString(60, y_position, f"{key}: {value}")
        y_position -= 20

    # Medications List
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position - 20, "Medications and Dosages:")
    pdf.setFont("Helvetica", 12)
    y_position -= 40

    for med, dose in zip(medications, dosages):
        pdf.drawString(60, y_position, f"• {med} - {dose}")
        y_position -= 20

    # Risk Factors Table
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position - 20, "Risk Factors:")
    y_position -= 40

    table_data = [["Risk Factor", "Risk Level (%)"]] + [[k, v] for k, v in risk_factors.items()]
    table = Table(table_data, colWidths=[250, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, y_position - 80)
    
    y_position -= 150  # Adjust for table height

    # Risk Factor Graph
    img_buffer = generate_risk_chart(risk_factors)
    img = Image(img_buffer, width=250, height=180)
    img.drawOn(pdf, 50, y_position - 190)
    y_position -= 220

    # Detailed Analysis
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position - 20, "Detailed Analysis:")
    pdf.setFont("Helvetica", 12)
    y_position -= 40

    for section, content in detailed_analysis.items():
        pdf.setFillColor(colors.darkblue)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(60, y_position, section)
        y_position -= 20
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)
        for item in content:
            pdf.drawString(70, y_position, f"• {item}")
            y_position -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
