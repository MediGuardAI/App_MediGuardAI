from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime

def generate_risk_chart(risk_factors):
    """Creates a risk factor bar chart and returns it as an image."""
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(risk_factors.keys(), risk_factors.values(), color=['red', 'yellow', 'blue', 'green'])
    ax.set_ylabel("Risk Level (%)")
    ax.set_title("Risk Factors")
    plt.xticks(rotation=45)
    
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
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(colors.darkblue)
    pdf.drawCentredString(width / 2, height - 60, "MediGuard AI - Drug Interaction Report")
    pdf.setStrokeColor(colors.grey)
    pdf.line(50, height - 70, width - 50, height - 70)
    
    # Timestamp
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.black)
    pdf.drawString(50, height - 90, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Patient Information
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 120, "Patient Information:")
    pdf.setFont("Helvetica", 12)
    y_position = height - 140
    
    for key, value in patient_data.items():
        pdf.drawString(60, y_position, f"{key}: {value}")
        y_position -= 20
    
    # Medications List
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position - 20, "Medications and Dosages:")
    pdf.setFont("Helvetica", 12)
    y_position -= 40
    
    for med in medications:
        pdf.drawString(60, y_position, f"• {med} - {dosages.get(med, 'N/A')} mg")
        y_position -= 20
    
    # Risk Factors Table
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y_position - 20, "Risk Factors:")
    y_position -= 40
    
    table_data = [["Risk Factor", "Risk Level (%)"]] + [[k, v] for k, v in risk_factors.items()]
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(pdf, width, height)
    table.drawOn(pdf, 50, y_position - 80)
    
    y_position -= 150
    
    # Risk Factor Graph
    img_buffer = generate_risk_chart(risk_factors)
    img = Image(img_buffer, width=200, height=150)
    img.drawOn(pdf, 50, y_position - 170)
    y_position -= 200  
    
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

#need to import the function in the main script